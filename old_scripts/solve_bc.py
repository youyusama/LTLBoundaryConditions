import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
from ltl_sat_check import sat_check
import io
from GORE import GoreCase

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


def check_nonsensebc_right():
  for gc in gc_list:
    print('check goal case: ', gc.name)
    nonsense_bc = gc.getNonsenseBC()
    for bc in nonsense_bc:
      print('\nbc: ', bc.to_str(), '\n', str(gc.isBC(bc, show_reason = True)))

def is_bc_right():
  for gc in gc_list:
    print(gc.name)
    for bc in gc.gen_t_bc:
      print('\nbc: ', bc.to_str(), '\n', str(gc.isBC(bc, show_reason = True)))
      # print(bc,gc.isBC(bc))

def why_imp():
  for gc in gc_list:
    print(gc.name)
    gc.its_impossible()

def not_gd_bc():
  for gc in gc_list:
    print(gc.name, gc.is_not_gd_BC())
    gc.is_not_gd_BC()

def real_bc_num():
  for gc in gc_list:
    print(gc.name)
    print(len(gc.gen_t_bc))
    bcset = gc.gen_t_bc
    for bc in bcset:
      for bc1 in bcset:
        if bc != bc1 and gc.isWitness(bc, bc1):
          bcset.remove(bc1)
    print(len(bcset))


def is_nonsense_contrasty():
  for gc in gc_list:
    print(gc.name)
    nonsense_bc = gc.getNonsenseBC()
    print(len(nonsense_bc))
    for bc in nonsense_bc:
      for bc1 in nonsense_bc:
        if bc != bc1 and gc.isWitness(bc, bc1):
          # nonsense_bc.remove(bc1)
          print(bc.to_str('spot')+'-----'+ bc1.to_str('spot'))
    print(len(nonsense_bc))


def is_nonsense_good():
  output_file = io.open(RESULT_PATH+CASE_NAME+'quick_solution.txt', 'w+', encoding = 'utf-8')
  for gc in gc_list:
    print(gc.name)
    output_file.write('case: ' + gc.name + '-----------------------------\n')
    nonsense_bc = gc.getNonsenseBC()
    excluded_bc = set()
    for n_bc in nonsense_bc:
      for bc in gc.gen_t_bc:
        # if gc.isGeneral(n_bc, bc):
        #   excluded_bc.add(bc)
        #   output_file.write('bc: ' + bc.to_str() +'\n be generaled by n_bc: ' + n_bc.to_str() + '\n')
        if gc.isWitness(n_bc, bc):
          excluded_bc.add(bc)
          output_file.write('bc: ' + bc.to_str() +'\n be witnessed by n_bc: ' + n_bc.to_str() + '\n')
        if gc.isWitness(bc, n_bc):
          output_file.write('bc: ' + n_bc.to_str() +'\n be witnessed by: ' + bc.to_str() + '\n')  
    if len(excluded_bc) < len(gc.gen_t_bc):
      for bc in gc.gen_t_bc:
        if bc not in excluded_bc:
          print('!!!!\n' + bc.to_str())

def quickSolutionAll():
  for gc in gc_list:
    BCg, BCs, gt, et = gc.quickSolution()
    all_bc = 0
    cover_bc = 0
    for bc in BCs:
      for gene_bc in gc.gen_t_bc:
        if not gc.isBC(gene_bc):
          print('fuck')
        all_bc += 1
        if gc.isWitness(bc, gene_bc) and not gc.isWitness(gene_bc, bc):
          cover_bc += 1
  output_file = io.open(RESULT_PATH+CASE_NAME+'_quick_solution.txt', 'w+', encoding = 'utf-8')
  output_file.write('case name: ' + gc.name + '\n')
  output_file.write('solved bc num: ' + str(len(BCg)) + '\n')
  output_file.write('bc solving time: ' + str(gt) + '\n')
  for bc in BCg:
    output_file.write(' - ' + bc.to_str() + '\n')
  output_file.write('\n')
  output_file.write('contrastive bc num: ' + str(len(BCs)) + '\n')
  output_file.write('bc evaluation time: ' + str(et) + '\n')
  for bc in BCs:
    output_file.write(' - ' + bc.to_str() + '\n')
  output_file.write('cover rate: ' + str(cover_bc/all_bc if all_bc != 0 else 0) + '\n')


def get_by_quick_solution(gc):
  BCg, BCs, gt, et = gc.quickSolution()
  all_bc = 0
  cover_bc = 0
  for bc in BCs:
    for gene_bc in gc.gen_t_bc:
      if not gc.isBC(gene_bc):
        print('fuck')
      all_bc += 1
      if gc.isWitness(bc, gene_bc) and not gc.isWitness(gene_bc, bc):
        cover_bc += 1

  output_file = io.open(RESULT_PATH+CASE_NAME+'_quick_solution.txt', 'w+', encoding = 'utf-8')
  output_file.write('case name: ' + gc.name + '\n')
  output_file.write('solved bc num: ' + str(len(BCg)) + '\n')
  output_file.write('bc solving time: ' + str(gt) + '\n')
  for bc in BCg:
    output_file.write(' - ' + bc.to_str() + '\n')
  output_file.write('\n')
  output_file.write('contrastive bc num: ' + str(len(BCs)) + '\n')
  output_file.write('bc evaluation time: ' + str(et) + '\n')
  for bc in BCs:
    output_file.write(' - ' + bc.to_str() + '\n')
  output_file.write('cover rate: ' + str(cover_bc/all_bc if all_bc != 0 else 0) + '\n')
  

def get_contrasty():
  gc = gc_list[0]
  BCs_real = gc.gen_t_bc
  for bc in BCs_real:
    if not gc.isBC(bc):
      BCs_real.remove(bc)
      continue
    for bc1 in BCs_real:
      if bc != bc1:
        a = gc.isWitness(bc, bc1)
        b = gc.isWitness(bc1, bc)
        if a and b:
          if len(bc.to_str()) < len(bc1.to_str()):
            BCs_real.remove(bc1)
        if a and not b:
          BCs_real.remove(bc1)
  for bc in BCs_real:
    print(bc.to_str())

if __name__ == '__main__':
  is_bc_right()
  # gc_list[7].quickSolution()
  # quickSolutionAll()
  # get_contrasty()
  # not_gd_bc()
  # real_bc_num()
  # is_nonsense_contrasty()
  # why_imp()
  # check_nonsensebc_right()
  # is_nonsense_good()
  # print(gc_list[0].isWitness('!a|F!b','X!a|F!b'))
  # print(gc_list[1].isWitness('X!(h->Xp)|F!(m->X!p)', '(!(h->Xp)|F!(m->X!p)) & (XF!(h->Xp)|F!(m->X!p))'))
  # f1 = spot.formula('[]<>idle && [](X!grant_0 || X((!idle && !request_0) U (idle && !request_0))) && [](Xgrant_1 -> request_1) && !<>[](request_1 && X!grant_1) && []X(!grant_0 || !grant_1) && []((request_0 && Xrequest_1) -> XX(grant_0 && grant_1)) && [](!idle -> X(!grant_0 && !grant_1)) && [](request_0 -> grant_1) && [](Xgrant_0 -> request_0) && ([](request_0 && X!grant_0) || <>[](request_1 && X!grant_1) || <>[]!idle || <>(Xgrant_0 && X((idle || request_0) V (!idle || request_0))) || <>(!request_1 && Xgrant_1) || <>X(grant_0 && grant_1) || <>(request_0 && Xrequest_1 && XX(!grant_0 || !grant_1)) || <>(!idle && X(grant_0 || grant_1)) || <>(!grant_1 && request_0) || <>(!request_0 && Xgrant_0))')
  # f2 = spot.formula('F ( p & r & !s ) U (p & !r & !s )')
  # a = f1.translate('ba')
  # print(a.is_empty())
  # print(sat_check(f1.to_str()))
  # print(sat_check(spot.formula_And([spot.formula_Not(f1), f2]).to_str()))
  # print(sat_check(spot.formula_And([f1, spot.formula_Not(f2) ]).to_str()))
  # print(sat_check(spot.formula('[](ta <-> X tc) && [](X cc -> (ca && go)) && [](ta -> !go) && [](tc -> !cc) && <>((cc && tc) V ((cc && tc) || (go && tc)))')))
