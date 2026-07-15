#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent ascending-part hostile replay.  Does not load claimant verifier.

require "digest"

def check(value, message)
  raise message unless value
end

def ascending_profiles(double_count)
  target_count = 211 - double_count
  rows = []
  counts = Array.new(14, 0)
  search = nil
  search = lambda do |part, left_count, left_sum, left_square|
    if part == 14
      rows << counts.dup if left_count.zero? && left_sum.zero? && left_square.zero?
      return
    end
    maximum = [left_count, left_sum / part,
               left_square / (part * part)].min
    (0..maximum).each do |multiplicity|
      c = left_count - multiplicity
      s = left_sum - multiplicity * part
      q = left_square - multiplicity * part * part
      next if s < c * (part + 1) || q < c * (part + 1) * (part + 1)
      next if s > 13 * c || q > 169 * c
      counts[part] = multiplicity
      search.call(part + 1, c, s, q)
    end
    counts[part] = 0
  end
  search.call(1, target_count, 208, 676)
  rows
end

def high_multiplicities(row)
  values = []
  (2..13).each { |x| row[x].times { values << x + 2 } }
  values
end

rows44 = ascending_profiles(44)
rows45 = ascending_profiles(45)
check(rows44.length == 4 && rows45.length == 4, "profile counts")

high44 = rows44.map { |row| high_multiplicities(row) }.sort
high45 = rows45.map { |row| high_multiplicities(row) }.sort
expected44 = [[4,4,7,14,15,15], [6,6,14,15,15],
              [11,14,14,14], [12,12,14,15]].sort
expected45 = [[4,4,9,13,15,15], [4,12,13,13,15],
              [5,5,6,14,15,15], [5,9,14,14,15]].sort
check(high44 == expected44, "D44 high profiles")
check(high45 == expected45, "D45 high profiles")

def obstruction(high)
  high.find { |k| k < 14 && k > high.length - 1 }
end

check(high44.all? { |high| obstruction(high) }, "D44 survivor")
check(high45.all? { |high| obstruction(high) }, "D45 survivor")

vector = (high44 + high45).map { |row| row.join(",") }.join(";") + "\n"
output = [
  "AUDIT_RANK15_M212_Q14_B42_D44_D45_HIGHPOINT_INCIDENCE_EXCLUSION: PASS",
  "enumeration=independent_ascending_parts",
  "D44_profiles=4 all_violate_k_le_H_minus_1",
  "D45_profiles=4 all_violate_k_le_H_minus_1",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=D44,D45",
  "nonclaim=D46_or_larger"
].join("\n") + "\n"

expected = File.join(__dir__,
  "audit_rank15_m212_q14_b42_d44_d45_highpoint_incidence_exclusion.expected.txt")
check(File.file?(expected), "missing expected output")
check(output == File.binread(expected), "expected-output drift")
print output

