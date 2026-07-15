#!/usr/bin/env ruby
# frozen_string_literal: true

require 'digest'

ROOT = File.expand_path('..', __dir__)
PINS = {
  'work/C0_Q64_F28_RESIDUAL_PENCIL_PAYMENT.md' =>
    '9c0142793a738513f8a83801ff2536cd2a463b8f377a34be716ca5744b1f4709',
  'work/verify_c0_q64_f28_residual_pencil_payment.rb' =>
    'c080aa36fe5af048eeb087975a6b88d42cb15b04ed056c39901b3bdaed148e51',
  'work/verify_c0_q64_f28_residual_pencil_payment.expected.txt' =>
    'aea77f11333714650f33e253fd0f0f7f5c63335dcb34bec7f03c4709d819b7c3',
  'work/C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md' =>
    '99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b',
  'work/C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER_PAYMENT.md' =>
    '704524424be7dc8b411a71011f8f8eb63ae88f9e7f4ebcfd100420e23c322ad5'
}.freeze

def assert(condition, label)
  raise "Q64 F28 AUDIT FAILURE: #{label}" unless condition
end

PINS.each do |relative, digest|
  assert(Digest::SHA256.file(File.join(ROOT, relative)).hexdigest == digest,
         "hash pin #{relative}")
end

n = 2_097_152
b = 32_768
t = 981_105
a = 67_472
f = 28
r = t - f * b
m = r - b
target = 274_854_110_496_187_592
fixed_cell_cap = 20_826_085
f29_cap = 1_619_679_744

assert(r == 63_601 && m == 30_833, 'two-block residual degrees')
assert(a == 2 * b + 1_936, 'two complete coefficient blocks visible')

# Directly check the scalar algebra behind the two-block comparison for many
# deterministic nonzero choices.  U and V coefficients are tracked as an
# ordered pair.  This is a replay guard for signs and scalar normalization,
# not a substitute for the printed formal derivation.
(1..20).each do |seed|
  qi0 = seed + 1
  q00 = seed + 21
  c = seed + 41
  lambda_i = Rational(seed + 3, seed + 2)
  lambda_0 = Rational(seed + 5, seed + 4)
  s = Rational(c * q00, qi0)
  qi1 = qi0 * lambda_i
  q01 = q00 * lambda_0
  # A_i0=sU; A_i1=sV+s(lambda0-lambdai)U.
  left_v = qi0 * s
  left_u = qi0 * s * (lambda_0 - lambda_i) + qi1 * s
  right_v = c * q00
  right_u = c * q01
  assert(left_v == right_v && left_u == right_u,
         "two-block algebra seed #{seed}")
end

# Recompute the exact base-root owner bound for every allowed c, not just at
# the endpoint.  A nonbase deployed point determines at most one parameter.
owner_by_base = (0..m).map { |common| (n - common) / (r - common) }
owner_cap = owner_by_base.max
maximizers = (0..m).select { |common| owner_by_base[common] == owner_cap }
assert(owner_cap == 63, 'residual pencil owner cap')
assert(maximizers.first == 30_802 && maximizers.last == 30_833,
       'owner-cap plateau')

f28_cap = owner_cap * 64 * fixed_cell_cap
joint_cap = f28_cap + f29_cap
assert(f28_cap == 83_970_774_720, 'complete f28 cap')
assert(joint_cap == 85_590_454_464, 'canonical f28/f29 sum')
assert(target - joint_cap == 274_854_024_905_733_128, 'joint margin')

puts 'HOSTILE_AUDIT_C0_Q64_F28_RESIDUAL_PENCIL: PASS'
puts "pins=#{PINS.length} f=#{f} residual=#{r}=B+#{m} modulus_a=2B+1936"
puts 'two_block_normal_form=A_i=s_i(P+(lambda0-lambdai)D), P=U+X^B*V, D=X^B*U'
puts "distinct_family_forces_degU<=#{m} base_roots<=#{m} owner_cap=#{owner_cap} plateau=#{maximizers.first}..#{maximizers.last}"
puts "fixed_cell_cap=#{fixed_cell_cap} scalar_cells<=64 residual_owners<=#{owner_cap} f28_cap=#{f28_cap}"
puts "canonical_f29_cap=#{f29_cap} disjoint_joint_cap=#{joint_cap} margin=#{target - joint_cap}"
puts 'scope=canonical_q64_f28_and_disjoint_f29_g_Xa only; no f0..27/cross-scale/general-g/uniform-c0/official payment'
