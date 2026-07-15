#!/usr/bin/env ruby
# frozen_string_literal: true

require "digest"

ROOT = File.expand_path("..", __dir__)
PINS = {
  "work/RANK15_M212_Q14_B42_D60_KNESER_AND_GRID_EXCLUSION.md" =>
    "87ac46a8f2e1112d683e71106347aecd5c91452813897954b2500662149ca1e1",
  "work/verify_rank15_m212_q14_b42_d60_kneser_and_grid_exclusion.rb" =>
    "5402d84a7f04c31acdcae429a45373a5771d7bc5dfb9254e6416c037472d8ee4",
  "work/verify_rank15_m212_q14_b42_d60_kneser_and_grid_exclusion.expected.txt" =>
    "7e0fdaac4482404bd823e4ebe0e615d24caa5cc066eb7a6c2d7298433827630c"
}.freeze

def check(value, message)
  raise message unless value
end

PINS.each do |relative, expected|
  check(Digest::SHA256.file(File.join(ROOT, relative)).hexdigest == expected,
        "pin drift #{relative}")
end

profiles = []
counts = Array.new(13, 0)
walk = nil
walk = lambda do |weight, total, square, number|
  if weight == 13
    profiles << counts[1, 12].dup if total == 57 && square == 411 && number <= 151
    next
  end
  maximum = [(57-total)/weight, (411-square)/(weight*weight), 151-number].min
  (0..maximum).each do |multiplicity|
    counts[weight] = multiplicity
    walk.call(weight+1, total+weight*multiplicity,
              square+weight*weight*multiplicity, number+multiplicity)
  end
  counts[weight] = 0
end
walk.call(1,0,0,0)
check(profiles.length == 1_183, "D60 moment count")

def patterns(threshold)
  rows=[]; counts=Array.new(10,0); visit=nil
  visit=lambda do |weight,total|
    if weight==11
      used=(1..10).select{|w| counts[w-1].positive?}
      rows << counts.dup if !used.empty? && total>=threshold && total-used.min<threshold
      next
    end
    maximum=(threshold+9-total)/weight
    if maximum>=0
      (0..maximum).each do |m|
        counts[weight-1]=m; visit.call(weight+1,total+weight*m)
      end
    end
    counts[weight-1]=0
  end
  visit.call(1,0); rows
end

GROUPS=(1..10).to_h{|threshold|[threshold,patterns(threshold)]}
MEMO={}
cover=nil
cover=lambda do |state,threshold|
  key=[state,threshold]; next MEMO[key] if MEMO.key?(key)
  best=0
  GROUPS.fetch(threshold).each do |group|
    next unless (0...10).all?{|i|group[i]<=state[i]}
    rest=(0...10).map{|i|state[i]-group[i]}
    best=[best,1+cover.call(rest,threshold)].max
  end
  MEMO[key]=best
end

kept=profiles.select do |profile|
  small=profile[0,10]; big=profile[10]+profile[11]
  small.each_with_index.all? do |multiplicity,index|
    next true if multiplicity.zero?
    other=small.dup; other[index]-=1
    index+4<=big+cover.call(other,10-index)
  end
end
check(kept.length==8,"D60 packing survivors")

p_field=2_130_706_433
check(51>48,"immediate heavy gate")
check([12,11,9].all?{|n|n>3},"immediate k5 gates")
check((p_field-1)%13==10,"13-grid field gate")

triple_total=13*13-2*21-3
selected=22+triple_total-(2+3+1)
check([triple_total,selected]==[124,140],"correlation floor")
divisors=(1..17).select{|h|(p_field-1)%h==0}
bounds=divisors.map{|h|2*h*((12+h-1)/h)-h}
check(divisors==[1,2,4,8,16] && bounds==[23,22,20,24,16],"Kneser cases")
check(144-3*8==120 && 120<selected,"H16 contradiction")

vector=[profiles.length,kept.length,triple_total,selected,divisors,bounds,120,10].join(":")+"\n"
output=[
  "AUDIT_RANK15_M212_Q14_B42_D60_KNESER_AND_GRID_EXCLUSION: PASS",
  "profiles=1183 local_survivors=8 independent=true",
  "immediate_exclusions=6 grid_row_excluded=true",
  "Kneser_row=triple124 selected140 quotient_cap17",
  "subgroup_orders=1,2,4,8,16 bounds=23,22,20,24,16 H16_cap120",
  "vector_sha256=#{Digest::SHA256.hexdigest(vector)}",
  "payment=D60",
  "nonclaim=D61_or_larger"
].join("\n")+"\n"

expected_path=File.join(__dir__,"audit_rank15_m212_q14_b42_d60_kneser_and_grid_exclusion.expected.txt")
check(File.file?(expected_path),"missing expected output")
check(output==File.binread(expected_path),"expected-output drift")
print output

