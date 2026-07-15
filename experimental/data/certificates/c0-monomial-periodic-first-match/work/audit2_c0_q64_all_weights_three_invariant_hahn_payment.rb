#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent hostile audit of the broadened all-fixed-residual/all-full-block-
# weight q64 periodic theorem.  The claimant and its verifier are hash-pinned
# but not imported.  Hahn witnesses are reconstructed from ordinary root
# products in a complete Hahn basis.

require 'digest'
require 'json'

ROOT = File.expand_path('..', __dir__)
P = 2_130_706_433
ZETA = 1_548_376_985
TARGET = 274_854_110_496_187_592
N = 64
MASK64 = (1 << 64) - 1

CLAIMANT_PINS = {
  'work/C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md' =>
    '99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b',
  'work/verify_c0_q64_three_invariant_hahn_payment.rb' =>
    'baf78eb9a8e297220bf69484f110bc108f88fb083d1e0693e05f570fa76722a5',
  'work/verify_c0_q64_three_invariant_hahn_payment.expected.txt' =>
    '28cd93bf4472d29537a267a7c84360f6f7c26eb9795aa4758e2a105383dcbba1'
}.freeze

SOURCE_PINS = {
  'work/DEPLOYED_C0_Q64_PERIODIC_FIXED_Q_REDUCTION.md' =>
    '8b2d84ffb344bbb0a78c904358645322f5159c20c152760ea7cd97354228fc69',
  'work/PROFILE1792_MU64_SHORT_TRADES_SQL_OUTPUT.txt' =>
    '58780e11b9c45d507e1daacbcb5be2548b82228bfe38e3e5c4e2d9f412211416',
  'work/HOSTILE_AUDIT3_MU64_DISTANCE7_GAP_ORBIT_CENSUS.md' =>
    '3542ad6a7f394fe7a0bae5d45c12598a045768997497448145976fff64e2b43a',
  'work/PROFILE1792_MU64_SIZE8_TRADE_CLASSIFICATION.md' =>
    '143341369f91a8965960d943a520ea0eb410b1ac5b82e7d447968dac9ebfa19e',
  'work/PROFILE1792_MU64_SIZE9_TRADE_CENSUS.md' =>
    'ebe4101c29d00cb4354b1cce6291b4640a4e457b69827c012dbdda292c5a7690',
  'work/mu64_size9_two_moment_records_compact.analysis.json' =>
    '3686fa22df3d93e85bb660f81667182e45ed2ec9c3cdf4b1aa8e3685eaf959b5'
}.freeze

CERTIFICATES = {
  8 => [7, [], 8],
  9 => [6, [9], 11],
  10 => [6, [9], 26],
  11 => [6, [10, 11], 91],
  12 => [18, [10, 12], 220],
  13 => [16, [10, 12, 13], 516],
  14 => [16, [10, 12, 13], 1_091],
  15 => [16, [10, 12, 13, 15], 3_093],
  16 => [32, [10, 12, 13, 15, 16], 10_217],
  17 => [28, [10, 12, 13, 15, 16], 20_908],
  18 => [28, [10, 12, 13, 15, 16, 18], 57_196],
  19 => [28, [10, 12, 13, 15, 16, 19], 145_025],
  20 => [46, [10, 12, 13, 15, 16, 18, 19], 296_899],
  21 => [40, [10, 12, 13, 15, 16, 18, 19], 614_503],
  22 => [40, [10, 12, 13, 15, 16, 18, 19, 22], 1_241_710],
  23 => [40, [10, 12, 13, 15, 16, 18, 19, 21, 22], 2_465_809],
  24 => [59, [10, 12, 13, 15, 16, 18, 19, 20, 21], 3_954_000],
  25 => [52, [10, 12, 13, 15, 16, 18, 19, 20, 21], 6_287_643],
  26 => [52, [10, 12, 13, 15, 16, 18, 19, 20, 21, 26], 10_193_410],
  27 => [52, [10, 12, 13, 15, 16, 18, 19, 21, 22, 27], 14_641_173],
  28 => [72, [10, 12, 13, 15, 16, 18, 19, 21, 22, 26, 27], 20_826_085],
  29 => [72, [10, 12, 13, 15, 16, 18, 19, 20, 21, 24, 25], 25_307_496]
}.freeze

def assert(condition, label)
  raise "AUDIT2 FAILURE: #{label}" unless condition
end

def choose(n, k)
  return 0 if k.negative? || k > n

  k = [k, n - k].min
  (1..k).reduce(1) { |answer, j| answer * (n - k + j) / j }
end

def mod_pow(base, exponent)
  answer = 1
  power = base % P
  until exponent.zero?
    answer = answer * power % P if exponent.odd?
    exponent >>= 1
    power = power * power % P unless exponent.zero?
  end
  answer
end

def rotate(mask, shift)
  shift %= 64
  return mask if shift.zero?

  ((mask << shift) | (mask >> (64 - shift))) & MASK64
end

def mask_indices(mask)
  (0...64).select { |j| ((mask >> j) & 1) == 1 }
end

def hahn(degree, distance, weight)
  (0..degree).reduce(Rational(0, 1)) do |answer, q|
    answer + Rational(
      (-1)**q * choose(degree, q) * choose(N + 1 - degree, q) *
        choose(distance, q),
      choose(weight, q) * choose(N - weight, q)
    )
  end
end

def solve(matrix, rhs)
  dimension = rhs.length
  dimension.times do |column|
    pivot = (column...dimension).find { |row| !matrix[row][column].zero? }
    raise 'singular independent all-weight Hahn system' unless pivot

    matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
    rhs[column], rhs[pivot] = rhs[pivot], rhs[column]
    divisor = matrix[column][column]
    (column...dimension).each { |j| matrix[column][j] /= divisor }
    rhs[column] /= divisor
    dimension.times do |row|
      next if row == column

      multiplier = matrix[row][column]
      next if multiplier.zero?

      (column...dimension).each do |j|
        matrix[row][j] -= multiplier * matrix[column][j]
      end
      rhs[row] -= multiplier * rhs[column]
    end
  end
  rhs
end

CLAIMANT_PINS.merge(SOURCE_PINS).each do |relative, digest|
  assert(Digest::SHA256.file(File.join(ROOT, relative)).hexdigest == digest,
         "hash pin #{relative}")
end
assert(P - 1 == 127 * (2**24), 'deployed p-1 factorization')
assert(mod_pow(ZETA, 64) == 1 && mod_pow(ZETA, 32) == P - 1,
       'literal primitive mu64 root')

# Independently enumerate maximal full/empty coset completions.  A four-loop
# compares every selected pair with every empty pair directly; unlike the
# claimant verifier, no pair-sum histograms are used.
labels = (0...16).to_a
partition_count = 0
a8_caps = {}
CERTIFICATES.each do |weight, (claimed_cap, _zeros, _fiber_cap)|
  full_count = weight / 4
  empty_count = (64 - weight) / 4
  maximum = -1
  labels.combination(full_count) do |full|
    rest = labels - full
    rest.combination(empty_count) do |empty|
      degree = 0
      full.combination(2) do |a, b|
        empty.combination(2) do |c, d|
          degree += 1 if (a + b - c - d) % 16 == 0
        end
      end
      maximum = degree if degree > maximum
      partition_count += 1
    end
  end
  assert(maximum == claimed_cap, "A8 cap at weight #{weight}")
  a8_caps[weight] = maximum
end
assert(partition_count == 606_060, 'all-weight completion count')

# Recheck the complete returned size-nine witness population in the literal
# field and expand the product-equal part under C64.
roots = (0...64).map { |j| mod_pow(ZETA, j) }
analysis = JSON.parse(File.binread(File.join(
  ROOT, 'work/mu64_size9_two_moment_records_compact.analysis.json'
)))
witnesses = analysis.fetch('first_witnesses')
assert(analysis.fetch('disjoint_pairs') == 55 && witnesses.length == 55,
       'size-nine complete witness input')
product_equal_bases = []
witnesses.each do |row|
  left = row.fetch(1).to_i(16)
  right = row.fetch(2).to_i(16)
  li = mask_indices(left)
  ri = mask_indices(right)
  assert(li.length == 9 && ri.length == 9 && (left & right).zero?,
         'size-nine disjoint weights')
  lv = li.map { |j| roots[j] }
  rv = ri.map { |j| roots[j] }
  le1 = lv.sum % P
  re1 = rv.sum % P
  le2 = lv.combination(2).sum { |x, y| x * y } % P
  re2 = rv.combination(2).sum { |x, y| x * y } % P
  assert(le1 == re1 && le2 == re2, 'size-nine literal moments')
  lp = lv.reduce(1) { |answer, value| answer * value % P }
  rp = rv.reduce(1) { |answer, value| answer * value % P }
  product_equal_bases << [left, right] if lp == rp
end
assert(product_equal_bases.length == 1, 'one product-equal size-nine orbit')
literal_nine_trades = {}
product_equal_bases.each do |left, right|
  (0...64).each do |shift|
    literal_nine_trades[[rotate(left, shift), rotate(right, shift)].sort] = true
  end
end
assert(literal_nine_trades.length == 64, 'A9 global universe')

# Reconstruct each claimed Hahn polynomial from its ordinary factorization.
# For root set Z, expand prod_z(x-z) in H_0,...,H_|Z| using values at
# 0,...,|Z|, then normalize the H_0 coefficient.  This is independent of the
# claimant's inhomogeneous prescribed-zero solve.
caps = (0..7).to_h { |weight| [weight, 1] }
bounds = {}
coefficient_stream = []
CERTIFICATES.each do |weight, (a8_cap, zeros, expected_cap)|
  degree = zeros.length
  raw_values = (0..degree).map do |distance|
    zeros.reduce(1) { |answer, root| answer * (distance - root) }.to_r
  end
  matrix = (0..degree).map do |distance|
    (0..degree).map { |j| hahn(j, distance, weight) }
  end
  raw_coefficients = solve(matrix, raw_values)
  assert(!raw_coefficients[0].zero?, "nonzero H0 coefficient weight #{weight}")
  coefficients = raw_coefficients.map { |value| value / raw_coefficients[0] }
  assert(coefficients[0] == 1 && coefficients.drop(1).all?(&:positive?),
         "positive Hahn coefficients weight #{weight}")

  polynomial = lambda do |distance|
    (0..degree).sum(Rational(0, 1)) do |j|
      coefficients[j] * hahn(j, distance, weight)
    end
  end
  (0..weight).each do |distance|
    ordinary = Rational(
      zeros.reduce(1) { |answer, root| answer * (distance - root) },
      raw_coefficients[0]
    )
    assert(polynomial.call(distance) == ordinary,
           "Hahn/ordinary identity weight #{weight} distance #{distance}")
  end
  assert((10..weight).all? { |distance| polynomial.call(distance) <= 0 },
         "full sign domain weight #{weight}")
  paid8 = a8_cap * [polynomial.call(8), 0].max
  paid9 = weight >= 9 ? 64 * [polynomial.call(9), 0].max : 0
  bound = polynomial.call(0) + paid8 + paid9
  cap = bound.floor
  assert(cap == expected_cap, "fiber cap weight #{weight}")
  caps[weight] = cap
  bounds[weight] = bound
  coefficient_stream << "w=#{weight};z=#{zeros.join(',')};" +
                        coefficients.drop(1).each_with_index.map do |value, j|
                          "#{j + 1}:#{value.numerator}/#{value.denominator}"
                        end.join('|')
end
coefficient_digest = Digest::SHA256.hexdigest(coefficient_stream.join("\n"))
assert(coefficient_digest ==
       '6b9fdd32619e2fd8ae53b05ac16de82e6c532bc18afecbeafda3fc66187d1d20',
       'all-weight coefficient digest')
uniform_cap = caps.values.max
assert(uniform_cap == caps.fetch(29) && uniform_cap == 25_307_496,
       'all-weight maximum')
assert(bounds.fetch(29) == Rational(7_162_373_179_063_296, 283_013_891),
       'weight29 exact rational')

# For every fixed residual support R, A_R(0) is nonzero because H is
# multiplicative.  Thus multiplication by A_R is invertible modulo X^a and
# preserves both equality and projective proportionality after cancellation.
# For fixed weight, c0(Q_S)=(-1)^f P_S lies in mu64.  Consequently any one
# projective ray has at most 64 nonempty absolute scalar cells.
coarse_cap = (P - 1) * uniform_cap
sharp_cap = 64 * uniform_cap
assert(coarse_cap < TARGET && sharp_cap < TARGET, 'projective arithmetic')

puts 'HOSTILE_AUDIT2_C0_Q64_ALL_WEIGHTS_THREE_INVARIANT_HAHN: PASS'
puts "claimant_pins=#{CLAIMANT_PINS.length} source_pins=#{SOURCE_PINS.length} weights=0..29"
puts "a8_partitions=#{partition_count} a8_caps=#{a8_caps.values.join(',')}"
puts "size9_orbits=#{witnesses.length} product_equal_orbits=#{product_equal_bases.length} literal_trades=#{literal_nine_trades.length} A9<=64"
puts "weight_caps=#{caps.values.join(',')}"
puts "coefficient_sha256=#{coefficient_digest} weight29_bound=#{bounds.fetch(29)} uniform_cap=#{uniform_cap}"
puts "coarse_p_minus_1_cap=#{coarse_cap} margin=#{TARGET - coarse_cap}"
puts "scalar_cells_per_ray<=64 sharp_cap=#{sharp_cap} margin=#{TARGET - sharp_cap}"
puts 'scope=for each fixed residual support separately and each f=0..29 full-block lane; no sum over residuals/general-g/uniform-c0/official payment'
