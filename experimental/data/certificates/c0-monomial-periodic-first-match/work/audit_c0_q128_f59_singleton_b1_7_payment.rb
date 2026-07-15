#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent hostile replay for C0_Q128_F59_SINGLETON_B1_7_PAYMENT.md.
# This does not import the claimant verifier.  It checks the source pins,
# coefficient window, singleton-certificate injection, the reduction to the
# accepted q64 caps, all target arithmetic, and the coarse-first routing.

require 'digest'

def assert(condition, message)
  raise message unless condition
end

def binom(n, k)
  return 0 if k.negative? || k > n

  k = [k, n - k].min
  (1..k).inject(1) { |acc, j| acc * (n - k + j) / j }
end

root = File.expand_path('..', __dir__)
pins = {
  'C0_Q128_F59_SINGLETON_B1_7_PAYMENT.md' =>
    '90aa42d622ae074f4a7a39e9acb894873978127c1a69d51bb122e4c93c89d143',
  'verify_c0_q128_f59_singleton_b1_7_payment.rb' =>
    '237c6118f1c8985d58ebd387d449aaddac395acb1f31ab9a4e8e6450c4529458',
  'verify_c0_q128_f59_singleton_b1_7_payment.expected.txt' =>
    'b85b4ce5545e669c0c3cdb2b94f00cf488bbe12fa8ec33c9dde485c8af349511',
  'C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md' =>
    '99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b',
  'verify_c0_q64_three_invariant_hahn_payment.rb' =>
    'baf78eb9a8e297220bf69484f110bc108f88fb083d1e0693e05f570fa76722a5',
  'verify_c0_q64_three_invariant_hahn_payment.expected.txt' =>
    '28cd93bf4472d29537a267a7c84360f6f7c26eb9795aa4758e2a105383dcbba1',
  'C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER_PAYMENT.md' =>
    '704524424be7dc8b411a71011f8f8eb63ae88f9e7f4ebcfd100420e23c322ad5',
  'HOSTILE_AUDIT_C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER_PAYMENT.md' =>
    'c1e4bdef06b71d881df7a35477e4d364f4d84692ac011ee5443bb4178d3e3225',
  'C0_Q64_F28_RESIDUAL_PENCIL_PAYMENT.md' =>
    '9c0142793a738513f8a83801ff2536cd2a463b8f377a34be716ca5744b1f4709',
  'HOSTILE_AUDIT_C0_Q64_F28_RESIDUAL_PENCIL_PAYMENT.md' =>
    '8f6870c1f834f06507823fa60101c75230b4610588bad8bb9c5451b46c3488f6'
}.freeze

pins.each do |name, expected|
  path = File.join(root, 'work', name)
  assert(File.file?(path), "missing pin #{name}")
  assert(Digest::SHA256.file(path).hexdigest == expected, "pin drift #{name}")
end

p = 2_130_706_433
n = 2_097_152
t = 981_105
a = 67_472
block = 16_384
residual = 14_449
target = 274_854_110_496_187_592

assert(t == 59 * block + residual, 'q128 footprint decomposition')
assert(n == 128 * block && (p - 1) % 128 == 0, 'literal q128 ledger')
assert(residual < block, 'residual owner degree window')
assert(4 * block < a && a < 5 * block, 'four normalized coefficient blocks')
assert([2, 3, 4].all? { |j| (p % j) != 0 }, 'Newton/cubic denominators')

# Accepted fixed-(product, inverse first moment, inverse second moment) q64
# caps, pinned above.  Only the four exact double-pair weights are consumed.
q64_caps = {
  29 => 25_307_496,
  28 => 20_826_085,
  27 => 14_641_173,
  26 => 10_193_410
}.freeze

singleton_caps = {
  1 => 1,
  3 => binom(128, 1) / binom(3, 2),
  5 => binom(128, 3) / binom(5, 2),
  7 => binom(128, 5) / binom(7, 2)
}.freeze
assert(singleton_caps == {1 => 1, 3 => 42, 5 => 34_137, 7 => 12_598_400},
       'two-odd-moment certificate arithmetic')

rows = singleton_caps.map do |singletons, hcap|
  doubles = (59 - singletons) / 2
  coarse_residual = residual + singletons * block
  contribution = hcap * q64_caps.fetch(doubles)
  [singletons, doubles, coarse_residual, hcap, q64_caps.fetch(doubles),
   contribution]
end

assert(rows.map { |row| row[1] } == [29, 28, 27, 26], 'coarse weights')
assert(rows.map { |row| row[2] } == [30_833, 63_601, 96_369, 129_137],
       'coarse residual degrees')
assert(rows.map { |row| [row[0], row[1]] }.uniq.length == 4,
       'occupancy cells disjoint')

absolute = rows.sum { |row| row[5] }
projective = 128 * absolute
new_rows = rows.select { |row| row[0] >= 5 }
new_absolute = new_rows.sum { |row| row[5] }
new_projective = 128 * new_absolute

assert(absolute == 128_921_362_269_767, 'absolute sum')
assert(projective == 16_501_934_370_530_176, 'projective sum')
assert(new_absolute == 128_920_462_266_701, 'coarse-first absolute sum')
assert(new_projective == 16_501_819_170_137_728, 'coarse-first projective sum')
assert(projective < target && new_projective < target, 'target margins')

# Independent finite-field stress test of the singleton certificate.  In
# mu_16 over F_257, (sum u, sum u^3) uniquely determines a no-antipodal
# omitted pair.  For each b, certificates of size b-2 are disjoint inside
# every moment fiber exactly as used in the proof.
p0 = 257
zeta = 3.pow(16, p0)
roots = Array.new(16) { |i| zeta.pow(i, p0) }
assert(zeta.pow(16, p0) == 1 && zeta.pow(8, p0) == p0 - 1,
       'small-field primitive root')

pair_labels = {}
(0...16).to_a.combination(2) do |i, j|
  next if (i - j).abs == 8

  u = roots[i]
  v = roots[j]
  s = (u + v) % p0
  h = (u.pow(3, p0) + v.pow(3, p0)) % p0
  assert(!s.zero?, 'no-antipodal pair has zero sum')
  uv = ((s.pow(3, p0) - h) * (3 * s).pow(p0 - 2, p0)) % p0
  assert(uv == (u * v) % p0, 'cubic reconstruction')
  key = [s, h]
  assert(!pair_labels.key?(key), 'two-odd-moment omitted-pair collision')
  pair_labels[key] = [i, j]
end

small_stats = {}
[1, 3, 5, 7].each do |b|
  families = Hash.new { |hash, key| hash[key] = [] }
  (0...16).to_a.combination(b) do |indices|
    next if indices.any? { |i| indices.include?((i + 8) % 16) }

    key = [indices.sum { |i| roots[i] } % p0,
           indices.sum { |i| roots[i].pow(3, p0) } % p0]
    families[key] << indices
  end

  if b == 1
    assert(families.values.all? { |family| family.length == 1 },
           'b=1 first moment is not injective')
  else
    families.each_value do |family|
      seen = {}
      family.each do |indices|
        indices.combination(b - 2) do |certificate|
          assert(!seen.key?(certificate), "certificate collision b=#{b}")
          seen[certificate] = indices
        end
      end
    end
  end
  small_stats[b] = [families.length, families.values.map(&:length).max]
end

puts 'HOSTILE_AUDIT_C0_Q128_F59_SINGLETON_B1_7_PAYMENT: PASS'
puts "pins=#{pins.length} q128_B=#{block} residual=#{residual} a=#{a}=4B+1936"
puts 'ray_invariants=normalized_e1_e2_e3_e4; q0_cells<=128; residual_owned=true'
rows.each do |b, d, coarse_residual, hcap, qcap, contribution|
  puts "b=#{b} d=#{d} coarse_residual=#{coarse_residual} H_b<=#{hcap} q64_cap=#{qcap} absolute=#{contribution}"
end
puts "all_b1_7_projective=#{projective} margin=#{target - projective}"
puts "coarse_first_new_b5_b7=#{new_projective} margin=#{target - new_projective}"
puts "small_mu16_pair_keys=#{pair_labels.length} singleton_stats=#{small_stats.map { |b, v| "b#{b}:#{v.join('/')}" }.join(',')}"
puts 'coarse_first=b1->f29,b3->f28 deleted; new=b5->f27,b7->f26'
puts 'nonclaim=b>=9,q128_f54..58,general_g,all_c0,and_official_question remain open'
