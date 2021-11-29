import argparse
import sys
import io
import os
sys.path.append('/usr/local/lib/python3.8/site-packages')
from spot.impl import formula
import spot
from ltl_sat_check import sat_check
import time
from GORE import GoreCase
from aut_based_solution import *
from quick_solution import *

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Part-of-Speech Testing')
  parser.add_argument('-m', '--method', choices=['aut', 'quick'], default='aut', help='the method to solve BCs')
  parser.add_argument('-c', '--case', default='AAP', help='the case to solve')
  args = parser.parse_args()

  CASE_PATH = 'goal_case/'+args.case+'.txt'
  if not os.path.exists(CASE_PATH):
    raise RuntimeError('no such case!')
  case_file = io.open(CASE_PATH, 'r', encoding='utf-8')

  temp_case = {}
  for line in case_file.readlines():
    line = line.rstrip('\n')
    if len(line) > 0:
      if line.startswith('CASE:'):
        in_bc = False
        line = line[5:]
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

  goal_case = GoreCase(temp_case['name'], temp_case['doms'], temp_case['goals'], temp_case['BC'])

  if args.method == 'aut':
    get_bc_by_aut(goal_case)
  else:
    get_bc_by_quick_solution(goal_case)