#include "SpikeIf.hpp"
#include <stdio.h>

int main(){
  char ISA[] = "RV64IMAFD";
  CSpikeIf A = SpawnSpikeIF("/scratch/discard/slsv-master/test_vectors/rv64g-p-tests/rv64ui-p-add",ISA);
  unsigned long long int pc = CgetVariable(A,(4096+32));
  while(pc != 0x80000048 ){
    pc = CgetVariable(A,(4096+32));
//    printf("%llx\n",pc);
    CsingleStep(A);
  }
  DestroySpikeIF(A);
  return 0;
}
