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
    print(spot.formula_And(self.doms+self.goals).to_str('spin'))

  def isBC(self, bc):
    if type(bc) is str:
      bc = spot.formula(bc)
    c = spot.language_containment_checker()
    if c.equal(spot.formula('true'), bc) or c.equal(spot.formula('false'), bc):
      return False
    if c.equal(spot.formula_Not(spot.formula_And(self.doms + self.goals)), bc):
      return False
    if sat_check_aalta(spot.formula_And(self.doms + self.goals + [bc,]).to_str('spin')):
      return False
    else:
      for i in range(len(self.goals)):
        if not sat_check_aalta(spot.formula_And(self.doms + [goal for goal in self.goals if goal != self.goals[i]] + [bc,]).to_str('spin')):
          return False
    return True

  def isGeneral(self, bc1, bc2):
    if type(bc1) is str:
      bc1 = spot.formula(bc1)
    if type(bc2) is str:
      bc2 = spot.formula(bc2)
    if not sat_check_aalta(spot.formula_And([bc2, spot.formula_Not(bc1)]).to_str('spin')):
      return True
    else:
      return False

  def isWitness(self, bc1, bc2):
    if type(bc1) is str:
      bc1 = spot.formula(bc1)
    if type(bc2) is str:
      bc2 = spot.formula(bc2)
    if not self.isBC(spot.formula_And([bc2, spot.formula_Not(bc1)])):
      return True
    else:
      return False
  
  def getNonsenseBC(self):
