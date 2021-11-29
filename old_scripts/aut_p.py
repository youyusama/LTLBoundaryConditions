import sys
sys.path.append('/usr/local/lib/python3.8/site-packages')
import spot
import buddy

a1 = spot.translate('!(GXp & F!p)', 'sbacc')
a2 = spot.translate('GXp', 'sbacc')
# print(a1.check())
# emptiness_check(a1)

def cus_product(negG_aut, gi_aut):
  bdict = negG_aut.get_dict()
  if gi_aut.get_dict() != bdict:
    raise RuntimeError("automata should share their dictionary")
      
  result = spot.make_twa_graph(bdict)
  result.copy_ap_of(negG_aut)
  result.copy_ap_of(gi_aut)

  sdict = {}
  todo = []
  def dst(ls, rs):
    pair = (ls, rs)
    p = sdict.get(pair)
    if p is None:
      p = result.new_state()
      sdict[pair] = p
      todo.append((ls, rs, p))
    return p

  result.set_init_state(dst(negG_aut.get_init_state_number(), gi_aut.get_init_state_number()))
  result.set_buchi()
  result.prop_state_acc(True)

  # while todo:
  #   lsrc, rsrc, osrc = todo.pop()
  #   for lt in negG_aut.out(lsrc):
  #     for rt in gi_aut.out(rsrc):
  #       if negG_aut.state_is_accepting(lsrc) and negG_aut.state_is_accepting(lt.dst):
  #         if lt.cond == buddy.bddtrue:
  #           cond = lt.cond
  #         else:
  #           cond = lt.cond | rt.cond
  #       else:
  #         cond = lt.cond & rt.cond
  #       if cond != buddy.bddfalse:
  #         if negG_aut.state_is_accepting(lsrc) and gi_aut.state_is_accepting(rsrc):
  #           result.new_edge(osrc, dst(lt.dst, rt.dst), cond, [0])
  #         else:
  #           result.new_edge(osrc, dst(lt.dst, rt.dst), cond)
  while todo:
    lsrc, rsrc, osrc = todo.pop()
    if negG_aut.state_is_accepting(lsrc):
      for lt in negG_aut.out(lsrc):
        result.new_edge(osrc, osrc, lt.cond, [0])
      continue
    for lt in negG_aut.out(lsrc):
      for rt in gi_aut.out(rsrc):
        cond = lt.cond & rt.cond
        if cond != buddy.bddfalse:
          if negG_aut.state_is_accepting(lsrc) and gi_aut.state_is_accepting(rsrc):
            result.new_edge(osrc, dst(lt.dst, rt.dst), cond, [0])
          else:
            result.new_edge(osrc, dst(lt.dst, rt.dst), cond)
        # else:
        #   result.new_edge(osrc, dst(lt.dst, rt.dst), cond)

  
  # result.merge_states()
  # result.merge_edges()
  # result.purge_dead_states()
  return result

def negG_p(negG_f, gi_f):
  if type(negG_f) is str:
    negG_aut = spot.translate(negG_f, 'ba', 'det')
  else:
    negG_aut = negG_f
  gi_aut = spot.translate(gi_f, 'ba', 'det')
  # print(negG_aut.to_str())

  negG_filter_gi = cus_product(negG_aut, gi_aut)

  print(negG_filter_gi.to_str())

  return negG_filter_gi
  
# finalG = negG_p('!(G(h->Xp) & G(m->X!p))','G(h->Xp)')
# finalG = negG_p(finalG, 'G(m->X!p)')

# finalG = negG_p('!(G(h->Xp) & G(m->X!p) & G((p&Xp)->XX!h)) ','G(h->Xp)')
# finalG = negG_p(finalG, 'G(m->X!p)')
# finalG = negG_p(finalG, 'G((p&Xp)->XX!h)')

# finalG = negG_p('!(GXp & F!p)','GXp')
# finalG = negG_p(finalG, 'F!p')

# finalG = negG_p('!( G(q->s) & G(r->G!s) & G(p->Fq))','G(q->s)')
# finalG = negG_p(finalG, ' G(r->G!s)')
# finalG = negG_p(finalG, 'G(p->Fq)')

# finalG = negG_p('!([] (ta <-> X(tc)) &[] (X(cc) -> ca && go)&[] (ta -> !go)& [] (tc -> !cc)) ','[] (ta <-> X(tc))')
# finalG = negG_p(finalG, ' [] (X(cc) -> ca && go)')
# finalG = negG_p(finalG, '[] (ta -> !go)')
# finalG = negG_p(finalG, '[] (tc -> !cc)')

# finalG = negG_p('!( G (c  -> (c  U (o || d)) ) & \
#                 G (c  ->  (c  U (f || d)) ) & \
#                 G (!o || !f) & \
#                 G (!o || !c) & \
#                 G (!c || !f)  )','G (c  -> (c  U (o || d)))')
# finalG = negG_p(finalG, ' G (c  ->  (c  U (f || d)) )')
# finalG = negG_p(finalG, 'G (!o || !f)')
# finalG = negG_p(finalG, 'G (!o || !c)')
# finalG = negG_p(finalG, 'G (!c || !f)')

# finalG = negG_p('!( [] (q -> p) & [] (p -> <>(q)) )','[] (q -> p)')
# finalG = negG_p(finalG, ' [] (p -> <>(q))')

# finalG = negG_p('!( [] (delivered -> (!send U ack))& [](send -> (!ack U delivered)) )','[] (delivered -> (!send U ack))')
# finalG = negG_p(finalG, ' [](send -> (!ack U delivered))')

# finalG = negG_p('!( [] ( X(open) -> atf) & [](call -> <>(open)) )','[](call -> <>(open))')
# finalG = negG_p(finalG, ' [] ( X(open) -> atf)')

# finalG = negG_p('!( [](l -> <>(! l)) & []((! p) -> ((! m) && X(l))) & []((p && ! l) -> m))','[](l -> <>(! l))')
# finalG = negG_p(finalG, ' []((! p) -> ((! m) && X(l)))')
# finalG = negG_p(finalG, '[]((p && ! l) -> m)')

# finalG = negG_p('!( [](a -> m) & []((c && (! n)) -> (! d)) & []((! n) -> (! i)) & []((c && m && n) -> d) & []((! h) -> (! n)) )','[](a -> m)')
# finalG = negG_p(finalG, ' []((c && (! n)) -> (! d))')
# finalG = negG_p(finalG, '[]((! n) -> (! i))')
# finalG = negG_p(finalG, '[]((c && m && n) -> d)')
# finalG = negG_p(finalG, '[]((! h) -> (! n))')

# finalG = negG_p('!( [] (p -> (q W s))& [] (q -> r) )','[] (p -> (q W s))')
# finalG = negG_p(finalG, ' [] (q -> r)')

# finalG.save('output.dot').save('output.dot', format='dot')

# print(spot.product_or(spot.translate('!(GXp & F!p)'), spot.translate('GXp')).to_str())

def custom_product(negG_aut, g_aut):
  bdict = negG_aut.get_dict()
  if g_aut.get_dict() != bdict:
    raise RuntimeError("automata should share their dictionary")   
  result = spot.make_twa_graph(bdict)
  result.copy_ap_of(negG_aut)
  result.copy_ap_of(g_aut)
  sdict = {}
  todo = []
  def dst(ls, rs):
    pair = (ls, rs)
    p = sdict.get(pair)
    if p is None:
      p = result.new_state()
      sdict[pair] = p
      todo.append((ls, rs, p))
    return p
  result.set_init_state(dst(negG_aut.get_init_state_number(), g_aut.get_init_state_number()))
  result.set_buchi()
  result.prop_state_acc(True)

  new_dead_states = []
  while todo:
    lsrc, rsrc, osrc = todo.pop()
    if negG_aut.state_is_accepting(lsrc):
      # print('left',lsrc, 'osrc', osrc)
      # for lt in negG_aut.out(lsrc):
      #   print(spot.bdd_format_formula(bdict,lt.cond))
      # print('right',rsrc)
      # for rt in g_aut.out(rsrc):
      #   print(spot.bdd_format_formula(bdict,rt.cond))
      
      for lt in negG_aut.out(lsrc):
        for rt in g_aut.out(rsrc):
          result.new_edge(osrc, osrc, lt.cond, [0])
          # print('state ', osrc, 'contradiction')
          # print(spot.bdd_format_formula(bdict,rt.cond))
      continue
    
    for lt in negG_aut.out(lsrc):
      for rt in g_aut.out(rsrc):
        cond = lt.cond & rt.cond
        if cond != buddy.bddfalse:
          result.new_edge(osrc, dst(lt.dst, rt.dst), cond)


  result.merge_states()
  result.merge_edges()
  result.purge_dead_states()
  return result


def filter_ngd(ngd_aut, goals):
  for goal in goals:
    # print('---')
    goal_aut = spot.translate(goal, 'ba', 'det')
    ngd_aut = custom_product(ngd_aut, goal_aut)

  ngd_has_acc = False
  for s in range(0, ngd_aut.num_states()):
    if ngd_aut.state_is_accepting(s):
      ngd_has_acc = True
  if ngd_has_acc:
    print('automata has acc')
  else:
    print('automata has no acc')
  return ngd_aut