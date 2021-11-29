import io
RESULT_PATH = 'case_result/'

def get_bc_by_quick_solution(gc):
  BCg, BCs, gt, et = gc.quickSolution()
  all_bc = 0
  cover_bc = 0
  for bc in BCs:
    for gene_bc in gc.gen_t_bc:
      if not gc.isBC(gene_bc):
        print('fuck')
      all_bc += 1
      if gc.isWitness(bc, gene_bc) and not gc.isWitness(gene_bc, bc):
        cover_bc += 1
      else:
        print(gene_bc.to_str())

  output_file = io.open(RESULT_PATH+gc.name+'_quick_solution.txt', 'w+', encoding = 'utf-8')
  output_file.write('case name: ' + gc.name + '\n')
  output_file.write('solved bc num: ' + str(len(BCg)) + '\n')
  output_file.write('bc solving time: ' + str(gt) + '\n')
  for bc in BCg:
    output_file.write(' - ' + bc.to_str() + '\n')
  output_file.write('\n')
  output_file.write('contrastive bc num: ' + str(len(BCs)) + '\n')
  output_file.write('bc evaluation time: ' + str(et) + '\n')
  for bc in BCs:
    output_file.write(' - ' + bc.to_str() + '\n')
  output_file.write('cover rate: ' + str(cover_bc/all_bc if all_bc != 0 else 0) + '\n')