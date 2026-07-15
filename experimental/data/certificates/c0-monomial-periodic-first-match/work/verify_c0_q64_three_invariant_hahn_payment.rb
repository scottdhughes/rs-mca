#!/usr/bin/env ruby
# frozen_string_literal: true

# Exact replay for the fixed-residual q64 periodic lane in the deployed c=0
# binary-apolar projective residue fiber.  Standard library only.

require 'digest'
require 'json'

P = 2_130_706_433
TARGET = 274_854_110_496_187_592
N = 64
ZETA = 1_548_376_985

# Each row stores [pointwise A8 cap, Hahn zero set, expected integer cap].
WEIGHT_CERTIFICATES = {
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

ROOT = File.expand_path('..', __dir__)
PINS = {
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

def check(condition, message)
  raise message unless condition
end

def choose(n, k)
  return 0 if k.negative? || k > n

  k = [k, n - k].min
  (1..k).inject(1) { |value, index| value * (n - k + index) / index }
end

def hahn(degree, distance, weight)
  (0..degree).sum(Rational(0, 1)) do |q|
    Rational(
      (-1)**q * choose(degree, q) * choose(N + 1 - degree, q) *
        choose(distance, q),
      choose(weight, q) * choose(N - weight, q)
    )
  end
end

def solve_linear(matrix, rhs)
  dimension = rhs.length
  dimension.times do |column|
    pivot = (column...dimension).find { |row| !matrix[row][column].zero? }
    raise 'singular exact system' unless pivot

    matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
    rhs[column], rhs[pivot] = rhs[pivot], rhs[column]
    scale = matrix[column][column]
    (column...dimension).each { |j| matrix[column][j] /= scale }
    rhs[column] /= scale

    dimension.times do |row|
      next if row == column

      factor = matrix[row][column]
      next if factor.zero?

      (column...dimension).each do |j|
        matrix[row][j] -= factor * matrix[column][j]
      end
      rhs[row] -= factor * rhs[column]
    end
  end
  rhs
end

PINS.each do |relative, digest|
  path = File.join(ROOT, relative)
  check(Digest::SHA256.file(path).hexdigest == digest, "pin drift: #{relative}")
end

check(P - 1 == 127 * (2**24), 'deployed prime factorization')
check(ZETA.pow(64, P) == 1 && ZETA.pow(32, P) == P - 1,
      'deployed primitive mu64 root')

# A distance-eight full-invariant trade is, after inversion, an exchange of
# two full mu4 cosets for two disjoint full mu4 cosets with equal label sum
# modulo 16.  For every weight 8..29, exhaust the maximal possible sets of
# full and empty cosets.  Extending smaller such sets only adds exchanges.
labels = (0...16).to_a
partitions = 0
computed_a8 = {}
WEIGHT_CERTIFICATES.each do |weight, (expected_a8, _zeros, _cap)|
  full_count = weight / 4
  empty_count = (64 - weight) / 4
  maximum = -1
  labels.combination(full_count) do |full|
    remaining = labels - full
    remaining.combination(empty_count) do |empty|
      full_sums = Hash.new(0)
      empty_sums = Hash.new(0)
      full.combination(2) { |x, y| full_sums[(x + y) % 16] += 1 }
      empty.combination(2) { |x, y| empty_sums[(x + y) % 16] += 1 }
      degree = (0...16).sum { |sum| full_sums[sum] * empty_sums[sum] }
      maximum = degree if degree > maximum
      partitions += 1
    end
  end
  check(maximum == expected_a8,
        "distance-eight cap drift at weight #{weight}: #{maximum}")
  computed_a8[weight] = maximum
end
check(partitions == 606_060, 'all-weight full/empty partition census')

# The accepted complete size-nine two-moment census has 55 rotation-orbit
# representatives.  Recompute the product exponent on both aligned wings.
# Exactly one orbit also has equal product, hence the full three-invariant
# trade universe contains 64 literal distance-nine trades.
analysis_path = File.join(
  ROOT, 'work/mu64_size9_two_moment_records_compact.analysis.json'
)
analysis = JSON.parse(File.read(analysis_path))
witnesses = analysis.fetch('first_witnesses')
check(witnesses.length == 55 && analysis.fetch('disjoint_pairs') == 55,
      'size-nine witness census')
product_equal_orbits = 0
witness_masks = []
witnesses.each do |row|
  left = row[1].to_i(16)
  right = row[2].to_i(16)
  check((left & right).zero?, 'size-nine wings not disjoint')
  check(left.digits(2).sum == 9 && right.digits(2).sum == 9,
        'size-nine wing weight')
  left_sum = (0...64).select { |index| ((left >> index) & 1) == 1 }.sum % 64
  right_sum = (0...64).select { |index| ((right >> index) & 1) == 1 }.sum % 64
  product_equal_orbits += 1 if left_sum == right_sum
  witness_masks << left << right
end
check(witness_masks.uniq.length == 110, 'representative wing collision')
check(product_equal_orbits == 1,
      "product-equal size-nine orbit drift: #{product_equal_orbits}")
max_a9 = 64

# Exact Delsarte/Hahn certificates for every possible number 8..29 of full
# blocks.  Weights 0..7 have cap one because their maximum Johnson distance
# is below the already proved minimum distance eight.
coefficient_stream = []
caps = (0..7).to_h { |weight| [weight, 1] }
bounds = {}
WEIGHT_CERTIFICATES.each do |weight, (max_a8, zeros, expected_cap)|
  degrees = (1..zeros.length).to_a
  matrix = zeros.map do |distance|
    degrees.map { |degree| hahn(degree, distance, weight) }
  end
  coefficients = solve_linear(matrix, Array.new(zeros.length, -1.to_r))
  check(coefficients.all?(&:positive?),
        "nonpositive Hahn coefficient at weight #{weight}")

  polynomial = lambda do |distance|
    1 + degrees.each_with_index.sum(Rational(0, 1)) do |degree, index|
      coefficients[index] * hahn(degree, distance, weight)
    end
  end

  check((1..weight).all? { |degree| hahn(degree, 0, weight) == 1 },
        "Hahn normalization at weight #{weight}")
  check((10..weight).all? { |distance| polynomial.call(distance) <= 0 },
        "Hahn sign failure at weight #{weight}")
  check((10..weight).select { |distance| polynomial.call(distance).zero? } ==
        zeros.reject { |distance| distance == 9 },
        "Hahn zero-set drift at weight #{weight}")

  paid8 = max_a8 * [polynomial.call(8), 0].max
  paid9 = weight >= 9 ? max_a9 * [polynomial.call(9), 0].max : 0
  bound = 1 + coefficients.sum + paid8 + paid9
  cap = bound.floor
  check(cap == expected_cap,
        "exact fixed-scalar cap drift at weight #{weight}: #{cap}")
  caps[weight] = cap
  bounds[weight] = bound
  coefficient_stream << "w=#{weight};z=#{zeros.join(',')};" +
                        coefficients.each_with_index.map do |value, index|
                          "#{index + 1}:#{value.numerator}/#{value.denominator}"
                        end.join('|')
end

coefficient_digest = Digest::SHA256.hexdigest(coefficient_stream.join("\n"))
check(coefficient_digest ==
      '6b9fdd32619e2fd8ae53b05ac16de82e6c532bc18afecbeafda3fc66187d1d20',
      "all-weight Hahn coefficient drift: #{coefficient_digest}")

cap = caps.values.max
check(cap == caps[29] && cap == 25_307_496, 'uniform full-block cap')
check(cap < TARGET / (P - 1), 'fixed-scalar target not paid')

projective_cap = (P - 1) * cap
margin = TARGET - projective_cap
check(margin.positive?, 'projective periodic lane not paid')
ray_scalar_cells = 64
narrow_ray_cap = ray_scalar_cells * cap
check(narrow_ray_cap < TARGET, 'narrow projective ray not paid')

puts 'C0_Q64_THREE_INVARIANT_HAHN_PAYMENT: PASS'
puts "pins=#{PINS.length} field=#{P} quotient=#{N} full_block_weights=0..29"
puts "a8_partitions=#{partitions} a8_caps=#{computed_a8.values.join(',')}"
puts "size9_two_moment_orbits=#{witnesses.length} product_equal_orbits=#{product_equal_orbits} A9<=#{max_a9}"
puts "weight_caps=#{caps.values.join(',')} coefficient_sha256=#{coefficient_digest}"
puts "weight29_exact_bound=#{bounds[29]} floor=#{cap} fixed_scalar_target_floor=#{TARGET / (P - 1)}"
puts "projective_cap=#{projective_cap} target=#{TARGET} margin=#{margin}"
puts "ray_scalar_cells<=#{ray_scalar_cells} narrow_ray_cap=#{narrow_ray_cap}"
puts 'scope=all fixed-residual 0..29-full-mu32768-block periodic lanes; no sum over residuals or uniform c0 claim'
