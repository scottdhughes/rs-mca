#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"

def check(value, message)
  raise message unless value
end

def moment_profiles(double_count)
  higher_count = 211 - double_count
  rows = []
  counts = Array.new(14, 0)
  visit = nil
  visit = lambda do |part, count, total, square|
    if part.zero?
      rows << counts.dup if count == higher_count && total == 208 && square == 676
      return
    end
    maximum = [higher_count - count, (208 - total) / part,
               (676 - square) / (part * part)].min
    (0..maximum).each do |multiplicity|
      new_count = count + multiplicity
      new_total = total + multiplicity * part
      new_square = square + multiplicity * part * part
      remaining = higher_count - new_count
      next if new_total + remaining > 208 || new_square + remaining > 676
      next if part > 1 && (new_total + (part - 1) * remaining < 208 ||
                           new_square + (part - 1) * (part - 1) * remaining < 676)
      counts[part] = multiplicity
      visit.call(part - 1, new_count, new_total, new_square)
    end
    counts[part] = 0
  end
  visit.call(13, 0, 0, 0)
  rows
end

def multiplicity_profile(row)
  result = []
  (1..13).each do |x|
    row[x].times { result << x + 2 }
  end
  result
end

expected44 = [
  [3] * 163 + [11] + [14] * 3,
  [3] * 163 + [12] * 2 + [14, 15],
  [3] * 162 + [6] * 2 + [14] + [15] * 2,
  [3] * 161 + [4] * 2 + [7, 14] + [15] * 2
].map(&:sort).sort

expected45 = [
  [3] * 161 + [4, 12, 13, 13, 15],
  [3] * 161 + [5, 9, 14, 14, 15],
  [3] * 160 + [4, 4, 9, 13, 15, 15],
  [3] * 160 + [5, 5, 6, 14, 15, 15]
].map(&:sort).sort

rows44 = moment_profiles(44).map { |row| multiplicity_profile(row) }.sort
rows45 = moment_profiles(45).map { |row| multiplicity_profile(row) }.sort
check(rows44 == expected44, "D44 moment census drift")
check(rows45 == expected45, "D45 moment census drift")

def violating_high_point(profile)
  high = profile.select { |k| k >= 4 }
  high.find { |k| k < 14 && k > high.length - 1 }
end

w44 = rows44.map { |profile| violating_high_point(profile) }
w45 = rows45.map { |profile| violating_high_point(profile) }
check(w44.none?(&:nil?) && w45.none?(&:nil?), "incidence lemma left a row")

vector = [rows44.length, rows45.length, w44.sort, w45.sort].join(":") + "\n"
output = [
  "RANK15_M212_Q14_B42_D44_D45_HIGHPOINT_INCIDENCE_EXCLUSION: PASS",
  "moments=count211 incidence630 pairs861 line_support15",
  "D44_profiles=#{rows44.length} violating_k=#{w44.sort.join(',')}",
  "D45_profiles=#{rows45.length} violating_k=#{w45.sort.join(',')}",
  "lemma=every_high_k_lt_14_satisfies_k_le_H_minus_1",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=D44,D45",
  "next=D46 profiles=6 incidence_survivors=2"
].join("\n") + "\n"

expected = File.join(__dir__,
  "verify_rank15_m212_q14_b42_d44_d45_highpoint_incidence_exclusion.expected.txt")
check(File.file?(expected), "missing expected output")
check(output == File.binread(expected), "expected-output drift")
print output

