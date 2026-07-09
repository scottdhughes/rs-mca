// Lean compiler output
// Module: RouteDResidual.ClosureBoard
// Imports: public import Init public meta import Init
#include <lean/lean.h>
#if defined(__clang__)
#pragma clang diagnostic ignored "-Wunused-parameter"
#pragma clang diagnostic ignored "-Wunused-label"
#elif defined(__GNUC__) && !defined(__CLANG__)
#pragma GCC diagnostic ignored "-Wunused-parameter"
#pragma GCC diagnostic ignored "-Wunused-label"
#pragma GCC diagnostic ignored "-Wunused-but-set-variable"
#endif
#ifdef __cplusplus
extern "C" {
#endif
lean_object* lean_nat_to_int(lean_object*);
lean_object* l_String_quote(lean_object*);
lean_object* l_Repr_addAppParen(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
lean_object* lean_string_length(lean_object*);
uint8_t lean_nat_dec_eq(lean_object*, lean_object*);
uint8_t lean_nat_dec_le(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_toCtorIdx(uint8_t);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_toCtorIdx___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorElim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorElim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorElim(lean_object*, lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorElim___boxed(lean_object*, lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_closed_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_closed_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_closed_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_closed_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_conditional_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_conditional_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_conditional_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_conditional_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_pending_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_pending_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_pending_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_pending_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_refuted_elim___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_refuted_elim___redArg___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_refuted_elim(lean_object*, uint8_t, lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_refuted_elim___boxed(lean_object*, lean_object*, lean_object*, lean_object*);
LEAN_EXPORT uint8_t lp_route__d__residual_RouteDResidual_ProofStatus_ofNat(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ofNat___boxed(lean_object*);
LEAN_EXPORT uint8_t lp_route__d__residual_RouteDResidual_instDecidableEqProofStatus(uint8_t, uint8_t);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instDecidableEqProofStatus___boxed(lean_object*, lean_object*);
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 34, .m_capacity = 34, .m_length = 33, .m_data = "RouteDResidual.ProofStatus.closed"};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__0 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__0_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__0_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__1 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__1_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 39, .m_capacity = 39, .m_length = 38, .m_data = "RouteDResidual.ProofStatus.conditional"};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__2 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__2_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__2_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__3 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__3_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 35, .m_capacity = 35, .m_length = 34, .m_data = "RouteDResidual.ProofStatus.pending"};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__4 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__4_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__4_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__5 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__5_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 35, .m_capacity = 35, .m_length = 34, .m_data = "RouteDResidual.ProofStatus.refuted"};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__6 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__6_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__6_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__7 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__7_value;
static lean_once_cell_t lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8;
static lean_once_cell_t lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9;
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr(uint8_t, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_route__d__residual_RouteDResidual_instReprProofStatus___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus___closed__0 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus___closed__0_value;
LEAN_EXPORT const lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprProofStatus___closed__0_value;
LEAN_EXPORT uint8_t lp_route__d__residual_RouteDResidual_ProofStatus_isSettled(uint8_t);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_isSettled___boxed(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_p;
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_nDomain;
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_A;
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_e;
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_nPrime;
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_H2;
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_BstarSq;
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_BstarFloor;
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "{ "};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__0 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__0_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = "id"};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__1 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__1_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__1_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__2 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__2_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)(((size_t)(0) << 1) | 1)),((lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__2_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__3 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__3_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 5, .m_capacity = 5, .m_length = 4, .m_data = " := "};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__4 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__4_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__4_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__5 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__5_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 5}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__3_value),((lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__5_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__6 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__6_value;
static lean_once_cell_t lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__7_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__7;
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 2, .m_capacity = 2, .m_length = 1, .m_data = ","};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__8 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__8_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__8_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__9 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__9_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "packet"};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__10 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__10_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__10_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__11 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__11_value;
static lean_once_cell_t lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__12_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__12;
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 7, .m_capacity = 7, .m_length = 6, .m_data = "status"};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__13 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__13_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__13_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__14 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__14_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 3, .m_capacity = 3, .m_length = 2, .m_data = " }"};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__15 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__15_value;
static lean_once_cell_t lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__16_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__16;
static lean_once_cell_t lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__17_once = LEAN_ONCE_CELL_INITIALIZER;
static lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__17;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__0_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__18 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__18_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*1 + 0, .m_other = 1, .m_tag = 3}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__15_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__19 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__19_value;
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg(lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr(lean_object*, lean_object*);
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___boxed(lean_object*, lean_object*);
static const lean_closure_object lp_route__d__residual_RouteDResidual_instReprClosureNode___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_closure_object) + sizeof(void*)*0, .m_other = 0, .m_tag = 245}, .m_fun = (void*)lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___boxed, .m_arity = 2, .m_num_fixed = 0, .m_objs = {} };
static const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode___closed__0 = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode___closed__0_value;
LEAN_EXPORT const lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode = (const lean_object*)&lp_route__d__residual_RouteDResidual_instReprClosureNode___closed__0_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 9, .m_capacity = 9, .m_length = 8, .m_data = "C_unique"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__0 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__0_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "v53"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__1 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__1_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__0_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__1_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__2 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__2_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "terminal_star"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__3 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__3_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "v54"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__4 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__4_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__3_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__4_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__5 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__5_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "U2e"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__6 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__6_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "v51"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__7 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__7_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__6_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__7_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__8 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__8_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "e2_T_le_H2"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__9 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__9_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "v48/v50"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__10 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__10_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__9_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__10_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__11 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__11_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__12_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 26, .m_capacity = 26, .m_length = 25, .m_data = "terminal_high_injectivity"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__12 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__12_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__13_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "v57"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__13 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__13_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__14_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__12_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__13_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__14 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__14_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__15_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 16, .m_capacity = 16, .m_length = 15, .m_data = "plancherel_coll"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__15 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__15_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__16_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "v58"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__16 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__16_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__17_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__15_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__16_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__17 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__17_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__18_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 13, .m_capacity = 13, .m_length = 12, .m_data = "G_plancherel"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__18 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__18_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__19_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "v59"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__19 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__19_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__20_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__18_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__19_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__20 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__20_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__21_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 14, .m_capacity = 14, .m_length = 13, .m_data = "soft_B_budget"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__21 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__21_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__22_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "v64"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__22 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__22_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__23_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__21_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__22_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__23 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__23_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__24_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 26, .m_capacity = 26, .m_length = 25, .m_data = "deployed_Bstar_arithmetic"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__24 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__24_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__25_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__24_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__22_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__25 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__25_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__26_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 10, .m_capacity = 10, .m_length = 9, .m_data = "energy_G4"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__26 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__26_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__27_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "v65"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__27 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__27_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__28_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__26_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__27_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__28 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__28_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__29_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "subgroup_G"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__29 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__29_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__30_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__29_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__27_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__30 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__30_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__31_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 16, .m_capacity = 16, .m_length = 15, .m_data = "incomplete_GP_G"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__31 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__31_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__32_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "v66"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__32 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__32_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__33_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__31_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__32_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__33 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__33_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__34_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 17, .m_capacity = 17, .m_length = 16, .m_data = "e3_lab_structure"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__34 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__34_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_closedNodes___closed__35_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "v60-v63"};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__35 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__35_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__36_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__34_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__35_value),LEAN_SCALAR_PTR_LITERAL(0, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__36 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__36_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__37_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__36_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__37 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__37_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__38_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__33_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__37_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__38 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__38_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__39_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__30_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__38_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__39 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__39_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__40_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__28_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__39_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__40 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__40_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__41_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__25_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__40_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__41 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__41_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__42_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__23_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__41_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__42 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__42_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__43_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__20_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__42_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__43 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__43_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__44_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__17_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__43_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__44 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__44_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__45_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__14_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__44_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__45 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__45_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__46_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__11_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__45_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__46 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__46_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__47_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__8_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__46_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__47 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__47_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__48_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__5_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__47_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__48 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__48_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_closedNodes___closed__49_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__2_value),((lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__48_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_closedNodes___closed__49 = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__49_value;
LEAN_EXPORT const lean_object* lp_route__d__residual_RouteDResidual_closedNodes = (const lean_object*)&lp_route__d__residual_RouteDResidual_closedNodes___closed__49_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_openNodes___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = "SoftB_Deployed"};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__0 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__0_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_openNodes___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "v64-v67"};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__1 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__1_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_openNodes___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__0_value),((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__1_value),LEAN_SCALAR_PTR_LITERAL(2, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__2 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__2_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_openNodes___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 15, .m_capacity = 15, .m_length = 14, .m_data = "R2_pair_budget"};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__3 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__3_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_openNodes___closed__4_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "v45-v46"};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__4 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__4_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_openNodes___closed__5_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__3_value),((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__4_value),LEAN_SCALAR_PTR_LITERAL(2, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__5 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__5_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_openNodes___closed__6_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 11, .m_capacity = 11, .m_length = 10, .m_data = "A_SP_le_tp"};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__6 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__6_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_openNodes___closed__7_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 8, .m_capacity = 8, .m_length = 7, .m_data = "program"};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__7 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__7_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_openNodes___closed__8_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__6_value),((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__7_value),LEAN_SCALAR_PTR_LITERAL(2, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__8 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__8_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_openNodes___closed__9_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__8_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__9 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__9_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_openNodes___closed__10_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__5_value),((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__9_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__10 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__10_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_openNodes___closed__11_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__2_value),((lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__10_value)}};
static const lean_object* lp_route__d__residual_RouteDResidual_openNodes___closed__11 = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__11_value;
LEAN_EXPORT const lean_object* lp_route__d__residual_RouteDResidual_openNodes = (const lean_object*)&lp_route__d__residual_RouteDResidual_openNodes___closed__11_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_conditionalNodes___closed__0_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 20, .m_capacity = 20, .m_length = 19, .m_data = "conditional_T_le_H2"};
static const lean_object* lp_route__d__residual_RouteDResidual_conditionalNodes___closed__0 = (const lean_object*)&lp_route__d__residual_RouteDResidual_conditionalNodes___closed__0_value;
static const lean_string_object lp_route__d__residual_RouteDResidual_conditionalNodes___closed__1_value = {.m_header = {.m_rc = 0, .m_cs_sz = 0, .m_other = 0, .m_tag = 249}, .m_size = 4, .m_capacity = 4, .m_length = 3, .m_data = "v67"};
static const lean_object* lp_route__d__residual_RouteDResidual_conditionalNodes___closed__1 = (const lean_object*)&lp_route__d__residual_RouteDResidual_conditionalNodes___closed__1_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_conditionalNodes___closed__2_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 8, .m_other = 2, .m_tag = 0}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_conditionalNodes___closed__0_value),((lean_object*)&lp_route__d__residual_RouteDResidual_conditionalNodes___closed__1_value),LEAN_SCALAR_PTR_LITERAL(1, 0, 0, 0, 0, 0, 0, 0)}};
static const lean_object* lp_route__d__residual_RouteDResidual_conditionalNodes___closed__2 = (const lean_object*)&lp_route__d__residual_RouteDResidual_conditionalNodes___closed__2_value;
static const lean_ctor_object lp_route__d__residual_RouteDResidual_conditionalNodes___closed__3_value = {.m_header = {.m_rc = 0, .m_cs_sz = sizeof(lean_ctor_object) + sizeof(void*)*2 + 0, .m_other = 2, .m_tag = 1}, .m_objs = {((lean_object*)&lp_route__d__residual_RouteDResidual_conditionalNodes___closed__2_value),((lean_object*)(((size_t)(0) << 1) | 1))}};
static const lean_object* lp_route__d__residual_RouteDResidual_conditionalNodes___closed__3 = (const lean_object*)&lp_route__d__residual_RouteDResidual_conditionalNodes___closed__3_value;
LEAN_EXPORT const lean_object* lp_route__d__residual_RouteDResidual_conditionalNodes = (const lean_object*)&lp_route__d__residual_RouteDResidual_conditionalNodes___closed__3_value;
LEAN_EXPORT uint8_t lp_route__d__residual_RouteDResidual_fullResidualClosed;
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorIdx(uint8_t v_x_1_){
_start:
{
switch(v_x_1_)
{
case 0:
{
lean_object* v___x_2_; 
v___x_2_ = lean_unsigned_to_nat(0u);
return v___x_2_;
}
case 1:
{
lean_object* v___x_3_; 
v___x_3_ = lean_unsigned_to_nat(1u);
return v___x_3_;
}
case 2:
{
lean_object* v___x_4_; 
v___x_4_ = lean_unsigned_to_nat(2u);
return v___x_4_;
}
default: 
{
lean_object* v___x_5_; 
v___x_5_ = lean_unsigned_to_nat(3u);
return v___x_5_;
}
}
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorIdx___boxed(lean_object* v_x_6_){
_start:
{
uint8_t v_x_boxed_7_; lean_object* v_res_8_; 
v_x_boxed_7_ = lean_unbox(v_x_6_);
v_res_8_ = lp_route__d__residual_RouteDResidual_ProofStatus_ctorIdx(v_x_boxed_7_);
return v_res_8_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_toCtorIdx(uint8_t v_x_9_){
_start:
{
lean_object* v___x_10_; 
v___x_10_ = lp_route__d__residual_RouteDResidual_ProofStatus_ctorIdx(v_x_9_);
return v___x_10_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_toCtorIdx___boxed(lean_object* v_x_11_){
_start:
{
uint8_t v_x_4__boxed_12_; lean_object* v_res_13_; 
v_x_4__boxed_12_ = lean_unbox(v_x_11_);
v_res_13_ = lp_route__d__residual_RouteDResidual_ProofStatus_toCtorIdx(v_x_4__boxed_12_);
return v_res_13_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorElim___redArg(lean_object* v_k_14_){
_start:
{
lean_inc(v_k_14_);
return v_k_14_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorElim___redArg___boxed(lean_object* v_k_15_){
_start:
{
lean_object* v_res_16_; 
v_res_16_ = lp_route__d__residual_RouteDResidual_ProofStatus_ctorElim___redArg(v_k_15_);
lean_dec(v_k_15_);
return v_res_16_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorElim(lean_object* v_motive_17_, lean_object* v_ctorIdx_18_, uint8_t v_t_19_, lean_object* v_h_20_, lean_object* v_k_21_){
_start:
{
lean_inc(v_k_21_);
return v_k_21_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ctorElim___boxed(lean_object* v_motive_22_, lean_object* v_ctorIdx_23_, lean_object* v_t_24_, lean_object* v_h_25_, lean_object* v_k_26_){
_start:
{
uint8_t v_t_boxed_27_; lean_object* v_res_28_; 
v_t_boxed_27_ = lean_unbox(v_t_24_);
v_res_28_ = lp_route__d__residual_RouteDResidual_ProofStatus_ctorElim(v_motive_22_, v_ctorIdx_23_, v_t_boxed_27_, v_h_25_, v_k_26_);
lean_dec(v_k_26_);
lean_dec(v_ctorIdx_23_);
return v_res_28_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_closed_elim___redArg(lean_object* v_closed_29_){
_start:
{
lean_inc(v_closed_29_);
return v_closed_29_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_closed_elim___redArg___boxed(lean_object* v_closed_30_){
_start:
{
lean_object* v_res_31_; 
v_res_31_ = lp_route__d__residual_RouteDResidual_ProofStatus_closed_elim___redArg(v_closed_30_);
lean_dec(v_closed_30_);
return v_res_31_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_closed_elim(lean_object* v_motive_32_, uint8_t v_t_33_, lean_object* v_h_34_, lean_object* v_closed_35_){
_start:
{
lean_inc(v_closed_35_);
return v_closed_35_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_closed_elim___boxed(lean_object* v_motive_36_, lean_object* v_t_37_, lean_object* v_h_38_, lean_object* v_closed_39_){
_start:
{
uint8_t v_t_boxed_40_; lean_object* v_res_41_; 
v_t_boxed_40_ = lean_unbox(v_t_37_);
v_res_41_ = lp_route__d__residual_RouteDResidual_ProofStatus_closed_elim(v_motive_36_, v_t_boxed_40_, v_h_38_, v_closed_39_);
lean_dec(v_closed_39_);
return v_res_41_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_conditional_elim___redArg(lean_object* v_conditional_42_){
_start:
{
lean_inc(v_conditional_42_);
return v_conditional_42_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_conditional_elim___redArg___boxed(lean_object* v_conditional_43_){
_start:
{
lean_object* v_res_44_; 
v_res_44_ = lp_route__d__residual_RouteDResidual_ProofStatus_conditional_elim___redArg(v_conditional_43_);
lean_dec(v_conditional_43_);
return v_res_44_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_conditional_elim(lean_object* v_motive_45_, uint8_t v_t_46_, lean_object* v_h_47_, lean_object* v_conditional_48_){
_start:
{
lean_inc(v_conditional_48_);
return v_conditional_48_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_conditional_elim___boxed(lean_object* v_motive_49_, lean_object* v_t_50_, lean_object* v_h_51_, lean_object* v_conditional_52_){
_start:
{
uint8_t v_t_boxed_53_; lean_object* v_res_54_; 
v_t_boxed_53_ = lean_unbox(v_t_50_);
v_res_54_ = lp_route__d__residual_RouteDResidual_ProofStatus_conditional_elim(v_motive_49_, v_t_boxed_53_, v_h_51_, v_conditional_52_);
lean_dec(v_conditional_52_);
return v_res_54_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_pending_elim___redArg(lean_object* v_pending_55_){
_start:
{
lean_inc(v_pending_55_);
return v_pending_55_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_pending_elim___redArg___boxed(lean_object* v_pending_56_){
_start:
{
lean_object* v_res_57_; 
v_res_57_ = lp_route__d__residual_RouteDResidual_ProofStatus_pending_elim___redArg(v_pending_56_);
lean_dec(v_pending_56_);
return v_res_57_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_pending_elim(lean_object* v_motive_58_, uint8_t v_t_59_, lean_object* v_h_60_, lean_object* v_pending_61_){
_start:
{
lean_inc(v_pending_61_);
return v_pending_61_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_pending_elim___boxed(lean_object* v_motive_62_, lean_object* v_t_63_, lean_object* v_h_64_, lean_object* v_pending_65_){
_start:
{
uint8_t v_t_boxed_66_; lean_object* v_res_67_; 
v_t_boxed_66_ = lean_unbox(v_t_63_);
v_res_67_ = lp_route__d__residual_RouteDResidual_ProofStatus_pending_elim(v_motive_62_, v_t_boxed_66_, v_h_64_, v_pending_65_);
lean_dec(v_pending_65_);
return v_res_67_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_refuted_elim___redArg(lean_object* v_refuted_68_){
_start:
{
lean_inc(v_refuted_68_);
return v_refuted_68_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_refuted_elim___redArg___boxed(lean_object* v_refuted_69_){
_start:
{
lean_object* v_res_70_; 
v_res_70_ = lp_route__d__residual_RouteDResidual_ProofStatus_refuted_elim___redArg(v_refuted_69_);
lean_dec(v_refuted_69_);
return v_res_70_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_refuted_elim(lean_object* v_motive_71_, uint8_t v_t_72_, lean_object* v_h_73_, lean_object* v_refuted_74_){
_start:
{
lean_inc(v_refuted_74_);
return v_refuted_74_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_refuted_elim___boxed(lean_object* v_motive_75_, lean_object* v_t_76_, lean_object* v_h_77_, lean_object* v_refuted_78_){
_start:
{
uint8_t v_t_boxed_79_; lean_object* v_res_80_; 
v_t_boxed_79_ = lean_unbox(v_t_76_);
v_res_80_ = lp_route__d__residual_RouteDResidual_ProofStatus_refuted_elim(v_motive_75_, v_t_boxed_79_, v_h_77_, v_refuted_78_);
lean_dec(v_refuted_78_);
return v_res_80_;
}
}
LEAN_EXPORT uint8_t lp_route__d__residual_RouteDResidual_ProofStatus_ofNat(lean_object* v_n_81_){
_start:
{
lean_object* v___x_82_; uint8_t v___x_83_; 
v___x_82_ = lean_unsigned_to_nat(1u);
v___x_83_ = lean_nat_dec_le(v_n_81_, v___x_82_);
if (v___x_83_ == 0)
{
lean_object* v___x_84_; uint8_t v___x_85_; 
v___x_84_ = lean_unsigned_to_nat(2u);
v___x_85_ = lean_nat_dec_le(v_n_81_, v___x_84_);
if (v___x_85_ == 0)
{
uint8_t v___x_86_; 
v___x_86_ = 3;
return v___x_86_;
}
else
{
uint8_t v___x_87_; 
v___x_87_ = 2;
return v___x_87_;
}
}
else
{
lean_object* v___x_88_; uint8_t v___x_89_; 
v___x_88_ = lean_unsigned_to_nat(0u);
v___x_89_ = lean_nat_dec_le(v_n_81_, v___x_88_);
if (v___x_89_ == 0)
{
uint8_t v___x_90_; 
v___x_90_ = 1;
return v___x_90_;
}
else
{
uint8_t v___x_91_; 
v___x_91_ = 0;
return v___x_91_;
}
}
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_ofNat___boxed(lean_object* v_n_92_){
_start:
{
uint8_t v_res_93_; lean_object* v_r_94_; 
v_res_93_ = lp_route__d__residual_RouteDResidual_ProofStatus_ofNat(v_n_92_);
lean_dec(v_n_92_);
v_r_94_ = lean_box(v_res_93_);
return v_r_94_;
}
}
LEAN_EXPORT uint8_t lp_route__d__residual_RouteDResidual_instDecidableEqProofStatus(uint8_t v_x_95_, uint8_t v_y_96_){
_start:
{
lean_object* v___x_97_; lean_object* v___x_98_; uint8_t v___x_99_; 
v___x_97_ = lp_route__d__residual_RouteDResidual_ProofStatus_ctorIdx(v_x_95_);
v___x_98_ = lp_route__d__residual_RouteDResidual_ProofStatus_ctorIdx(v_y_96_);
v___x_99_ = lean_nat_dec_eq(v___x_97_, v___x_98_);
lean_dec(v___x_98_);
lean_dec(v___x_97_);
return v___x_99_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instDecidableEqProofStatus___boxed(lean_object* v_x_100_, lean_object* v_y_101_){
_start:
{
uint8_t v_x_13__boxed_102_; uint8_t v_y_14__boxed_103_; uint8_t v_res_104_; lean_object* v_r_105_; 
v_x_13__boxed_102_ = lean_unbox(v_x_100_);
v_y_14__boxed_103_ = lean_unbox(v_y_101_);
v_res_104_ = lp_route__d__residual_RouteDResidual_instDecidableEqProofStatus(v_x_13__boxed_102_, v_y_14__boxed_103_);
v_r_105_ = lean_box(v_res_104_);
return v_r_105_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8(void){
_start:
{
lean_object* v___x_118_; lean_object* v___x_119_; 
v___x_118_ = lean_unsigned_to_nat(2u);
v___x_119_ = lean_nat_to_int(v___x_118_);
return v___x_119_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9(void){
_start:
{
lean_object* v___x_120_; lean_object* v___x_121_; 
v___x_120_ = lean_unsigned_to_nat(1u);
v___x_121_ = lean_nat_to_int(v___x_120_);
return v___x_121_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr(uint8_t v_x_122_, lean_object* v_prec_123_){
_start:
{
lean_object* v___y_125_; lean_object* v___y_132_; lean_object* v___y_139_; lean_object* v___y_146_; 
switch(v_x_122_)
{
case 0:
{
lean_object* v___x_152_; uint8_t v___x_153_; 
v___x_152_ = lean_unsigned_to_nat(1024u);
v___x_153_ = lean_nat_dec_le(v___x_152_, v_prec_123_);
if (v___x_153_ == 0)
{
lean_object* v___x_154_; 
v___x_154_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8, &lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8_once, _init_lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8);
v___y_125_ = v___x_154_;
goto v___jp_124_;
}
else
{
lean_object* v___x_155_; 
v___x_155_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9, &lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9_once, _init_lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9);
v___y_125_ = v___x_155_;
goto v___jp_124_;
}
}
case 1:
{
lean_object* v___x_156_; uint8_t v___x_157_; 
v___x_156_ = lean_unsigned_to_nat(1024u);
v___x_157_ = lean_nat_dec_le(v___x_156_, v_prec_123_);
if (v___x_157_ == 0)
{
lean_object* v___x_158_; 
v___x_158_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8, &lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8_once, _init_lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8);
v___y_132_ = v___x_158_;
goto v___jp_131_;
}
else
{
lean_object* v___x_159_; 
v___x_159_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9, &lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9_once, _init_lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9);
v___y_132_ = v___x_159_;
goto v___jp_131_;
}
}
case 2:
{
lean_object* v___x_160_; uint8_t v___x_161_; 
v___x_160_ = lean_unsigned_to_nat(1024u);
v___x_161_ = lean_nat_dec_le(v___x_160_, v_prec_123_);
if (v___x_161_ == 0)
{
lean_object* v___x_162_; 
v___x_162_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8, &lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8_once, _init_lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8);
v___y_139_ = v___x_162_;
goto v___jp_138_;
}
else
{
lean_object* v___x_163_; 
v___x_163_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9, &lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9_once, _init_lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9);
v___y_139_ = v___x_163_;
goto v___jp_138_;
}
}
default: 
{
lean_object* v___x_164_; uint8_t v___x_165_; 
v___x_164_ = lean_unsigned_to_nat(1024u);
v___x_165_ = lean_nat_dec_le(v___x_164_, v_prec_123_);
if (v___x_165_ == 0)
{
lean_object* v___x_166_; 
v___x_166_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8, &lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8_once, _init_lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__8);
v___y_146_ = v___x_166_;
goto v___jp_145_;
}
else
{
lean_object* v___x_167_; 
v___x_167_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9, &lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9_once, _init_lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__9);
v___y_146_ = v___x_167_;
goto v___jp_145_;
}
}
}
v___jp_124_:
{
lean_object* v___x_126_; lean_object* v___x_127_; uint8_t v___x_128_; lean_object* v___x_129_; lean_object* v___x_130_; 
v___x_126_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__1));
lean_inc(v___y_125_);
v___x_127_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_127_, 0, v___y_125_);
lean_ctor_set(v___x_127_, 1, v___x_126_);
v___x_128_ = 0;
v___x_129_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_129_, 0, v___x_127_);
lean_ctor_set_uint8(v___x_129_, sizeof(void*)*1, v___x_128_);
v___x_130_ = l_Repr_addAppParen(v___x_129_, v_prec_123_);
return v___x_130_;
}
v___jp_131_:
{
lean_object* v___x_133_; lean_object* v___x_134_; uint8_t v___x_135_; lean_object* v___x_136_; lean_object* v___x_137_; 
v___x_133_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__3));
lean_inc(v___y_132_);
v___x_134_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_134_, 0, v___y_132_);
lean_ctor_set(v___x_134_, 1, v___x_133_);
v___x_135_ = 0;
v___x_136_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_136_, 0, v___x_134_);
lean_ctor_set_uint8(v___x_136_, sizeof(void*)*1, v___x_135_);
v___x_137_ = l_Repr_addAppParen(v___x_136_, v_prec_123_);
return v___x_137_;
}
v___jp_138_:
{
lean_object* v___x_140_; lean_object* v___x_141_; uint8_t v___x_142_; lean_object* v___x_143_; lean_object* v___x_144_; 
v___x_140_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__5));
lean_inc(v___y_139_);
v___x_141_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_141_, 0, v___y_139_);
lean_ctor_set(v___x_141_, 1, v___x_140_);
v___x_142_ = 0;
v___x_143_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_143_, 0, v___x_141_);
lean_ctor_set_uint8(v___x_143_, sizeof(void*)*1, v___x_142_);
v___x_144_ = l_Repr_addAppParen(v___x_143_, v_prec_123_);
return v___x_144_;
}
v___jp_145_:
{
lean_object* v___x_147_; lean_object* v___x_148_; uint8_t v___x_149_; lean_object* v___x_150_; lean_object* v___x_151_; 
v___x_147_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___closed__7));
lean_inc(v___y_146_);
v___x_148_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_148_, 0, v___y_146_);
lean_ctor_set(v___x_148_, 1, v___x_147_);
v___x_149_ = 0;
v___x_150_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_150_, 0, v___x_148_);
lean_ctor_set_uint8(v___x_150_, sizeof(void*)*1, v___x_149_);
v___x_151_ = l_Repr_addAppParen(v___x_150_, v_prec_123_);
return v___x_151_;
}
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instReprProofStatus_repr___boxed(lean_object* v_x_168_, lean_object* v_prec_169_){
_start:
{
uint8_t v_x_233__boxed_170_; lean_object* v_res_171_; 
v_x_233__boxed_170_ = lean_unbox(v_x_168_);
v_res_171_ = lp_route__d__residual_RouteDResidual_instReprProofStatus_repr(v_x_233__boxed_170_, v_prec_169_);
lean_dec(v_prec_169_);
return v_res_171_;
}
}
LEAN_EXPORT uint8_t lp_route__d__residual_RouteDResidual_ProofStatus_isSettled(uint8_t v_x_174_){
_start:
{
switch(v_x_174_)
{
case 0:
{
uint8_t v___x_175_; 
v___x_175_ = 1;
return v___x_175_;
}
case 3:
{
uint8_t v___x_176_; 
v___x_176_ = 1;
return v___x_176_;
}
default: 
{
uint8_t v___x_177_; 
v___x_177_ = 0;
return v___x_177_;
}
}
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_ProofStatus_isSettled___boxed(lean_object* v_x_178_){
_start:
{
uint8_t v_x_26__boxed_179_; uint8_t v_res_180_; lean_object* v_r_181_; 
v_x_26__boxed_179_ = lean_unbox(v_x_178_);
v_res_180_ = lp_route__d__residual_RouteDResidual_ProofStatus_isSettled(v_x_26__boxed_179_);
v_r_181_ = lean_box(v_res_180_);
return v_r_181_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_p(void){
_start:
{
lean_object* v___x_182_; 
v___x_182_ = lean_unsigned_to_nat(2130706433u);
return v___x_182_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_nDomain(void){
_start:
{
lean_object* v___x_183_; 
v___x_183_ = lean_unsigned_to_nat(2097152u);
return v___x_183_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_A(void){
_start:
{
lean_object* v___x_184_; 
v___x_184_ = lean_unsigned_to_nat(1116048u);
return v___x_184_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_e(void){
_start:
{
lean_object* v___x_185_; 
v___x_185_ = lean_unsigned_to_nat(67472u);
return v___x_185_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_nPrime(void){
_start:
{
lean_object* v___x_186_; 
v___x_186_ = lean_unsigned_to_nat(1183520u);
return v___x_186_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_H2(void){
_start:
{
lean_object* v___x_187_; 
v___x_187_ = lean_cstr_to_nat("77291948627");
return v___x_187_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_BstarSq(void){
_start:
{
lean_object* v___x_188_; 
v___x_188_ = lean_cstr_to_nat("154583897254");
return v___x_188_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_BstarFloor(void){
_start:
{
lean_object* v___x_189_; 
v___x_189_ = lean_unsigned_to_nat(393171u);
return v___x_189_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__7(void){
_start:
{
lean_object* v___x_203_; lean_object* v___x_204_; 
v___x_203_ = lean_unsigned_to_nat(6u);
v___x_204_ = lean_nat_to_int(v___x_203_);
return v___x_204_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__12(void){
_start:
{
lean_object* v___x_211_; lean_object* v___x_212_; 
v___x_211_ = lean_unsigned_to_nat(10u);
v___x_212_ = lean_nat_to_int(v___x_211_);
return v___x_212_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__16(void){
_start:
{
lean_object* v___x_217_; lean_object* v___x_218_; 
v___x_217_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__0));
v___x_218_ = lean_string_length(v___x_217_);
return v___x_218_;
}
}
static lean_object* _init_lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__17(void){
_start:
{
lean_object* v___x_219_; lean_object* v___x_220_; 
v___x_219_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__16, &lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__16_once, _init_lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__16);
v___x_220_ = lean_nat_to_int(v___x_219_);
return v___x_220_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg(lean_object* v_x_225_){
_start:
{
lean_object* v_id_226_; lean_object* v_packet_227_; uint8_t v_status_228_; lean_object* v___x_229_; lean_object* v___x_230_; lean_object* v___x_231_; lean_object* v___x_232_; lean_object* v___x_233_; lean_object* v___x_234_; uint8_t v___x_235_; lean_object* v___x_236_; lean_object* v___x_237_; lean_object* v___x_238_; lean_object* v___x_239_; lean_object* v___x_240_; lean_object* v___x_241_; lean_object* v___x_242_; lean_object* v___x_243_; lean_object* v___x_244_; lean_object* v___x_245_; lean_object* v___x_246_; lean_object* v___x_247_; lean_object* v___x_248_; lean_object* v___x_249_; lean_object* v___x_250_; lean_object* v___x_251_; lean_object* v___x_252_; lean_object* v___x_253_; lean_object* v___x_254_; lean_object* v___x_255_; lean_object* v___x_256_; lean_object* v___x_257_; lean_object* v___x_258_; lean_object* v___x_259_; lean_object* v___x_260_; lean_object* v___x_261_; lean_object* v___x_262_; lean_object* v___x_263_; lean_object* v___x_264_; lean_object* v___x_265_; lean_object* v___x_266_; lean_object* v___x_267_; 
v_id_226_ = lean_ctor_get(v_x_225_, 0);
lean_inc_ref(v_id_226_);
v_packet_227_ = lean_ctor_get(v_x_225_, 1);
lean_inc_ref(v_packet_227_);
v_status_228_ = lean_ctor_get_uint8(v_x_225_, sizeof(void*)*2);
lean_dec_ref(v_x_225_);
v___x_229_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__5));
v___x_230_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__6));
v___x_231_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__7, &lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__7_once, _init_lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__7);
v___x_232_ = l_String_quote(v_id_226_);
v___x_233_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_233_, 0, v___x_232_);
v___x_234_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_234_, 0, v___x_231_);
lean_ctor_set(v___x_234_, 1, v___x_233_);
v___x_235_ = 0;
v___x_236_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_236_, 0, v___x_234_);
lean_ctor_set_uint8(v___x_236_, sizeof(void*)*1, v___x_235_);
v___x_237_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_237_, 0, v___x_230_);
lean_ctor_set(v___x_237_, 1, v___x_236_);
v___x_238_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__9));
v___x_239_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_239_, 0, v___x_237_);
lean_ctor_set(v___x_239_, 1, v___x_238_);
v___x_240_ = lean_box(1);
v___x_241_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_241_, 0, v___x_239_);
lean_ctor_set(v___x_241_, 1, v___x_240_);
v___x_242_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__11));
v___x_243_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_243_, 0, v___x_241_);
lean_ctor_set(v___x_243_, 1, v___x_242_);
v___x_244_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_244_, 0, v___x_243_);
lean_ctor_set(v___x_244_, 1, v___x_229_);
v___x_245_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__12, &lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__12_once, _init_lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__12);
v___x_246_ = l_String_quote(v_packet_227_);
v___x_247_ = lean_alloc_ctor(3, 1, 0);
lean_ctor_set(v___x_247_, 0, v___x_246_);
v___x_248_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_248_, 0, v___x_245_);
lean_ctor_set(v___x_248_, 1, v___x_247_);
v___x_249_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_249_, 0, v___x_248_);
lean_ctor_set_uint8(v___x_249_, sizeof(void*)*1, v___x_235_);
v___x_250_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_250_, 0, v___x_244_);
lean_ctor_set(v___x_250_, 1, v___x_249_);
v___x_251_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_251_, 0, v___x_250_);
lean_ctor_set(v___x_251_, 1, v___x_238_);
v___x_252_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_252_, 0, v___x_251_);
lean_ctor_set(v___x_252_, 1, v___x_240_);
v___x_253_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__14));
v___x_254_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_254_, 0, v___x_252_);
lean_ctor_set(v___x_254_, 1, v___x_253_);
v___x_255_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_255_, 0, v___x_254_);
lean_ctor_set(v___x_255_, 1, v___x_229_);
v___x_256_ = lean_unsigned_to_nat(0u);
v___x_257_ = lp_route__d__residual_RouteDResidual_instReprProofStatus_repr(v_status_228_, v___x_256_);
v___x_258_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_258_, 0, v___x_245_);
lean_ctor_set(v___x_258_, 1, v___x_257_);
v___x_259_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_259_, 0, v___x_258_);
lean_ctor_set_uint8(v___x_259_, sizeof(void*)*1, v___x_235_);
v___x_260_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_260_, 0, v___x_255_);
lean_ctor_set(v___x_260_, 1, v___x_259_);
v___x_261_ = lean_obj_once(&lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__17, &lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__17_once, _init_lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__17);
v___x_262_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__18));
v___x_263_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_263_, 0, v___x_262_);
lean_ctor_set(v___x_263_, 1, v___x_260_);
v___x_264_ = ((lean_object*)(lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg___closed__19));
v___x_265_ = lean_alloc_ctor(5, 2, 0);
lean_ctor_set(v___x_265_, 0, v___x_263_);
lean_ctor_set(v___x_265_, 1, v___x_264_);
v___x_266_ = lean_alloc_ctor(4, 2, 0);
lean_ctor_set(v___x_266_, 0, v___x_261_);
lean_ctor_set(v___x_266_, 1, v___x_265_);
v___x_267_ = lean_alloc_ctor(6, 1, 1);
lean_ctor_set(v___x_267_, 0, v___x_266_);
lean_ctor_set_uint8(v___x_267_, sizeof(void*)*1, v___x_235_);
return v___x_267_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr(lean_object* v_x_268_, lean_object* v_prec_269_){
_start:
{
lean_object* v___x_270_; 
v___x_270_ = lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___redArg(v_x_268_);
return v___x_270_;
}
}
LEAN_EXPORT lean_object* lp_route__d__residual_RouteDResidual_instReprClosureNode_repr___boxed(lean_object* v_x_271_, lean_object* v_prec_272_){
_start:
{
lean_object* v_res_273_; 
v_res_273_ = lp_route__d__residual_RouteDResidual_instReprClosureNode_repr(v_x_271_, v_prec_272_);
lean_dec(v_prec_272_);
return v_res_273_;
}
}
static uint8_t _init_lp_route__d__residual_RouteDResidual_fullResidualClosed(void){
_start:
{
uint8_t v___x_430_; 
v___x_430_ = 0;
return v___x_430_;
}
}
lean_object* initialize_Init(uint8_t builtin);
lean_object* initialize_Init(uint8_t builtin);
static bool _G_initialized = false;
LEAN_EXPORT lean_object* initialize_route__d__residual_RouteDResidual_ClosureBoard(uint8_t builtin) {
lean_object * res;
if (_G_initialized) return lean_io_result_mk_ok(lean_box(0));
_G_initialized = true;
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
res = initialize_Init(builtin);
if (lean_io_result_is_error(res)) return res;
lean_dec_ref(res);
lp_route__d__residual_RouteDResidual_p = _init_lp_route__d__residual_RouteDResidual_p();
lean_mark_persistent(lp_route__d__residual_RouteDResidual_p);
lp_route__d__residual_RouteDResidual_nDomain = _init_lp_route__d__residual_RouteDResidual_nDomain();
lean_mark_persistent(lp_route__d__residual_RouteDResidual_nDomain);
lp_route__d__residual_RouteDResidual_A = _init_lp_route__d__residual_RouteDResidual_A();
lean_mark_persistent(lp_route__d__residual_RouteDResidual_A);
lp_route__d__residual_RouteDResidual_e = _init_lp_route__d__residual_RouteDResidual_e();
lean_mark_persistent(lp_route__d__residual_RouteDResidual_e);
lp_route__d__residual_RouteDResidual_nPrime = _init_lp_route__d__residual_RouteDResidual_nPrime();
lean_mark_persistent(lp_route__d__residual_RouteDResidual_nPrime);
lp_route__d__residual_RouteDResidual_H2 = _init_lp_route__d__residual_RouteDResidual_H2();
lean_mark_persistent(lp_route__d__residual_RouteDResidual_H2);
lp_route__d__residual_RouteDResidual_BstarSq = _init_lp_route__d__residual_RouteDResidual_BstarSq();
lean_mark_persistent(lp_route__d__residual_RouteDResidual_BstarSq);
lp_route__d__residual_RouteDResidual_BstarFloor = _init_lp_route__d__residual_RouteDResidual_BstarFloor();
lean_mark_persistent(lp_route__d__residual_RouteDResidual_BstarFloor);
lp_route__d__residual_RouteDResidual_fullResidualClosed = _init_lp_route__d__residual_RouteDResidual_fullResidualClosed();
return lean_io_result_mk_ok(lean_box(0));
}
#ifdef __cplusplus
}
#endif
