import subprocess
AALTA_PATH = '/home/youyu/aalta/aalta'
# case_file = io.open('unsat.txt', 'w+', encoding='utf-8')
import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot

def sat_check(ltl):
  #spot
  # print('--', ltl)
  f = spot.formula(ltl)
  a = f.translate('ba')
  return False if a.is_empty() else True

  # #aalta
  # ltl = ltl.replace('X', 'X ')
  # # print('aalta check: ' + ltl)
  # p = subprocess.Popen(AALTA_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  # p.stdin.write(ltl.encode())
  # p.stdin.close()
  # # res = p.stdout.read().decode('utf-8').split('\n')
  # # return True if res[1] == 'sat' else False

  # try:
  #   p.wait(5)
  #   res = p.stdout.read().decode('utf-8').split('\n')
  #   # p.kill()
  #   # print(res)
  #   if len(res) == 3:
  #     # if res[1] != 'sat':
  #     #   case_file.write(ltl+'\n')
  #     return True if res[1] == 'sat' else False
  # except:
  #   # print('can not handle ltl:' + ltl)
  #   print('can not handle ltl')
  # else:
  #   # p.kill()
  #   #spot check
  #   f = spot.formula(ltl)
  #   a = f.translate('ba')
  #   return False if a.is_empty() else True
  