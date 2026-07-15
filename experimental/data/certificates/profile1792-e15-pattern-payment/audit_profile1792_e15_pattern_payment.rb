#!/usr/bin/env ruby
# Independent exact reconstruction of the Profile1792 e15=32 payment.

T = 274_854_110_496_187_592
U_DYADIC = 57_121_027_290_597_096
OLD_CAP = 121_502_836_610_262
TOTAL_PROFILES = 1_792

def assert(condition, label)
  raise "audit failed: #{label}" unless condition
end

def choose(n, k)
  return 0 if k.negative? || k > n
  k = [k, n - k].min
  (1..k).reduce(1) { |acc, i| acc * (n - k + i) / i }
end

# Keys are [weight, count_size_2, count_size_4, ...].
states = { [0] => 1, [1] => 1 }
(1..6).each do |height|
  size = 1 << height
  next_states = Hash.new(0)
  states.each do |left, left_number|
    states.each do |right, right_number|
      weight = left[0] + right[0]
      width = [left.length, right.length].max - 1
      counts = (0...width).map do |i|
        left.fetch(i + 1, 0) + right.fetch(i + 1, 0)
      end
      counts << (weight == size ? 1 : 0)
      next_states[[weight, *counts]] += left_number * right_number
    end
  end
  states = next_states
end

weight_32_total = states.sum { |key, count| key[0] == 32 ? count : 0 }
assert(weight_32_total == choose(64, 32), "weight-32 total")

rows = []
states.each do |key, count|
  next unless key[0] == 32
  e16, e17, e18, e19, e20, _e21 = key[1, 6]
  next unless e16 <= 15 && e17 <= 7 && e18 <= 3 && e19 <= 1 && e20.zero?
  rows << [[32, e16, e17, e18, e19, e20], count]
end

assert(rows.length == 166, "residual profile count")
assert(rows.sum { |_, count| count } == choose(64, 32) - 601_080_390,
       "residual pattern total")

paid, unpaid = rows.partition { |_, count| count <= OLD_CAP }
assert(paid.length == 110, "paid count")
assert(unpaid.length == 56, "unpaid count")

paid_total = paid.sum { |_, count| count }
saving = paid.length * OLD_CAP - paid_total
remaining = TOTAL_PROFILES - paid.length
new_cap, margin = (T - U_DYADIC - paid_total).divmod(remaining)

assert(paid_total == 904_093_061_906_432, "paid aggregate")
assert(saving == 12_461_218_965_222_388, "saving")
assert(remaining == 1_682, "remaining profiles")
assert(new_cap == 128_911_409_122_285, "relaxed cap")
assert(margin == 694, "margin")
assert(U_DYADIC + paid_total + remaining * new_cap == T - margin,
       "add-back")

largest_profile, largest_count = rows.max_by { |_, count| count }
smallest_unpaid_profile, smallest_unpaid_count = unpaid.min_by { |_, count| count }
assert(largest_profile == [32, 8, 1, 0, 0, 0], "largest profile")
assert(largest_count == 247_029_899_691_294_720, "largest count")
assert(smallest_unpaid_profile == [32, 13, 3, 0, 0, 0],
       "smallest unpaid profile")
assert(smallest_unpaid_count == 170_870_483_976_192,
       "smallest unpaid count")

puts "PROFILE1792_E15_32_PATTERN_PAYMENT_INDEPENDENT_AUDIT: PASS"
puts "residual_e15_32_profiles=#{rows.length}"
puts "paid_profiles=#{paid.length} unpaid_e15_32_profiles=#{unpaid.length}"
puts "paid_exact_aggregate=#{paid_total}"
puts "uniform_budget_saving=#{saving}"
puts "remaining_all_profiles=#{remaining}"
puts "relaxed_uniform_cap=#{new_cap}"
puts "closing_margin=#{margin}"
puts "largest_profile=#{largest_profile.inspect} count=#{largest_count}"
puts "smallest_unpaid_profile=#{smallest_unpaid_profile.inspect} count=#{smallest_unpaid_count}"
