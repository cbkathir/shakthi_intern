/*-------------------------------------------------------------------------------------------------- 
* Copyright (c) 2018, IIT Madras All rights reserved.
* 
* Redistribution and use in source and binary forms, with or without modification, are permitted
* provided that the following conditions are met:
* 
* - Redistributions of source code must retain the below copyright notice, this list of conditions
*   and the following disclaimer.  
* - Redistributions in binary form must reproduce the above copyright notice, this list of 
*   conditions and the following disclaimer in the documentation and/or other materials provided 
*   with the distribution.  
* - Neither the name of IIT Madras  nor the names of its contributors may be used to endorse or 
*   promote products derived from this software without specific prior written permission.
* 
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
* OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
* AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
* CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
* DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
* IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT 
* OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*
* --------------------------------------------------------------------------------------------------
* Author:  Paul George
* Email id: pg456@snu.edu.in
* ------------------------------------------------------------------------------------------------*/
#ifndef Spike_LowOH_Interface
#define Spike_LowOH_Interface

#include <stdio.h>
#include <stdlib.h>

typedef void*  CSpikeIf;

#ifdef __cplusplus
extern "C"  {
#endif
	CSpikeIf SpawnSpikeIF(char* String,char* ISA);
	unsigned int CsingleStep(CSpikeIf instance);
	unsigned long long int CgetVariable(CSpikeIf instance,unsigned int SLSVaddress);
	void DestroySpikeIF(CSpikeIf instance);
#ifdef __cplusplus
}
#endif


// Include File to get directly innto spike
#ifdef __cplusplus

#include "sim.h"
#include "mmu.h"
#include "remote_bitbang.h"
#include "cachesim.h"
#include "extension.h"
#include <dlfcn.h>
#include <fesvr/option_parser.h>

#include <iostream>
#include <vector>
#include <string>
#include <memory>



class SpikeIf{
public:
  // Constructors
  SpikeIf();
	// Destructor
  ~SpikeIf();
	bool destroy_s();	
	bool Initialise(char* ISA);
	uint32_t Single_Step();
	uint64_t CGetVariable(uint32_t address);
	void CSetVariable(uint32_t address,uint64_t val);
  sim_t* s;
	std::string SpikeArguments = "/home/commandpaul/slsv-master/test_vectors/Tests/test0.rv64imafd";
};

#endif

#endif
