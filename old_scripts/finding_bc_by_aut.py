import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
from ltl_sat_check import sat_check
import io
from aut_p import *
from GORE import GoreCase
from queue import Queue

gore_cases = []
CASE_NAME = 'LB'
CASE_PATH = 'goal_case/'+CASE_NAME+'.txt'
RESULT_PATH = 'case_result/'

case_file = io.open(CASE_PATH, 'r', encoding='utf-8')

temp_case = {}
in_bc = False
for line in case_file.readlines():
  line = line.rstrip('\n')
  if len(line) > 0:
    if line.startswith('CASE:'):
      in_bc = False
      line = line[5:]
      temp_case = {}
      temp_case['name'] = line
      temp_case['BC'] = []
    if in_bc:
      temp_case['BC'].append(line)
    if line.startswith('BC:'):
      in_bc = True
    if line.startswith('DOM:'):
      line = line[5:-1]
      temp_case['doms'] = line.split(',') if  len(line) > 0 else []
    if line.startswith('GOALS:'):
      line = line[7:-1]
      temp_case['goals'] = line.split(',')
      gore_cases.append(temp_case)

gc_list = []
for case in gore_cases:
  gc_list.append(GoreCase(case['name'], case['doms'], case['goals'], case['BC']))

def aut_has_acc(aut):
  for s in range(0, aut.num_states()):
    if aut.state_is_accepting(s):
      return True
  return False

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



def get_bc_by_aut():
  gc = gc_list[0]
  dng_aut = gc.dandng_aut()
  aut_phi = filter_ngd(dng_aut, gc.goals)
  aut_phi.save('output.dot', format='dot')

  pbcs = get_pbcs_from_aut(aut_phi)
  for pbc in pbcs:
    print(pbc.to_str())
    no_relation_gi = []
    isBC_result = gc.isBC_t(pbc, no_relation_gi)

    while isBC_result != -1 and isBC_result != -2:
      no_relation_gi.append(isBC_result)
      isBC_result = gc.isBC_t(pbc, no_relation_gi)

    if isBC_result == -1:
      print('not bc')
    elif isBC_result == -2:
      print('is bc')
    

def show_bc_in_dot():
  gc = gc_list[0]
  gc.showdg()
  ngd_aut = gc.dandng_aut()
  # ngd_aut.highlight_edges([8,12],1)
  # ngd_aut.save('output.dot', format='dot')
  bc = filter_ngd(ngd_aut, gc.goals)

  # bc.highlight_edges([4,8,12],1)
  # run = bc.accepting_run()
  # run.highlight(0)
  # bc.highlight_edges([2,6,8],2)
  # bc.highlight_edges([3,12],4)
  bc.save('output.dot', format='dot')


if __name__ == '__main__':
  # show_bc_in_dot()
  get_bc_by_aut()