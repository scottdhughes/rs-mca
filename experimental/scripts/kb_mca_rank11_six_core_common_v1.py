"""Shared exact arithmetic for the KoalaBear rank-eleven router."""
from __future__ import annotations
from fractions import Fraction
from math import comb

ROW={"p":2130706433,"extension_degree":6,"n":2097152,"K":1048576,
     "m":1116048,"w":67472,"near":134944,"budget":274980728111395087}
THETA_RESOURCE=106618568137036225644
AFFINE_DIMENSION=10
FIXED_RIGHT_RAY_CAP=8147918
PARENT="193b7bf99a5cc7ccea042f25677e698d9f988eee"

class Reject(ValueError):
    pass

def require(condition:bool,message:str)->None:
    if not condition: raise Reject(message)

def ceil_fraction(x:Fraction)->int:
    return -(-x.numerator//x.denominator)

def low_required(tau:int)->int:
    return ROW["budget"]-ROW["near"]-THETA_RESOURCE//(tau+1)+1

def pair_list_cap(rank:int,tau:int)->int:
    if rank==0:return 1
    return comb(ROW["K"]+rank,rank)//comb(ROW["w"]-tau+rank,rank)

def pair_owner_cap(tau:int)->int:
    return ROW["n"]-(ROW["m"]-tau)

def list_count_for_outside(q:int,tau:int,rank:int=10)->int:
    if q<0 or q>ROW["K"]:return 0
    return comb(ROW["K"]-q+rank,rank)//comb(ROW["w"]-tau+rank,rank)

def fixed_left_cap_at_q(q:int,tau:int)->int:
    return q*list_count_for_outside(q,tau)+1

def numerator_sequence(q:int)->int:
    return q*comb(ROW["K"]-q+AFFINE_DIMENSION,AFFINE_DIMENSION)
