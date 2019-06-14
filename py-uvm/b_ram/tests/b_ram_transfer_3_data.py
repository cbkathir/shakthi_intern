import os
import sys
import cocotb
import logging
from cocotb.result import TestFailure
from cocotb.result import TestSuccess
from cocotb.clock import Clock
from cocotb.triggers import Timer , RisingEdge
from AXI4_MASTER_Driver import AXI4_master
import uart_predefined_signals as up

CLK_PERIOD = 10
def setup_dut(dut):
	cocotb.fork(Clock(dut.CLK, CLK_PERIOD).start())
"""
address = address of the first transfer in a write burst transaction in uart case
Baudreg = 0x20000
rxreg = 0x20004
txreg = 0x20008
statusreg = 0x2000c

no_of_beats_in_burst = the exact number of transfers or beats in a burst . 
in uart case
1)for Baudreg the value is 1
2)for rxreg,txreg the values are 1,2,3 

size_of_beat_in_bytes = the size(in bytes) of each transfer or beats in the burst.
in case uart
 BaudReg      2 bytes(16-bit) Register to change the baud-value of the UART.
 RxReg        1 byte (8-bit) register to read the incoming value.
 TxReg        1 byte (8-bit) register to be written to send data out.
 StatusReg    The 4-bit register capturing the status of the rx/tx user side FIFOs  (doubt ????)

data = the data to be written on the memory

last_beat_of_burst= True (indicates the last transfer in a write burst)
				  = False (indicates the not last transfer in a write burst)

"""

@cocotb.test(skip = False)
def write_read(dut):
	setup_dut(dut)
	axim = AXI4_master(dut, None, dut.CLK)
	
	dut.RST_N <= 0
	yield Timer(CLK_PERIOD * 10)
	dut.RST_N <= 1
	# yield Timer(CLK_PERIOD)
	
	"""
	setting the Baudrate (0x20000) = 0
	"""
	address = 0x20000
	no_of_beats_in_burst = 1 
	size_of_beat_in_bytes = 2
	

	yield axim._send_write_address(address,up.AxID,up.AxPROT,no_of_beats_in_burst,size_of_beat_in_bytes,up.burst_type)
	dut.log.info("Baudreg address was read by slave")

	
	data = 0x0000
	last_beat_of_burst = True
	
	yield axim._send_write_data(data,up.WID,up.Baud_WSTRB,last_beat_of_burst)
	dut.log.info("Baudreg data was read by slave")
	yield Timer(CLK_PERIOD * 50)

	_BRESP = yield axim._get_write_response()
	dut.log.info("the value of BRESP for Baudreg = %s" %_BRESP)
	yield Timer(CLK_PERIOD * 10)
	"""
	reading back the data from the Baud reg
	"""
	
	address = 0x20000
	no_of_beats_in_burst = 1 
	size_of_beat_in_bytes = 2

	yield axim._send_Read_address(address,up.ARID,up.AxPROT,no_of_beats_in_burst,size_of_beat_in_bytes,up.burst_type)
	dut.log.info("Read address was read by slave")

	_RDATA=yield axim._get_Read_data()
	if int(str(_RDATA)[0:16] , 2) == int(data) :
		dut.log.info("the value of Baudreg = %d" %int(str(_RDATA)[0:16] , 2))	
	else:
		raise TestFailure("Data read form the Baudreg is incorrect %d "%int(str(_RDATA)[0:16] , 2))

	yield axim._reset_handshaking_signals()
	dut.WLAST <= 0
	yield Timer(CLK_PERIOD * 50)
	"""
	1st data transfer
	settting Rxreg(0x20004) = 'a'
	"""
	t_data='abc'
	address = 0x20004
	no_of_beats_in_burst = 3 
	size_of_beat_in_bytes = 1
	yield axim._send_write_address(address,up.AxID,up.AxPROT,no_of_beats_in_burst,size_of_beat_in_bytes,up.burst_type)
	dut.log.info("Rxreg(0x20004) address was read by slave")


	data = ord(t_data[0])
	last_beat_of_burst = False

	yield axim._send_write_data(data,up.WID,up.Tx_Rx_WSTRB,last_beat_of_burst)
	dut.log.info("Data of 1st data_transfer of the burst was read by slave")
	yield Timer(CLK_PERIOD * 50)
	# _BRESP = yield axim._get_write_response()
	# dut.log.info("the value of BRESP for Data of 1st data_transfer of the burst = %s" %_BRESP)

	yield axim._reset_handshaking_signals()
	yield Timer(CLK_PERIOD * 200)
	print("reset done")
	# """
	# 2nd data transfer
	# settting Rxreg(0x20004) = 'b'
	# """
	
	data = ord(t_data[1])
	last_beat_of_burst = False

	yield axim._send_write_data(data,up.WID,up.Tx_Rx_WSTRB,last_beat_of_burst)
	dut.log.info("Data of 2nd data_transfer of the burst was read by slave")
	yield Timer(CLK_PERIOD * 50)

	# _BRESP = yield axim._get_write_response()
	# dut.log.info("the value of BRESP for Data of 2nd data_transfer of the burst = %s" %_BRESP)

	yield axim._reset_handshaking_signals()
	yield Timer(CLK_PERIOD * 200)

	"""
	3rd data transfer
	settting Rxreg(0x20004) = 'c'
	"""
	
	data = ord(t_data[2])
	last_beat_of_burst = True

	yield axim._send_write_data(data,up.WID,up.Tx_Rx_WSTRB,last_beat_of_burst)
	dut.log.info("Data of 3rd data_transfer of the burst was read by slave")
	yield Timer(CLK_PERIOD * 50)

	_BRESP = yield axim._get_write_response()
	dut.log.info("the value of BRESP for Data of 3rd data_transfer of the burst = %s" %_BRESP)


	yield axim._reset_handshaking_signals()
	yield Timer(CLK_PERIOD * 200)

	"""
	reading back the data from the Txreg
	"""
	
	address = 0x20008
	no_of_beats_in_burst = 3 
	size_of_beat_in_bytes = 1

	yield axim._send_Read_address(address,up.ARID,up.AxPROT,no_of_beats_in_burst,size_of_beat_in_bytes,up.burst_type)
	dut.log.info("Txreg address was read by slave")
	i=0
	while True:
		_RDATA=yield axim._get_Read_data()
		
		if chr(int((str(_RDATA)[0:8]) , 2)) == t_data[i] :
			dut.log.info("the value of data = %c" %chr(int((str(_RDATA)[0:8]) , 2)))	
		else:
			raise TestFailure("Data read is incorrect %d "%int((str(_RDATA)[0:8]) , 2))
		i=i+1

		if int(dut.RLAST)==1:
			break
