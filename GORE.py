import sys

from spot.impl import formula
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
from ltl_sat_check import sat_check
import time

class GoreCase:
  def __init__(self, name, doms, goals, bcs):
    self.name = name
    self.doms = [spot.formula(dom) for dom in doms] if len(doms) > 0 else []
    self.goals = [spot.formula(goal) for goal in goals]
    self.gen_t_bc = [spot.formula(bc) for bc in bcs] if len(bcs) > 0 else []


  def showdg(self):
    print(spot.formula_And(self.doms+self.goals).to_str())


  def ngd_aut(self):
    return spot.translate(spot.formula_Not(spot.formula_And(self.goals + self.doms)), 'ba', 'det')

  def dandng_aut(self):
    return spot.translate(spot.formula_And([spot.formula_Not(spot.formula_And(self.goals))] + self.doms), 'ba', 'det')

  def dproperties_and_goals(self):
    return self.doms + self.goals


  def isBC_t(self, bc, no_relation_gi):
    if type(bc) is str:
      bc = spot.formula(bc)

    #logical incosistency
    if sat_check(spot.formula_And(self.doms + self.goals + [bc,]).to_str('spin')):
      return -1
    else:
    #minimality
      no_relation_g = []
      for i in range(len(self.goals)):
        if i in no_relation_gi:
          no_relation_g.append(self.goals[i])

      for i in range(len(self.goals)):
        if i in no_relation_gi:
          continue
        if not sat_check(spot.formula_And(self.doms + [goal for goal in self.goals if goal != self.goals[i] and goal not in no_relation_g] + [bc,]).to_str('spin')):
          return i
    return -2


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
            print(i, self.goals[i].to_str())
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
    # if self.isGeneral(bc1, bc2):
    #   print('just genral')
    #   return False
    if not self.isBC(spot.formula_And([bc2, spot.formula_Not(bc1)])):
      return True
    else:
      return False


  def its_impossible(self):
    for i in range(len(self.goals)):
      if not sat_check( spot.formula_And( self.doms + [goal if goal != self.goals[i] else spot.formula_Not(goal) for goal in self.goals ] ).to_str('spin') ):
        print('why')
        print(str(i), self.goals[i].to_str())


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
    # start = time.time()
    f = spot.formula_Not(spot.formula_And(self.goals))
    sim_option = spot.tl_simplifier_options()
    sim_option.reduce_basics = False
    sim = spot.tl_simplifier(sim_option)
    f = sim.simplify(f)
    f = spot.unabbreviate(f, "GFMW^ie")
    print(f.to_str())

    nonsense_bc = []
    for child_i in f:
      if child_i.kind() == spot.op_F:
        nonsense_bc.append(spot.formula_Or([child if child != child_i else child[0] for child in f]))
        nonsense_bc.append(spot.formula_Or([child if child != child_i else spot.formula_X(child[0]) for child in f]))
    # print('get nonsense in: ' + str(time.time()-start))
    return nonsense_bc
        
  
  

  def quickSolution(self):
    start_time = time.time()
    BCs = []
    for goal_i in self.goals:
      G_minusi = spot.formula_And([g for g in self.goals if g != goal_i])
      
      sim_option = spot.tl_simplifier_options()
      sim_option.reduce_basics = False
      sim = spot.tl_simplifier(sim_option)
      regular_goal_i = sim.simplify(spot.formula_Not(goal_i))
      regular_goal_i = spot.unabbreviate(regular_goal_i, "FMW^ie")
      # print(regular_goal_i.to_str())

      all_ap = spot.atomic_prop_collect(spot.formula_And(self.doms+self.goals))
      gi_ap = spot.atomic_prop_collect(goal_i)
      none_relation_ap = [ap for ap in all_ap if ap not in gi_ap]

      # special case
      special_cases = []
      if regular_goal_i.kind() == spot.op_ap:
        for ap in none_relation_ap:
          special_cases.append(spot.formula_And([regular_goal_i,ap]))
      elif regular_goal_i.kind() == spot.op_tt:
        for ap in none_relation_ap:
          special_cases.append(spot.formula_And([regular_goal_i,ap]))
      elif regular_goal_i.kind() == spot.op_Not:
        for ap in none_relation_ap:
          special_cases.append(spot.formula_And([regular_goal_i,ap]))
      elif regular_goal_i.kind() == spot.op_And:
        for ap in none_relation_ap:
          special_cases.append(spot.formula_And([regular_goal_i,ap]))
      elif regular_goal_i.kind() == spot.op_G:
        for ap in none_relation_ap:
          special_cases.append(spot.formula_And([regular_goal_i,ap]))
      elif regular_goal_i.kind() == spot.op_Or:
        a = regular_goal_i[0]
        b = regular_goal_i[1]
        special_cases = [a,b]
      elif regular_goal_i.kind() == spot.op_X:
        for ap in none_relation_ap:
          special_cases.append(spot.formula_And([regular_goal_i,ap]))
      elif regular_goal_i.kind() == spot.op_R:
        a = regular_goal_i[0]
        b = regular_goal_i[1]
        special_cases = [a,spot.formula_And([b,spot.formula_X(a)])]
      elif regular_goal_i.kind() == spot.op_U:
        a = regular_goal_i[0]
        b = regular_goal_i[1]
        special_cases = [b,spot.formula_And([a,spot.formula_X(b)])]
      else:
        continue

      # check sc
      for sc in special_cases:
        f = spot.formula_And([sc, G_minusi] + self.doms).to_str()
        pbc = spot.formula_Or([sc, spot.formula_Not(G_minusi)])
        if sat_check(f):
          BCs.append(pbc)
        
    gen_time = time.time()
    # for bc in BCs:
    #   print(bc.to_str())
    #   print(self.isBC(bc))
    BCs_real = []
    for bc in BCs:
      if self.isBC(bc):
        BCs_real.append(bc)

    BCg = BCs_real.copy()

    for bc in BCs_real:
      if not self.isBC(bc):
        BCs_real.remove(bc)
      for bc1 in BCs_real:
        if bc != bc1:
          a = self.isWitness(bc, bc1)
          b = self.isWitness(bc1, bc)
          if a and b:
            if len(bc.to_str()) < len(bc1.to_str()):
              BCs_real.remove(bc1)
          if a and not b:
            BCs_real.remove(bc1)
    
    # for bc in BCs:
    #   print(bc.to_str())
    return BCg, BCs_real, gen_time-start_time, time.time()-gen_time
