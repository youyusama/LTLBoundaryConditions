import subprocess
import io
AALTA_PATH = '/root/aalta-master/aalta'
# case_file = io.open('unsat.txt', 'w+', encoding='utf-8')

def sat_check_aalta(ltl):
  ltl = ltl.replace('X', 'X ')
  p = subprocess.Popen(AALTA_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  p.stdin.write(ltl.encode())
  p.stdin.close()
  print('aalta check: ' + ltl)
  res = p.stdout.read().decode('utf-8').split('\n')
  print(res)
  # if res[1] != 'sat':
  #   case_file.write(ltl+'\n')
  return True if res[1] == 'sat' else False