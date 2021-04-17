import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
from aalta import sat_check_aalta

# print(sat_check_aalta('[] (q -> s)'))
f = spot.formula('G (q->s)')
print(f.to_str('spin', parenth=True))

