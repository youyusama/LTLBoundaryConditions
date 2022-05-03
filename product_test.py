import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
import buddy
from ltl_sat_check import sat_check

# def formula_to_bdd(f):
#   a = spot.translate(spot.formula(f), 'sbacc', 'ba')
#   for t in a.out(0):
#     print(spot.bdd_format_formula(a.get_dict(), t.cond))
#     return t.cond

allowed_conflict = ['p', 'q']
abstraction_transition_list = []


def product3(left, right):
  # the twa_graph.is_existential() method returns a Boolean, not a spot.trival
  if not (left.is_existential() and right.is_existential()):
    raise RuntimeError("alternating automata are not supported")
  bdict = left.get_dict()
  if right.get_dict() != bdict:
    raise RuntimeError("automata should share their dictionary")

  result = spot.make_twa_graph(bdict)
  result.copy_ap_of(left)
  result.copy_ap_of(right)

  def remove_brackets(vec):
    vec = vec.replace('(', '')
    vec = vec.replace(')', '')
    return vec

  #  transfer a bdd string(without '|' ) to a bdd
  def cc_string_to_bdd(string_cc):
    bdd_cc = buddy.bddtrue
    string_cc = remove_brackets(string_cc)
    for ap in string_cc.split('&'):
      ap = ap.strip()
      if ap == '1':
        bdd_cc = bdd_cc & buddy.bddtrue
      elif ap == '0':
        bdd_cc = buddy.bddfalse
      elif ap.startswith('!'):
        bdd_cc = bdd_cc & buddy.bdd_nithvar(result.register_ap(ap[1:]))
      else:
        bdd_cc = bdd_cc & buddy.bdd_ithvar(result.register_ap(ap))
    return bdd_cc

  # the core abstraction operation
  def bdd_tight_abstraction(bdd_1, bdd_2):
    if bdd_1 & bdd_2 != buddy.bddfalse:
      return bdd_1 & bdd_2
    cond = buddy.bddfalse
    # for every two transitions
    for t1 in spot.bdd_format_formula(bdict, bdd_1).split('|'):
      for t2 in spot.bdd_format_formula(bdict, bdd_2).split('|'):
        t1 = remove_brackets(t1)
        t2 = remove_brackets(t2)
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
              aps[ap2] = 1
        if diff_count < 2 and diff_ap in allowed_conflict:
          string_cc = '1'
          for ap in aps:
            if ap != diff_ap:
              if aps[ap] == 1:
                string_cc += ' & ' + ap
              else:
                string_cc += ' & !' + ap
        else:
          string_cc = '0'
        bdd_cc = cc_string_to_bdd(string_cc)
        cond = cond | bdd_cc
        if cond != buddy.bddfalse:
          print('edge: ' + spot.bdd_format_formula(bdict, bdd_cc) + '  conflict: ' + diff_ap)
    return cond
  
  pairs = []   # our array of state pairs
  sdict = {}
  todo = []
  def dst(ls, rs):
    pair = (ls, rs)
    p = sdict.get(pair)
    if p is None:
      p = result.new_state()
      sdict[pair] = p
      todo.append((ls, rs, p))
      pairs.append((ls, rs)) # name each state
    return p
  
  result.set_init_state(dst(left.get_init_state_number(), right.get_init_state_number()))

  shift = left.num_sets()
  result.set_acceptance(shift + right.num_sets(), left.get_acceptance() & (right.get_acceptance() << shift))
  
  while todo:
    lsrc, rsrc, osrc = todo.pop()
    for lt in left.out(lsrc):
      for rt in right.out(rsrc):
        cond = bdd_tight_abstraction(lt.cond, rt.cond)
        if cond != buddy.bddfalse:
          print('from ' , lsrc , ',' , rsrc , 'to' , lt.dst , ',' , rt.dst)
          acc = lt.acc | (rt.acc << shift)
          result.new_edge(osrc, dst(lt.dst, rt.dst), cond, acc)
          if lt.cond & rt.cond == buddy.bddfalse:
            abstraction_transition_list.append((osrc, sdict.get((lt.dst, rt.dst))))

  # Remember the origin of our states
  result.set_product_states(pairs)
  
  # Loop over all the properties we want to preserve if they hold in both automata
  for p in ('prop_universal', 'prop_complete', 'prop_weak', 'prop_inherently_weak', 
    'prop_terminal', 'prop_stutter_invariant', 'prop_state_acc'):
    if getattr(left, p)() and getattr(right, p)():
      getattr(result, p)(True)

  # print(sdict)
  return result

a1 = spot.translate('!G(p -> Fq) & G(q -> p)', 'ba', 'sbacc')
a2 = spot.translate('G(p -> Fq) & !G(q -> p)', 'ba', 'sbacc')
# a1 = spot.translate('!G(ta <-> Xtc) & G(Xcc -> (ca & go)) & G(ta -> !go) & G(tc -> !cc)', 'ba', 'sbacc')
# a2 = spot.translate('G(ta <-> Xtc) & !G(Xcc -> (ca & go)) & G(ta -> !go) & G(tc -> !cc)', 'ba', 'sbacc')
# a1 = spot.translate('!Ga & Gb', 'ba', 'sbacc')
# a2 = spot.translate('Ga & !Gb', 'ba', 'sbacc')
# a1 = spot.translate('!G(h -> Xp) & G(m -> X!p)', 'ba', 'sbacc')
# a2 = spot.translate('G(h -> Xp) & !G(m -> X!p)', 'ba', 'sbacc')

p3 = product3(a1, a2)
# p3 = p3.postprocess('ba')
# p3.merge_states()
p3.merge_edges()
p3.purge_dead_states()
p3.save('output.dot', format='dot')
run = p3.accepting_run()


# if run:
#   print(run)
#   plist = [p for p in run.prefix]
#   bct = spot.formula_tt()
#   step = 0
#   for p in plist:
#     p_step = spot.bdd_format_formula(p3.get_dict(), p.label)
#     p_step = spot.formula(p_step)
#     for i in range(step):
#       p_step = spot.formula_X(p_step)
#     bct = spot.formula_And([bct, p_step])
#     step += 1
#   print(bct.to_str())
# else:
#   print('empty')

# print(abstraction_transition_list)

# not used
def run_has_abstraction(aut, run):
  abstraction_transition = []
  run_list = [p for p in run.prefix] + [c for c in run.cycle]
  state_num = aut.get_init_state_number()
  state_list = [state_num]
  for r in run_list:
    for t in aut.out(state_num):
      if r.label == t.cond:
        state_num = t.dst
        state_list.append(state_num)
        break
  ab_count = 0
  for i in range(len(state_list)-1):
    # print((state_list[i], state_list[i+1]))
    if (state_list[i], state_list[i+1]) in abstraction_transition_list:
      abstraction_transition.append((state_list[i], state_list[i+1]))
  return abstraction_transition


def del_abstraction_edge(aut, edge):
  for t in aut.out(edge[0]):
    if t.dst == edge[1]:
      t.cond = buddy.bddfalse
      return aut


def run_2_bc(run):
  plist = [p for p in run.prefix]
  clist = [c for c in run.cycle]
  if len(clist) > 1:
    return 'Can not transfer to formula: ' + spot.twa_word(run)
  bct = spot.formula_tt()
  # prefix
  step = 0
  for p in plist:
    p_step = spot.bdd_format_formula(p3.get_dict(), p.label)
    p_step = spot.formula(p_step)
    for i in range(step):
      p_step = spot.formula_X(p_step)
    bct = spot.formula_And([bct, p_step])
    step += 1
  # cycle
  c_step = spot.bdd_format_formula(p3.get_dict(), clist[0].label)
  c_step = spot.formula_G(spot.formula(c_step))
  for i in range(step):
    c_step = spot.formula_X(c_step)
  bct = spot.formula_And([bct, c_step])
  # print(bct.to_str())
  return bct


def copy_aut(aut):
  return spot.automaton(aut.to_str('hoa', '1.1'))


def get_BC_in_ab_aut(aut, abstraction_transition_list):
  # select one abstraction
  for ab_t in abstraction_transition_list:
    temp_aut = copy_aut(aut)
    # delete other abstractions
    for del_ab_t in abstraction_transition_list:
      if del_ab_t != ab_t:
        del_abstraction_edge(temp_aut, del_ab_t)
    # get bc
    run = temp_aut.accepting_run()
    if run:
      bcs.append(run_2_bc(run))
      meaningful_bcs.append(run_2_m_bc(run))

meaningful_bcs = []
bcs = []
get_BC_in_ab_aut(p3, abstraction_transition_list)
for bc in bcs:
  print(bc.to_str())

print(abstraction_transition_list)