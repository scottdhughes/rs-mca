#!/usr/bin/env ruby
# frozen_string_literal: true

require 'digest'

N = 2_097_152
B = 32_768
T = 981_105
A = 67_472
FULL_BLOCKS = 28
R = 63_601
M = R - B
TARGET = 274_854_110_496_187_592
FIXED_SCALAR_CAP = 20_826_085
RAY_SCALAR_CELLS = 64
F29_CAP = 1_619_679_744

ROOT = File.expand_path('..', __dir__)
PINS = {
  'work/C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md' =>
    '99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b',
  'work/verify_c0_q64_three_invariant_hahn_payment.rb' =>
    'baf78eb9a8e297220bf69484f110bc108f88fb083d1e0693e05f570fa76722a5',
  'work/verify_c0_q64_three_invariant_hahn_payment.expected.txt' =>
    '28cd93bf4472d29537a267a7c84360f6f7c26eb9795aa4758e2a105383dcbba1',
  'work/C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER_PAYMENT.md' =>
    '704524424be7dc8b411a71011f8f8eb63ae88f9e7f4ebcfd100420e23c322ad5',
  'work/verify_c0_q64_f29_projective_residual_owner_payment.rb' =>
    '52c95bdcf544081281a2590e653320db7d59efd3ca193687160802bcb7dc5478',
  'work/verify_c0_q64_f29_projective_residual_owner_payment.expected.txt' =>
    '2d296032abd51cafafd7f46cb23bf4db0d1f8c99e7e015c20d26fe0a40c06543'
}.freeze

def check(condition, message)
  raise message unless condition
end

PINS.each do |relative, digest|
  path = File.join(ROOT, relative)
  check(Digest::SHA256.file(path).hexdigest == digest, "pin drift: #{relative}")
end

check(T == FULL_BLOCKS * B + R, 'support decomposition')
check(R == B + M && M == 30_833, 'two-block residual decomposition')
check(A == 2 * B + 1_936 && A > 2 * B, 'two complete residue blocks')

owner_caps = (0..M).map { |base| (N - base) / (R - base) }
owner_cap = owner_caps.max
maximizers = (0..M).select { |base| owner_caps[base] == owner_cap }
check(owner_cap == 63, 'residual pencil owner cap')
check(maximizers.first == 30_802 && maximizers.last == M,
      'owner-cap maximizing interval drift')

f28_cap = owner_cap * RAY_SCALAR_CELLS * FIXED_SCALAR_CAP
joint_cap = f28_cap + F29_CAP
margin = TARGET - joint_cap
check(f28_cap == 83_970_774_720, 'f28 cap arithmetic')
check(joint_cap == 85_590_454_464, 'f28/f29 joint arithmetic')
check(margin == 274_854_024_905_733_128, 'joint margin arithmetic')

puts 'C0_Q64_F28_RESIDUAL_PENCIL_PAYMENT: PASS'
puts "pins=#{PINS.length} B=#{B} t=#{T} a=#{A} f=#{FULL_BLOCKS} residual=#{R} second_block_degree=#{M}"
puts "pencil=P+theta*D D=X^B*U distinct_family_forces_degU<=#{M}"
puts "base_roots<=#{M} owner_cap=#{owner_cap} maximizing_base_interval=#{maximizers.first}..#{maximizers.last}"
puts "fixed_scalar_cap=#{FIXED_SCALAR_CAP} scalar_cells<=#{RAY_SCALAR_CELLS} f28_cap=#{f28_cap}"
puts "f29_cap=#{F29_CAP} joint_f28_f29_cap=#{joint_cap} target=#{TARGET} margin=#{margin}"
puts 'scope=complete f28 and joint f28/f29 strata for g=X^67472; f0..27 and arbitrary g remain'
