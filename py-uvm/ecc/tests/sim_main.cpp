#include "Vmodule_ecc_encode.h"
#include "verilated.h"
#include "verilated_vpi.h"

      vluint64_t main_time = 0;   // See comments in first example
      double sc_time_stamp () { return main_time; }

   int main(int argc, char** argv, char** env) {
          Verilated::commandArgs(argc, argv);
          Vmodule_ecc_encode* top = new Vmodule_ecc_encode;
          Verilated::internalsDump();  // See scopes to help debug
          while (!Verilated::gotFinish()) {
              top->eval();
              VerilatedVpi::callValueCbs();  // For signal callbacks
          }
          delete top;
          exit(0);
      }
