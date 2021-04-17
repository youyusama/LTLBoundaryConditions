import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
from aalta import sat_check_aalta

class GoreCase:
  def __init__(self, name, doms, goals):
    self.name = name
    self.doms = [spot.formula(dom) for dom in doms] if len(doms) > 0 else []
    self.goals = [spot.formula(goal) for goal in goals]

  def showdg(self):
    print(spot.formula.And(self.doms+self.goals).to_str('spin'))

  def isBC(self, bc):
    bc = spot.formula(bc)
    if sat_check_aalta(spot.formula_And(self.doms + self.goals + bc)):
      return False
    else:
      for i in range(len(self.goals)):
        if not sat_check_aalta(spot.formula_And(self.doms + [goal for goal in goals if goal != goals[i]] + bc)):
          return False
    return True