import cocotb
from cocotb.triggers import RisingEdge, ReadOnly, Lock ,NextTimeStep
from cocotb.drivers import BusDriver
from cocotb.result import ReturnValue
from cocotb.binary import BinaryValue
import logging

class AXI4_master(BusDriver):
	#AXI4_MASTER_INTERFACE_WITH_UART#

	_signals = ["AWVALID", "AWADDR", "AWREADY","AWSIZE","AWPROT","AWLEN","AWBURST","AWID",
				"WVALID", "WREADY", "WDATA", "WSTRB","WLAST","WID",
				"BVALID", "BREADY", "BRESP", "BID",
				"ARVALID", "ARADDR", "ARREADY","ARSIZE","ARPROT","ARLEN","ARBURST","ARID",
				"RVALID", "RREADY", "RRESP", "RDATA","RLAST","RID"] 
	def __init__(self, entity, name, clock):
		BusDriver.__init__(self, entity, name, clock)
		self.bus.AWVALID.setimmediatevalue(0)
		self.bus.WVALID.setimmediatevalue(0)
		self.bus.ARVALID.setimmediatevalue(0)
		self.bus.BREADY.setimmediatevalue(0)
		self.bus.RREADY.setimmediatevalue(0)
		#doubt whether we can use setimmediate value for signals greater than 1bit
		self.bus.AWADDR <= 0
		self.bus.AWSIZE <= 0
		self.bus.AWPROT <= 0
		self.bus.AWLEN <= 0
		self.bus.AWBURST <= 0

		self.bus.AWID <= 0
		self.bus.WDATA <= 0
		self.bus.WSTRB <= 0
		self.bus.WLAST <= 0
		self.bus.WID <= 0

		self.bus.ARVALID <= 0
		self.bus.ARADDR <= 0
		self.bus.ARSIZE <= 0
		self.bus.ARPROT <= 0
		self.bus.ARLEN <= 0

		self.bus.ARBURST <= 0
		self.bus.ARID <= 0
		self.bus.RREADY <= 0

	@cocotb.coroutine
	def _send_write_address(self,_AWADDR,_AWID,_AWPROT,_AWLEN,_AWSIZE,_AWBURST):
		#sending write address#
		yield RisingEdge(self.clock)
		while True:
			yield RisingEdge(self.clock)
			if self.bus.AWREADY.value:
				break
		self.bus.AWADDR <= _AWADDR
		self.bus.AWID <= _AWID
		self.bus.AWPROT <= _AWPROT
		
		"""
		AWLEN signal specifies the number of data transfers that occur within each
		burst
		Burst_Length = AWLEN[3:0] + 1
		"""
		if _AWLEN <=256:
			self.bus.AWLEN <= _AWLEN - 1
			self.log.info("_AWLEN = %d" %_AWLEN)
		else:
			self.log.debug("number of data transfers that occur within each burst is greater than the limit(256)")
		
		"""
		AWSIZE signal specifies the maximum number of data
		bytes to transfer in each beat, or data transfer, within a burst
		"""
		for x in range(8):
			if pow(2,x) == _AWSIZE:
				self.bus.AWSIZE <= x
				break
			# else:
			# 	self.log.debug("the maximum number of data bytes to transfer in each beat, or data transfer, within a burst is greater than the limit of 128 bytes")
		
		"""
		AXI protocol defines three main burst types FIXED,INCR,WRAP,optional = Reserved
		"""
		if _AWBURST == "FIXED":
			self.bus.AWBURST <= 0b00
		elif _AWBURST == "INCR":
			self.bus.AWBURST <= 0b01
		elif _AWBURST == "WRAP":
			self.bus.AWBURST <= 0b10
		elif _AWBURST == "Reserved":
			self.bus.AWBURST <= 0b11
		
		self.bus.AWVALID <= 1

	@cocotb.coroutine
	def _send_write_data(self,_WDATA,_WID,_WSTRB,_WLAST):
		#sending write data#
		# yield RisingEdge(self.clock)
		while True:
			yield RisingEdge(self.clock)
			if self.bus.WREADY.value:
				break
		self.bus.WVALID <= 1
		self.bus.WDATA <= _WDATA
		self.bus.WID <= _WID
		self.bus.WSTRB <= _WSTRB
		self.bus.WLAST <= int(_WLAST)
		
		
	
	@cocotb.coroutine
	def _get_write_response(self):
		# write response#
		# while True:
		# 	yield RisingEdge(self.clock)
		# 	if int(self.bus.BVALID) == 0:	
		# 		self.bus.BREADY <= 1
		# 		break
		self.bus.BREADY <= 1
		while True:
			yield RisingEdge(self.clock)
			if self.bus.BVALID.value:
				break
		
		
		_BRESP= self.bus.BRESP
		raise ReturnValue(_BRESP)

	@cocotb.coroutine
	def _send_Read_address(self,_ARADDR,_ARID,_ARPROT,_ARLEN,_ARSIZE,_ARBURST):
		#sending write address#
		yield RisingEdge(self.clock)
		while True:
			yield RisingEdge(self.clock)
			if self.bus.ARREADY.value:
				break
		
		self.bus.ARADDR <= _ARADDR
		self.bus.ARID <= _ARID
		self.bus.ARPROT <= _ARPROT
		

		"""
		ARLEN signal specifies the exact number of transfers in a burst. This
		information determines the number of data transfers associated with the address
		Burst_Length = ARLEN[3:0] + 1
		"""
		if _ARLEN <= 256:
			self.log.info("_ARLEN = %d" %_ARLEN)
			self.bus.ARLEN <= _ARLEN - 1
		else:
			self.log.debug("number of data transfers that occur within each burst is greater than the limit(256)")
		
		"""
		ARSIZE signal specifies the maximum number of data
		bytes to transfer in each beat, or data transfer, within a burst
		"""
		for x in range(8):
			if pow(2,x) == _ARSIZE:
				self.bus.ARSIZE <= x
			# else:
			# 	self.log.debug("the maximum number of data bytes to transfer in each beat, or data transfer, within a burst is greater than the limit of 128 bytes")
		
		"""
		AXI protocol defines three main burst types FIXED,INCR,WRAP,optional = Reserved
		"""
		if _ARBURST == "FIXED":
			self.bus.ARBURST <= 0b00
		elif _ARBURST == "INCR":
			self.bus.ARBURST <= 0b01
		elif _ARBURST == "WRAP":
			self.bus.ARBURST <= 0b10
		elif _ARBURST == "Reserved":
			self.bus.ARBURST <= 0b11
		
		self.bus.ARVALID <= 1
		


	@cocotb.coroutine
	def _get_Read_data(self):
		# write response#
		# yield RisingEdge(self.clock)
		while True:
			yield RisingEdge(self.clock)
			if self.bus.RVALID.value:
				break
		
		self.bus.RREADY <= 1
		_RDATA= self.bus.RDATA
		raise ReturnValue(_RDATA)

		

	@cocotb.coroutine
	def _reset_handshaking_signals(self):
		yield RisingEdge(self.clock)
		self.bus.AWVALID <= 0
		self.bus.WVALID <= 0
		self.bus.BREADY <= 0
		self.bus.ARVALID <= 0






	 
		

		



