#!/usr/bin/env ruby
# frozen_string_literal: true

require 'digest'

def check(condition, message)
  raise message unless condition
end

def choose(n, k)
  return 0 if k.negative? || k > n
  k = [k, n - k].min
  (1..k).inject(1) { |v, i| v * (n - k + i) / i }
end

root = File.expand_path('..', __dir__)
pins = {
  'C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md' =>
    '99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b',
  'verify_c0_q64_three_invariant_hahn_payment.rb' =>
    'baf78eb9a8e297220bf69484f110bc108f88fb083d1e0693e05f570fa76722a5',
  'verify_c0_q64_three_invariant_hahn_payment.expected.txt' =>
    '28cd93bf4472d29537a267a7c84360f6f7c26eb9795aa4758e2a105383dcbba1'
}
pins.each do |name, digest|
  path = File.join(root, 'work', name)
  check(File.file?(path), "missing pinned input #{name}")
  check(Digest::SHA256.file(path).hexdigest == digest, "pin drift #{name}")
end

p = 2_130_706_433
n = 2_097_152
t = 981_105
a = 67_472
b128 = 16_384
target = 274_854_110_496_187_592

check(t == 59 * b128 + 14_449, 'q128 top decomposition')
check(a == 4 * b128 + 1_936, 'four normalized coefficient window')
check(14_449 < b128 && 4 * b128 < a && a < 5 * b128,
      'ownership and coefficient inequalities')
check((p - 1) % 128 == 0 && n == 128 * b128, 'literal subgroup ledger')
check((p % 3) != 0, 'singleton cubic identity characteristic')

q64_caps = {
  29 => 25_307_496,
  28 => 20_826_085,
  27 => 14_641_173,
  26 => 10_193_410
}

singleton_caps = {}
[1, 3, 5, 7].each do |b|
  singleton_caps[b] = if b == 1
                        1
                      else
                        choose(128, b - 2) / choose(b, 2)
                      end
end
check(singleton_caps == {1 => 1, 3 => 42, 5 => 34_137, 7 => 12_598_400},
      'singleton certificate caps')

rows = [1, 3, 5, 7].map do |b|
  d = (59 - b) / 2
  residual = 14_449 + b * b128
  [b, d, residual, singleton_caps.fetch(b), q64_caps.fetch(d),
   singleton_caps.fetch(b) * q64_caps.fetch(d)]
end

check(rows.map { |row| row[1] } == [29, 28, 27, 26], 'coarse q64 counts')
check(rows.map { |row| row[2] } == [30_833, 63_601, 96_369, 129_137],
      'coarse residual degrees')

absolute_sum = rows.sum { |row| row[5] }
projective_sum = 128 * absolute_sum
new_absolute = rows.select { |row| row[0] >= 5 }.sum { |row| row[5] }
new_projective = 128 * new_absolute

check(absolute_sum == 128_921_362_269_767, 'absolute all-b sum')
check(projective_sum == 16_501_934_370_530_176, 'projective all-b sum')
check(new_absolute == 128_920_462_266_701, 'absolute first-match-new sum')
check(new_projective == 16_501_819_170_137_728, 'projective first-match-new sum')
check(projective_sum < target && new_projective < target, 'target payments')

# Deterministic small-field anti-tamper replay of the two-odd-moment
# certificate: in a no-antipodal family, one (b-2)-subset cannot extend in
# two different ways at fixed first and third sums.
p0 = 257
zeta = 3.pow((p0 - 1) / 16, p0)
roots = Array.new(16) { |i| zeta.pow(i, p0) }
families = Hash.new { |h, key| h[key] = [] }
(0...16).to_a.combination(5) do |idx|
  next if idx.any? { |i| idx.include?((i + 8) % 16) }
  key = [idx.sum { |i| roots[i] } % p0,
         idx.sum { |i| roots[i].pow(3, p0) } % p0]
  families[key] << idx
end
families.each_value do |family|
  seen = {}
  family.each do |idx|
    idx.combination(3) do |cert|
      check(!seen.key?(cert), 'small singleton certificate collision')
      seen[cert] = idx
    end
  end
end

puts 'RESULT: PASS'
puts "q128_B=#{b128} residual=14449 a=#{a}=4B+1936"
puts 'normalized_invariants=e1,e2,e3,e4 absolute_product_cells=128'
rows.each do |b, d, residual, hcap, dcap, contribution|
  puts "b=#{b} q64_f=#{d} coarse_residual=#{residual} singleton_cap=#{hcap} q64_cap=#{dcap} absolute_contribution=#{contribution}"
end
puts "all_b_le7_absolute=#{absolute_sum} projective=#{projective_sum} margin=#{target - projective_sum}"
puts "first_match_new_b5_b7_absolute=#{new_absolute} projective=#{new_projective} margin=#{target - new_projective}"
puts "small_no_antipodal_five_set_moment_classes=#{families.length}"
puts 'nonclaim=b_ge9_f54_58_general_g_and_official_question_remain_open'
