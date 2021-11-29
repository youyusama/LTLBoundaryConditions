import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
import buddy
import time
import io

def custom_product(negG_aut, g_aut):
  bdict = negG_aut.get_dict()
  if g_aut.get_dict() != bdict:
    raise RuntimeError("automata should share their dictionary")   
  result = spot.make_twa_graph(bdict)
  result.copy_ap_of(negG_aut)
  result.copy_ap_of(g_aut)
  sdict = {}
  todo = []
  def dst(ls, rs):
    pair = (ls, rs)
    p = sdict.get(pair)
    if p is None:
      p = result.new_state()
      sdict[pair] = p
      todo.append((ls, rs, p))
    return p
  result.set_init_state(dst(negG_aut.get_init_state_number(), g_aut.get_init_state_number()))
  result.set_buchi()
  result.prop_state_acc(True)

  new_dead_states = []
  while todo:
    lsrc, rsrc, osrc = todo.pop()
    if negG_aut.state_is_accepting(lsrc):
      for lt in negG_aut.out(lsrc):
        for rt in g_aut.out(rsrc):
          result.new_edge(osrc, osrc, lt.cond, [0])
      continue
    for lt in negG_aut.out(lsrc):
      for rt in g_aut.out(rsrc):
        cond = lt.cond & rt.cond
        if cond != buddy.bddfalse:
          result.new_edge(osrc, dst(lt.dst, rt.dst), cond)

  result.merge_states()
  result.merge_edges()
  result.purge_dead_states()
  return result


def filter_ngd(ngd_aut, goals):
  for goal in goals:
    # print('---')
    goal_aut = spot.translate(goal, 'ba', 'det')
    ngd_aut = custom_product(ngd_aut, goal_aut)
  return ngd_aut


def get_pbcs_from_aut(aut):
  pbcs = []
  acc = []
  for s in range(0, aut.num_states()):
    if aut.state_is_accepting(s):
      acc.append(s)

  for acc_i in acc:
    aut_temp = spot.automaton(aut.to_str('hoa', '1.1'))
    for acc_j in acc:
      if acc_j != acc_i:
        for t in aut_temp.out(acc_j):
          t.cond = buddy.bddfalse
    run = aut_temp.accepting_run()
    plist = [p for p in run.prefix]
    pbct = spot.formula_tt()
    step = 0
    for p in plist:
      p_step = spot.bdd_format_formula(aut.get_dict(), p.label)
      p_step = spot.formula(p_step)
      for i in range(step):
        p_step = spot.formula_X(p_step)
      pbct = spot.formula_And([pbct, p_step])
      step += 1
    pbcs.append(pbct)
  return pbcs


RESULT_PATH = 'case_result_aut/'


def get_bc_by_aut(gc):
  output_file = io.open(RESULT_PATH+gc.name+'_aut_based_solution.txt', 'w+', encoding = 'utf-8')
  output_file.write('case name: ' + gc.name + '\n')
  start_time = time.time()

  # translate the automata Dom & !G
  dng_aut = gc.dandng_aut()
  # calculate the automata phi by the reachability production
  aut_phi = filter_ngd(dng_aut, gc.goals)
  # show graph
  aut_phi.save('output.dot', format='dot')
  # get bcs from automata phi
  pbcs = get_pbcs_from_aut(aut_phi)

  # check the solved bcs
  for pbc in pbcs:
    no_relation_gi = []
    isBC_result = gc.isBC_t(pbc, no_relation_gi)

    while isBC_result != -1 and isBC_result != -2:
      no_relation_gi.append(isBC_result)
      print(no_relation_gi)
      isBC_result = gc.isBC_t(pbc, no_relation_gi)

    if isBC_result == -1:
      output_file.write('the potential BC: ' + pbc.to_str() + '\n')
    elif isBC_result == -2:
      output_file.write('*** the confirmed BC: \n')
      output_file.write(' - ' + pbc.to_str() + '\n')
      output_file.write('between the goals: \n')
      for i in range(len(gc.goals)):
        if i not in no_relation_gi:
          output_file.write('goal: ' + gc.goals[i].to_str() + '\n')
      

  output_file.write('\nbc solving time: ' + str(time.time()-start_time) + '\n')