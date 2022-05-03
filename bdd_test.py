import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
import buddy
from ltl_sat_check import sat_check

# bdict = spot.make_bdd_dict()
# aut = spot.make_twa_graph(bdict)

# p = buddy.bdd_ithvar(aut.register_ap('p'))
# q = buddy.bdd_ithvar(aut.register_ap('q'))
# r = buddy.bdd_ithvar(aut.register_ap('r'))

# p1 = buddy.bdd_not(q) & r
# p2 = buddy.bdd_not(p) & q

# print('p1 is: ', spot.bdd_format_formula(bdict, p1))
# print('p2 is: ', spot.bdd_format_formula(bdict, p2))
# p3 = p1|p2
# print('p2 is: ', spot.bdd_format_formula(bdict, p3))


#  transfer a bdd string(without '|' ) to a bdd
def cc_string_to_bdd(string_cc):
  bdd_cc = buddy.bddtrue
  string_cc = string_cc.replace('(', '')
  string_cc = string_cc.replace(')', '')
  for ap in string_cc.split('&'):
    ap = ap.strip()
    if ap == '1':
      bdd_cc = bdd_cc & buddy.bddtrue
    elif ap == '0':
      bdd_cc = buddy.bddfalse
    elif ap.startswith('!'):
      bdd_cc = bdd_cc & buddy.bdd_nithvar(aut.register_ap(ap[1:]))
    else:
      bdd_cc = bdd_cc & buddy.bdd_ithvar(aut.register_ap(ap))
  return bdd_cc


# the core abstraction operation
def bdd_tight_abstraction(bdd_1, bdd_2):
  if bdd_1 & bdd_2 != buddy.bddfalse:
    return bdd_1 & bdd_2
  cond = buddy.bddfalse
  # for every two transitions
  for t1 in spot.bdd_format_formula(bdict, bdd_1).split('|'):
    for t2 in spot.bdd_format_formula(bdict, bdd_2).split('|'):
      aps = {}
      diff_count = 0
      diff_ap = ''
      for ap1 in t1.split('&'):
        ap1 = ap1.strip()
        if ap1.startswith('!'):
          aps[ap1[1:]] = 0
        else:
          aps[ap1] = 1
      for ap2 in t2.split('&'):
        ap2 = ap2.strip()
        if ap2.startswith('!'):
          if ap2[1:] in aps:
            if aps[ap2[1:]] != 0:
              diff_count += 1
              diff_ap = ap2[1:]
          else:
            aps[ap2[1:]] = 0
        else:
          if ap2 in aps:
            if aps[ap2] != 1:
              diff_count += 1
              diff_ap = ap2
          else:
            aps[ap2] = 0
      if diff_count < 2:
        string_cc = '1'
        for ap in aps:
          if ap != diff_ap:
            if aps[ap] == 1:
              string_cc += ' & ' + ap
            else:
              string_cc += ' & !' + ap
      else:
        string_cc = '0'
      print(string_cc)
      bdd_cc = cc_string_to_bdd(string_cc)
      cond = cond | bdd_cc
  return cond

# print(spot.bdd_format_formula(bdict, bdd_tight_abstraction(p1, p2)))

# print(spot.bdd_format_formula(bdict, buddy.bdd_not(p2)&p1))
# print(buddy.bdd_pathcount(buddy.bdd_not(p2)&p1))