import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
import buddy
import time
import io
import threading


def product3(left, right, allowed_conflict, abstraction_transition_list):
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
    conflict_atom = ''
    if bdd_1 & bdd_2 != buddy.bddfalse:
      return bdd_1 & bdd_2, conflict_atom
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
          if conflict_atom != '':
            conflict_atom += ', '
          conflict_atom += diff_ap
    return cond, conflict_atom
  
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
        cond, conflict_atom = bdd_tight_abstraction(lt.cond, rt.cond)
        if cond != buddy.bddfalse:
          # print('from ' , lsrc , ',' , rsrc , 'to' , lt.dst , ',' , rt.dst)
          acc = lt.acc | (rt.acc << shift)
          result.new_edge(osrc, dst(lt.dst, rt.dst), cond, acc)
          if lt.cond & rt.cond == buddy.bddfalse:
            abstraction_transition_list.append((osrc, sdict.get((lt.dst, rt.dst)), conflict_atom, cond))

  # Remember the origin of our states
  result.set_product_states(pairs)
  
  # Loop over all the properties we want to preserve if they hold in both automata
  for p in ( 'prop_complete', 'prop_weak', 'prop_inherently_weak', 
    'prop_terminal', 'prop_stutter_invariant', 'prop_state_acc'):
    if getattr(left, p)() and getattr(right, p)():
      getattr(result, p)(True)

  # print(sdict)
  return result


def del_abstraction_edge(aut, edge):
  o_i = aut.out_iteraser(edge[0])
  while o_i:
    o = o_i.current()
    # print(o.dst)
    if o.dst == edge[1]:
      o.cond = buddy.bddfalse
    o_i.advance()
  o_i.erase()
  return


def re_abstraction_edge(aut, edge):
  o_i = aut.out_iteraser(edge[0])
  while o_i:
    o = o_i.current()
    # print(o.dst)
    if o.dst == edge[1]:
      o.cond = edge[3]
    o_i.advance()
  o_i.erase()
  return


def run_2_bc(run, aut):
  plist = [p for p in run.prefix]
  clist = [c for c in run.cycle]
  if len(clist) > 1:
    return str(spot.twa_word(run))
  bct = spot.formula_tt()
  # prefix
  step = 0
  for p in plist:
    p_step = spot.bdd_format_formula(aut.get_dict(), p.label)
    p_step = spot.formula(p_step)
    for i in range(step):
      p_step = spot.formula_X(p_step)
    bct = spot.formula_And([bct, p_step])
    step += 1
  # cycle
  c_step = spot.bdd_format_formula(aut.get_dict(), clist[0].label)
  c_step = spot.formula_G(spot.formula(c_step))
  for i in range(step):
    c_step = spot.formula_X(c_step)
  bct = spot.formula_And([bct, c_step])
  # print(bct.to_str())
  return bct


def run_2_conflict_message(run, aut, edge):
  clist = [c for c in run.cycle]
  if len(clist) > 1:
    return 'a run of BC, can not be transferred to a formula'
  conflict_message = str(run)
  conflict_message += 'from ' + str(edge[0]) +' to ' + str(edge[1]) +' has conflict: ' + str(edge[2]) + '\n'
  # print(run)
  # state_num = aut.get_init_state_number()
  # for t in aut.out(1):
  #   print(spot.bdd_format_formula(aut.get_dict(), t.cond))
  # for r in run_list:
  #   for t in aut.out(state_num):
  #     if r.label == t.cond:
  #       print(state_num, t.dst)
  #       print(spot.bdd_format_formula(aut.get_dict(), r.label))
  #       conflict_message += spot.bdd_format_formula(aut.get_dict(), r.label)
  #       if state_num == edge[0] and t.dst == edge[1]:
  #         conflict_message += ' --- has conflict: ' + edge[2]
  #       conflict_message += '\n'
  #       state_num = t.dst
  #       break
  return conflict_message


def copy_aut(aut):
  return spot.automaton(aut.to_str())


class delThread(threading.Thread):
  def __init__(self, aut, ab_t, abstraction_transition_list):
    threading.Thread.__init__(self)
    self.aut = aut
    self.ab_t = ab_t
    self.ab_list = abstraction_transition_list
    self.arun = None

  def get_result(self):
    return self.arun, self.aut

  def run(self):
    # delete other abstractions
    for del_ab_t in self.ab_list:
      if del_ab_t != self.ab_t:
        del_abstraction_edge(self.aut, del_ab_t)
    self.arun = self.aut.accepting_run()


def get_BC_in_ab_aut(aut, abstraction_transition_list):
  bcs = []
  conflict_message = []
  threads = []
  temp_aut = copy_aut(aut)
  
  for ab_t in abstraction_transition_list:
    del_abstraction_edge(temp_aut, ab_t)
  
  # select one abstraction
  for ab_t in abstraction_transition_list:
    re_abstraction_edge(temp_aut, ab_t)
    run = temp_aut.accepting_run()
    if run:
      bcs.append(run_2_bc(run, temp_aut))
      conflict_message.append(run_2_conflict_message(run, temp_aut, ab_t))
    del_abstraction_edge(temp_aut, ab_t)
  return bcs, conflict_message


class bcThread(threading.Thread):
  def __init__(self, f1, f2, allowed_conflict, gi, gj):
    threading.Thread.__init__(self)
    self.gi = gi
    self.gj = gj
    self.f1 = f1
    self.f2 = f2
    self.bcs = []
    self.conflict_message = []
    self.allowed_conflict = allowed_conflict

  def get_result(self):
    return self.f1.to_str(), self.f2.to_str(), self.bcs, self.conflict_message, self.gi, self.gj

  def run(self):
    abstraction_transition_list = []
    p1 = spot.translate(self.f1, 'ba')
    p2 = spot.translate(self.f2, 'ba')
    p3 = product3(p1, p2, self.allowed_conflict, abstraction_transition_list)
    self.bcs, self.conflict_message = get_BC_in_ab_aut(p3, abstraction_transition_list)


RESULT_PATH = 'case_result_abstraction/'


def get_bc_by_aut(gc):
  output_file = io.open(RESULT_PATH+gc.name+'_aut_based_solution.txt', 'w+', encoding = 'utf-8')
  output_file.write('case name: ' + gc.name + '\n')
  output_file.write('allowed conflicts: ' + ' '.join(gc.allowed_conflict) + '\n')
  start_time = time.time()
  bc_num = 0
  bc_word_num = 0

  allowed_conflict = gc.allowed_conflict
  # print(allowed_conflict)

  goals_set = 'noriginal'

  if goals_set == 'original':
    goals = gc.goals
  else:
    goals = gc.doms + gc.goals
  threads = []
  # for each two goals i and j
  for i in range(len(goals)-1):
    for j in range(i+1, len(goals)):
      if goals_set == 'original':
        f1 = spot.formula_And(gc.doms)
        f2 = spot.formula_And(gc.doms)
      else:
        f1 = spot.formula_tt()
        f2 = spot.formula_tt()
      # print(i, j)
      for k in range(len(goals)):
        if k == i:
          f1 = spot.formula_And([f1, spot.formula_Not(goals[k])])
        else:
          f1 = spot.formula_And([f1, goals[k]])
        if k == j:
          f2 = spot.formula_And([f2, spot.formula_Not(goals[k])])
        else:
          f2 = spot.formula_And([f2, goals[k]])

      t = bcThread(f1, f2, allowed_conflict, i, j)
      t.start()
      threads.append(t)
  
  contrasty_BC_num = 0
  for t in threads:
    t.join()
    f1, f2, bcs, conflict_message, gi, gj = t.get_result()

      # abstraction_transition_list = []
      # p1 = spot.translate(f1, 'ba')
      # p2 = spot.translate(f2, 'ba')
      # p3 = product3(p1, p2, allowed_conflict, abstraction_transition_list)

      # bcs, conflict_message = get_BC_in_ab_aut(p3, abstraction_transition_list)

    BCs_for_filtering = []
    if len(bcs) > 0:
      output_file.write('\n======================================================================\n')
      output_file.write('\nBC exists between goals: ' + f1 + ' --x-- ' + f2 + '\n')
      output_file.write('\n' )
      k = 0
      for bc in bcs:
        if type(bc) != str:
          output_file.write(' - ' + bc.to_str() + '\n')
          BCs_for_filtering.append(bc)
          bc_num += 1
        else:
          output_file.write(' - word: ' + bc + '\n')
          bc_word_num += 1
        output_file.write(' Conflict Message:\n' + conflict_message[k] + '\n')
        k += 1
    
      # filtering
      BCs_move = []
      for bc in BCs_for_filtering:
        if bc in BCs_move:
          continue
        # if not gc.isBC_2(bc, gi, gj):
        #   BCs_move.append(bc)
        #   pirnt('\n>>>>> WARRING! <<<<< THAT BC COULD NOT HAPPEN: ' + bc + '\n')
        #   continue
        for bc1 in BCs_for_filtering:
          if bc1 in BCs_move:
            continue
          if bc != bc1:
            a = gc.isWitness_2(bc, bc1, gi, gj)
            b = gc.isWitness_2(bc1, bc, gi, gj)
            if a and b:
              if len(bc.to_str()) < len(bc1.to_str()):
                BCs_move.append(bc1)
            if a and not b:
              BCs_move.append(bc1)
      for bc in BCs_move:
        BCs_for_filtering.remove(bc)
      contrasty_BC_num += len(BCs_for_filtering)

  output_file.write('\nBC solving time: ' + str(time.time()-start_time) + '\n')
  output_file.write('BC NUM: ' + str(bc_num) + '\n')
  output_file.write('BC contrasty NUM: ' + str(contrasty_BC_num) + '\n')
  output_file.write('BC word NUM: ' + str(bc_word_num) + '\n')
