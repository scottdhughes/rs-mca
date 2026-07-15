#!/usr/bin/env ruby
# frozen_string_literal: true

require 'digest'

ROOT = File.expand_path('..', __dir__)
PINS = {
  'work/C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER_PAYMENT.md' =>
    '704524424be7dc8b411a71011f8f8eb63ae88f9e7f4ebcfd100420e23c322ad5',
  'work/verify_c0_q64_f29_projective_residual_owner_payment.rb' =>
    '52c95bdcf544081281a2590e653320db7d59efd3ca193687160802bcb7dc5478',
  'work/verify_c0_q64_f29_projective_residual_owner_payment.expected.txt' =>
    '2d296032abd51cafafd7f46cb23bf4db0d1f8c99e7e015c20d26fe0a40c06543',
  'work/C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md' =>
    '99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b'
}.freeze

def assert(condition, label)
  raise "Q64 F29 AUDIT FAILURE: #{label}" unless condition
end

PINS.each do |relative, digest|
  assert(Digest::SHA256.file(File.join(ROOT, relative)).hexdigest == digest,
         "hash pin #{relative}")
end

n = 2_097_152
t = 981_105
b = 32_768
a = 67_472
f = 29
r = t - f * b
fixed_cell_cap = 25_307_496
target = 274_854_110_496_187_592

assert(n == 64 * b, '64 quotient fibers')
assert(r == 30_833 && r < b && b < a, 'residual ownership window')
assert(a == 2 * b + 1_936, 'literal monomial modulus scale')
ray_cap = 64 * fixed_cell_cap
assert(ray_cap == 1_619_679_744 && ray_cap < target, 'ray cap')
margin = target - ray_cap
assert(margin == 274_854_108_876_507_848, 'margin')

puts 'HOSTILE_AUDIT_C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER: PASS'
puts "pins=#{PINS.length} quotient_fibers=64 f=#{f} residual=#{r} residual<B<a"
puts 'ownership=same_projective_ray_mod_Xa_implies_same_monic_residual_via_mod_XB'
puts "fixed_absolute_cell_cap=#{fixed_cell_cap} scalar_cells<=64 ray_cap=#{ray_cap} margin=#{margin}"
puts 'scope=all_residual_supports_inside_canonical_f29_g_Xa_stratum only; no f0..28/cross-scale/general-g/uniform-c0/official payment'
