import subprocess
AALTA_PATH = '/root/aalta-master/aalta'
# case_file = io.open('unsat.txt', 'w+', encoding='utf-8')
import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot

def sat_check(ltl):
  #aalta
  ltl = ltl.replace('X', 'X ')
  p = subprocess.Popen(AALTA_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  p.stdin.write(ltl.encode())
  p.stdin.close()
  try:
    p.wait(3)
    # print('aalta check: ' + ltl)
    res = p.stdout.read().decode('utf-8').split('\n')
    # print(res)
    if len(res) == 3:
      # if res[1] != 'sat':
      #   case_file.write(ltl+'\n')
      return True if res[1] == 'sat' else False
  except:
    print('can not handle ltl:' + ltl)
  else:
  
    #spot check
    f = spot.formula(ltl)
    a = f.translate('ba')
    return False if a.is_empty() else True
  