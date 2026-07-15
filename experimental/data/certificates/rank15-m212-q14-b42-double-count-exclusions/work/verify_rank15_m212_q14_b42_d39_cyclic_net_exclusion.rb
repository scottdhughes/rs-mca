#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"

P_FIELD = 2_130_706_433
Q = 14
B = 42
POINTS = Q * Q + Q + 1

def check(condition, message)
  raise message unless condition
end

check(POINTS == 211, "Chern count")
check(B * (Q + 1) == 630, "incidence count")
check(B * (B - 1) / 2 == 861, "pair count")

# Enumerate the bounded moment partition after fixing D=n_2=39.
solutions = []
parts = 13.downto(1).to_a # x=k-2
search = nil
search = lambda do |index, count, total, square, row|
  if index == parts.length
    solutions << row.dup if count == 172 && total == 208 && square == 676
    next
  end
  part = parts[index]
  maximum = [172 - count, (208 - total) / part,
             (676 - square) / (part * part)].min
  (0..maximum).each do |multiplicity|
    new_count = count + multiplicity
    new_total = total + multiplicity * part
    new_square = square + multiplicity * part * part
    remaining = 172 - new_count
    next if new_total + remaining > 208 || new_square + remaining > 676
    if index + 1 < parts.length
      next_part = parts[index + 1]
      next if new_total + next_part * remaining < 208 ||
              new_square + next_part * next_part * remaining < 676
    end
    row[part] = multiplicity
    search.call(index + 1, new_count, new_total, new_square, row)
  end
  row.delete(part)
end
search.call(0, 0, 0, 0, {})

check(solutions.length == 1, "D39 moment partition not unique")
partition = solutions.first
check(partition[13] == 3 && partition[1] == 169,
      "wrong D39 multiplicities")
check(partition.reject { |part, _count| [1, 13].include?(part) }.values.all?(&:zero?),
      "unexpected intermediate multiplicity")

# Per-line type equations.
line_types = []
(0..15).each do |h|
  (0..15).each do |t|
    d = 15 - t - h
    line_types << [d, t, h] if d >= 0 && d + 2 * t + 14 * h == 41
  end
end
check(line_types.sort == [[1, 13, 1], [13, 0, 2]], "line types")
centers = 3 * 15 - B
check(centers == 3, "center count")
check(B - centers == 39, "leaf count")

# The isolated K2 residue determinant is 14^2-2*14=168.
k2_determinant = Q * Q - 2 * Q
check(k2_determinant == 168, "K2 determinant")
check((k2_determinant % P_FIELD).positive?, "K2 residue vanished")

check((P_FIELD - 1) % 13 == 10, "deployed modulus residue")
check((P_FIELD - 1) % 13 != 0, "unexpected 13th roots")

vector = [POINTS, 630, 861, solutions.length, partition[13], partition[1],
          centers, 39, k2_determinant, (P_FIELD - 1) % 13].join(":") + "\n"
output = [
  "RANK15_M212_Q14_B42_D39_CYCLIC_NET_EXCLUSION: PASS",
  "field=#{P_FIELD} q=#{Q} B=#{B} points=#{POINTS}",
  "moments=count211 incidence630 pairs861 D39_partition=n2:39,n3:169,n15:3",
  "line_types=3_centers_(13,0,2);39_leaves_(1,13,1)",
  "double_graph=three_K1,13_stars K2_obstruction=#{k2_determinant}",
  "residual_structure=F_p_rational_(3,13)_net",
  "field_gate=(p-1)_mod_13=#{(P_FIELD - 1) % 13}",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=q14_B42_D39_only next_double_count=44",
  "nonclaim=D44_or_larger_not_excluded"
].join("\n") + "\n"

expected_path = File.join(__dir__,
  "verify_rank15_m212_q14_b42_d39_cyclic_net_exclusion.expected.txt")
check(File.file?(expected_path), "missing expected output")
check(output == File.binread(expected_path), "expected output mismatch")
print output

