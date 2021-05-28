import sys

from spot.impl import formula
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
from ltl_sat_check import sat_check

class GoreCase:
  def __init__(self, name, doms, goals, bcs):
    self.name = name
    self.doms = [spot.formula(dom) for dom in doms] if len(doms) > 0 else []
    self.goals = [spot.formula(goal) for goal in goals]
    self.gen_t_bc = [spot.formula(bc) for bc in bcs] if len(bcs) > 0 else []


  def showdg(self):
    print(spot.formula_And(self.doms+self.goals).to_str('spin'))


  def isBC(self, bc, show_reason = False):
    if type(bc) is str:
      bc = spot.formula(bc)
    c = spot.language_containment_checker()
    #non-triviality
    if not sat_check(bc.to_str('spin')) or not sat_check(spot.formula_Not(bc).to_str('spin')):
      if show_reason:
        print('bc is true or false')
      return False
    not_g = spot.formula_Not(spot.formula_And(self.goals))
    if not sat_check(spot.formula_And([not_g, spot.formula_Not(bc)]).to_str('spin')) and not sat_check(spot.formula_And([spot.formula_Not(not_g), bc]).to_str('spin')):
      if show_reason:
        print('trivial')
      return False
    #logical incosistency
    if sat_check(spot.formula_And(self.doms + self.goals + [bc,]).to_str('spin')):
      if show_reason:
        print('consistency')
      return False
    else:
    #minimality
      for i in range(len(self.goals)):
        if not sat_check(spot.formula_And(self.doms + [goal for goal in self.goals if goal != self.goals[i]] + [bc,]).to_str('spin')):
          if show_reason:
            print('not minimality')
          return False
    return True


  def isGeneral(self, bc1, bc2):
    if type(bc1) is str:
      bc1 = spot.formula(bc1)
    if type(bc2) is str:
      bc2 = spot.formula(bc2)
    if not sat_check(spot.formula_And([bc2, spot.formula_Not(bc1)]).to_str('spin')):
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


  def its_impossible(self):
    for i in range(len(self.goals)):
      if not sat_check( spot.formula_And( self.doms + [goal if goal != self.goals[i] else spot.formula_Not(goal) for goal in self.goals ] ).to_str('spin') ):
        print('why')


  def is_not_gd_BC(self):
    not_g_d = spot.formula_Not(spot.formula_And(self.goals + self.doms))
    #logical incosistency
    if sat_check(spot.formula_And(self.doms + self.goals + [not_g_d,]).to_str('spot')):
      return False
    else:
    #minimality
      for i in range(len(self.goals)):
        if not sat_check(spot.formula_And(self.doms + [goal for goal in self.goals if goal != self.goals[i]] + [not_g_d,]).to_str('spin')):
          return False
    return True

  def getNonsenseBC(self):
    f = spot.formula_Not(spot.formula_And(self.doms + self.goals))
    sim_option = spot.tl_simplifier_options()
    sim_option.reduce_basics = False
    sim = spot.tl_simplifier(sim_option)
    f = sim.simplify(f)
    # ap = []
    # for child in f:a
    #   if child.kind() == spot.op_ap:
    #     ap.append(spot.formula_F(child))
    
    # f = spot.formula_Or([child for child in f if child.kind() != spot.op_ap])
    # print(f)
    nonsense_bc = []
    for child_i in f:
      if child_i.kind() == spot.op_F:
        nonsense_bc.append(spot.formula_Or([child if child != child_i else child[0] for child in f]))
    return nonsense_bc
        
    

