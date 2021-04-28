import subprocess
AALTA_PATH = '/root/aalta-master/aalta'

def sat_check_aalta(ltl):
  p = subprocess.Popen(AALTA_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  p.stdin.write(ltl.encode())
  p.stdin.close()
  print('check: ' + ltl)
  res = p.stdout.read().decode('utf-8').split('\n')
  # print(res)
  return True if res[1] == 'sat' else False