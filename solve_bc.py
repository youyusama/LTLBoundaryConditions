import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
from aalta import sat_check_aalta
import io
from GORE import GoreCase

gore_cases = []

case_file = io.open('GORE_case.txt', 'r', encoding='utf-8')
temp_case = {}
for line in case_file.readlines():
  line = line.rstrip('\n')
  if len(line) > 0:
    if line.startswith('CASE:'):
      line = line[5:]
      temp_case = {}
      temp_case['name'] = line
    if line.startswith('DOM:'):
      line = line[5:-1]
      temp_case['doms'] = line.split(',') if  len(line) > 0 else []
    if line.startswith('GOALS:'):
      line = line[7:-1]
      temp_case['goals'] = line.split(',')
      gore_cases.append(temp_case)

gc_list = []
for case in gore_cases:
  gc_list.append(GoreCase(case['name'], case['doms'], case['goals']))

nonsense_bc = gc_list[7].getNonsenseBC()
print(nonsense_bc)
for bc in nonsense_bc:
  print(gc_list[7].isBC(bc))
# print(spot.formula('').to_str('spin'))