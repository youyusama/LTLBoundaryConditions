import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
from aalta import sat_check_aalta
import io
from GORE import GoreCase

gore_cases = []

case_file = io.open('GORE_case.txt', 'r', encoding='utf-8')
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

print(gc_list[2].isBC('F (call&!open&( G(!atfloor & Xopen) | G(!atfloor & !open) ))', show_reason=True))
# nonsense_bc = gc_list[7].getNonsenseBC()
# for bc in nonsense_bc:
#   print(gc_list[7].isBC(bc))
# print(spot.formula('').to_str('spin'))
# for gc in gc_list:
#   print(gc.name)
#   nonsense_bc = gc.getNonsenseBC()
#   for bc in gc.gen_t_bc:
#     print('check:' + bc.to_str('spin'))
#     if not gc.isBC(bc, show_reason=True):
#       print(bc)
#   for bc in nonsense_bc:
#     if not gc.isBC(bc, show_reason=True):
#       print(bc)

# a1 = ''
# for a in spot.automata('''
# HOA: v1
# States: 4
# Start: 0
# AP: 3 "call" "open" "atfloor"
# acc-name: Buchi
# Acceptance: 1 Inf(0)
# properties: trans-labels explicit-labels state-acc
# --BODY--
# State: 0
# [!0 | 1] 0
# [0&!1] 1
# [!0&!2 | 1&!2] 2
# State: 1
# [!1] 1
# [1] 3
# State: 2
# [1] 3
# State: 3 {0}
# [0&!1] 1
# [t] 3
# --END--
# '''
# ):
#   a1 = a
# a2 = spot.formula('G (X open->atfloor)').translate('BA', 'Deterministic')
# prod = spot.product(a1, a2)
# print(prod.to_str())