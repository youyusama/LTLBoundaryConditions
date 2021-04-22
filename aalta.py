import subprocess
AALTA_PATH = '/root/aalta-master/aalta'

def sat_check_aalta(ltl):
  p = subprocess.Popen(AALTA_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  print(ltl)
  p.stdin.write(ltl.encode())
  p.stdin.close()
  return True if p.stdout.read().decode('utf-8').split('\n')[1] == 'sat' else False