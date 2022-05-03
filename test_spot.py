import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
import buddy
import resource

aut = spot.translate(spot.formula('(F(p & X(p & Xh)) & G((!h | Xp) & (!m | X!p))) | (F(h & X!p) & G((!m | X!p) & (!p | X(!p | X!h))))'))
for i in range(100):
  newaut = spot.automaton(aut.to_str())
  for i in range(0, 10):
    for t in newaut.out(i):
      pass
  del newaut
  print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)