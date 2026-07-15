#!/usr/bin/env ruby
# frozen_string_literal: true

require 'digest'

P = 2_130_706_433
B = 32_768
T = 981_105
A = 67_472
FULL_BLOCKS = 29
RESIDUAL = 30_833
TARGET = 274_854_110_496_187_592
FIXED_SCALAR_CAP = 25_307_496
RAY_SCALAR_CELLS = 64

ROOT = File.expand_path('..', __dir__)
PINS = {
  'work/DEPLOYED_C0_Q64_PERIODIC_FIXED_Q_REDUCTION.md' =>
    '8b2d84ffb344bbb0a78c904358645322f5159c20c152760ea7cd97354228fc69',
  'work/C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md' =>
    '99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b',
  'work/verify_c0_q64_three_invariant_hahn_payment.rb' =>
    'baf78eb9a8e297220bf69484f110bc108f88fb083d1e0693e05f570fa76722a5',
  'work/verify_c0_q64_three_invariant_hahn_payment.expected.txt' =>
    '28cd93bf4472d29537a267a7c84360f6f7c26eb9795aa4758e2a105383dcbba1'
}.freeze

def check(condition, message)
  raise message unless condition
end

PINS.each do |relative, digest|
  path = File.join(ROOT, relative)
  check(Digest::SHA256.file(path).hexdigest == digest, "pin drift: #{relative}")
end

check(P - 1 == 127 * (2**24), 'deployed prime factorization')
check(T == FULL_BLOCKS * B + RESIDUAL, 'support decomposition')
check(RESIDUAL < B && B < A, 'residual ownership inequalities')
check(A == 2 * B + 1_936, 'modulus scale')

# A constant term of a monic 29-subset locator on mu64 is nonzero and lies
# in mu64.  The proof uses only these two facts and monicity of A_R.
check(FULL_BLOCKS.odd?, 'quotient constant sign')
check((P - 1) % RAY_SCALAR_CELLS == 0, 'mu64 scalar subgroup')

ray_cap = RAY_SCALAR_CELLS * FIXED_SCALAR_CAP
margin = TARGET - ray_cap
check(ray_cap == 1_619_679_744, 'ray cap arithmetic')
check(margin == 274_854_108_876_507_848, 'target margin arithmetic')

puts 'C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER_PAYMENT: PASS'
puts "pins=#{PINS.length} B=#{B} t=#{T} a=#{A} full_blocks=#{FULL_BLOCKS} residual=#{RESIDUAL}"
puts "ownership_chain=residue_mod_Xa=>residue_mod_XB=>q0*A_R=c*q0p*A_Rp degrees_#{RESIDUAL}<#{B}=>R=Rp"
puts "fixed_scalar_cap=#{FIXED_SCALAR_CAP} ray_scalar_cells<=#{RAY_SCALAR_CELLS} ray_cap=#{ray_cap}"
puts "target=#{TARGET} margin=#{margin}"
puts 'scope=complete f29 stratum for g=X^67472; f0..28 and arbitrary g remain'
