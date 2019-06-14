#include "SpikeIf.hpp"

#include <iostream>
#include <vector>
#include <string>

//
void sim_t::main()  // This is private called somewhere in the start routine and when things need to comm with htif periphrals which we dont care about
{
  step(1);
  //if (remote_bitbang) remote_bitbang->tick();
}

void sim_t::set_log(bool value){
  step(1);
  log = false; // Silence log printing
}

void sim_t::step(size_t n)
{
  //if (remote_bitbang) remote_bitbang->tick(); // This was added here  it is functionally eqv
  for (size_t i = 0, steps = 0; i < n; i += steps)
  {
    steps = std::min(n - i, INTERLEAVE - current_step);
    procs[current_proc]->step(steps);

    current_step += steps;
    if (current_step == INTERLEAVE)
    {
      current_step = 0;
      procs[current_proc]->get_mmu()->yield_load_reservation();
      if (++current_proc == procs.size()) {
        current_proc = 0;
        clint->increment(INTERLEAVE / INSNS_PER_RTC_TICK);
      }
      //host->switch_to(); // This affects the ability of spike to terminate on infinite loops.
      // There are 2 contexts one host target , There is current an error with some sort of improper initialisation
      // which prints an error message when host->switch_to() is called . // figure out that for htif periphral compatibility.
    }
  }
}

void sim_thread_main(void* arg) //  ref:: sim_t ::main()
{
  ((sim_t*)arg)->main();
}

int sim_t::run()  // This method just initialises and loads the binary.
{
  host = context_t::current();
  target.init(sim_thread_main, this);
  htif_t::start();
  return 0;
}

// The SpikeIf Transport Interface module Members defined 
SpikeIf::SpikeIf(){
  std::cout << "Special SLSV Interface Instance Spawned" << std::endl ;
  return;
}
SpikeIf::~SpikeIf() {
  std::cout << "Special SLSV Interface Instance Destroyed" << std::endl ;
  return;
}

bool SpikeIf::destroy_s(){
  if(s != NULL){
    s->stop();
    delete s;
    std::cout << "Special SLSv Sim_t deleted" << std::endl ;
    return true;
  }
  return false;
}

static std::vector<std::pair<reg_t, mem_t*>> make_mems(const char* arg)
{
  // handle legacy mem argument
  char* p;
  auto mb = strtoull(arg, &p, 0);
  if (*p == 0) {
    reg_t size = reg_t(mb) << 20;
    if (size != (size_t)size)
      throw std::runtime_error("Size would overflow size_t");
    return std::vector<std::pair<reg_t, mem_t*>>(1, std::make_pair(reg_t(DRAM_BASE), new mem_t(size)));
  }

  // handle base/size tuples
  std::vector<std::pair<reg_t, mem_t*>> res;
  while (true) {
    auto base = strtoull(arg, &p, 0);
    auto size = strtoull(p + 1, &p, 0);
    res.push_back(std::make_pair(reg_t(base), new mem_t(size)));
    if (!*p)
      break;
    arg = p + 1;
  }
  return res;
}

bool SpikeIf::Initialise(char* ISA) {
  bool debug = false;
  bool halted = false;
  bool histogram = false;
  //bool log = false;
  //bool dump_dts = false;
  size_t nprocs = 1;
  reg_t start_pc = reg_t(-1);
  std::vector<std::pair<reg_t, mem_t*>> mems;
  std::unique_ptr<icache_sim_t> ic;
  std::unique_ptr<dcache_sim_t> dc;
  std::unique_ptr<cache_sim_t> l2;
  std::function<extension_t*()> extension;
  unsigned abstract_rti = 0;
  unsigned dmi_rti = 0;
  const char* isa = "RV64IMAFDC";
  debug_module_config_t dm_config = {
    .progbufsize = 2,
    .max_bus_master_bits = 0,
    .require_authentication = false,
    .abstract_rti = 0,
    .support_hasel = true,
    .support_abstract_csr_access = true,
    .support_haltgroups = true
  };

  if(ISA != NULL){
	  isa = (const char*)ISA;
  }

  uint16_t rbb_port = 0; // Set These Enabled if you want To USE GDB on the monitor additionally.
  bool use_rbb = false;  // Set These Enabled if you want To USE GDB on the monitor additionally.
  
  unsigned progsize = 2;
  unsigned max_bus_master_bits = 0;
  bool require_authentication = false;
  std::vector<int> hartids;

if (mems.empty())
    mems = make_mems("2048"); // Memory Set to 2048 Change this if more is necessary

  std::vector<std::string> htif_args;
  htif_args.push_back(SpikeArguments);

  //htif_args.push_back(SpikeArguments);

  s = new sim_t(isa, nprocs, halted, start_pc, mems, htif_args, std::move(hartids), dm_config);
          //sim_t(isa,_nprocs, halted,start_pc , mems, args     , const std::vector<int> hartids,unsigned progsize, unsigned max_bus_master_bits, bool require_authentication); // Updated interface for new commit
      
  std::unique_ptr<remote_bitbang_t> remote_bitbang((remote_bitbang_t *) NULL);
  std::unique_ptr<jtag_dtm_t> jtag_dtm(new jtag_dtm_t(&s->debug_module, dmi_rti));
  if (use_rbb) {
    remote_bitbang.reset(new remote_bitbang_t(rbb_port, &(*jtag_dtm)));
   s->set_remote_bitbang(&(*remote_bitbang));
  }
  
  for (size_t i = 0; i < nprocs; i++)
  {
    if (ic)s->get_core(i)->get_mmu()->register_memtracer(&*ic);
    if (dc)s->get_core(i)->get_mmu()->register_memtracer(&*dc);
    if (extension)s->get_core(i)->register_extension(extension());
  }

 s->set_debug(debug);
 s->set_histogram(histogram);
  
 s->run(); // Essentially initialises everything :P

 //s->set_log(log); // This is a single step 

  return true;
}


uint32_t SpikeIf::Single_Step() {
	uint32_t event = 0; //ALL_OK; // ref events.hpp	 // ALL OK is Equal to 0
  s->set_log(0);
	return event;
}

void SpikeIf::CSetVariable(uint32_t address,uint64_t val){
  uint32_t hart  = (address & 0xFFFF0000) >>16 ; 
  uint32_t stateid = address & 0x0000FFFF;
  if (hart != 0 )return;
  if (stateid > (4096+65) )return;
  processor_t* HART =s->get_core(hart); // This is where Im locking this down to one core
  //state_t* hartstate = HART->get_state();

	if(stateid<4096){
    HART->set_csr(stateid,val);
  } 
  return;
}

uint64_t SpikeIf::CGetVariable(uint32_t address){
  uint64_t value = 0xAAAAAAAAAAAAAAAA;
  uint32_t hart  = (address & 0xFFFF0000) >>16 ; 
  uint32_t stateid = address & 0x0000FFFF;
  
  //std::cout << hart << stateid << std::endl ;  // debug

  // This CODE is FRAGILE and WILL Break for an INVALID ADDRESS PLEASE 
  // Fragile Interface Safeguard start 
  if (hart != 0 )return value;
  if (stateid > (4096+65) )return value;
  // Fragile Interface Safeguard end 

  processor_t* HART =s->get_core(hart); // This is where Im locking this down to one core
  state_t* hartstate = HART->get_state();

	if(stateid<4096){
    value = HART->get_csr(stateid);
    return value;
  }
  stateid = stateid - 4096;
  if (stateid < 32){
    value = hartstate->XPR[stateid];
  }
  else if(stateid==32)value = hartstate->pc; 
  else if(stateid==65)value = hartstate->prv; 
  else {
     //uint64_t softfloat_cast<float128_t, uint64_t>(const float128_t &v)
    float128_t lv_value = hartstate->FPR[stateid-33];
    value = *(reinterpret_cast<uint64_t*>(&lv_value));
    // the only thing left is FPR as GPR CSR adn PC and FRAGILE take care of everything else
//    value = static_cast<uint64_t>(lv_value);
  }
  return value;
}

void* SpawnSpikeIF(char* String,char* ISA){
  SpikeIf* A = new SpikeIf ;
  ((SpikeIf*)(A))->SpikeArguments = std::string(String);
  ((SpikeIf*)(A))->Initialise(ISA);
  //return reinterpret_cast<void*>(A);
  return (void*)A;
}

void CSetVariable(CSpikeIf instance,uint32_t address,uint64_t val){
  CSpikeIf A = reinterpret_cast<CSpikeIf*>(instance);
  ((SpikeIf*)(A))->CSetVariable(address,val);
  return;
  }

unsigned int CsingleStep(CSpikeIf instance){
  CSpikeIf A = reinterpret_cast<CSpikeIf*>(instance);
  ((SpikeIf*)(A))->Single_Step();
  return 0;
}

unsigned long long int CgetVariable(CSpikeIf instance,unsigned int SLSVaddress){
  CSpikeIf A = reinterpret_cast<CSpikeIf*>(instance);
  return ((SpikeIf*)(A))->CGetVariable(SLSVaddress);
}

void DestroySpikeIF(CSpikeIf instance){
  delete reinterpret_cast<CSpikeIf*>(instance);
  return;
}


