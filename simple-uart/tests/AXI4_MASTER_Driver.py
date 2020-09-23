"""
Driver for AXI4 MASTER
NOTE:we can de-assert the i/p handshaking signals once the handshaking is over 
"""
import cocotb
from cocotb.triggers import RisingEdge, ReadOnly, Lock ,NextTimeStep
from cocotb.drivers import BusDriver
from cocotb.result import TestFailure
from cocotb.result import ReturnValue
from cocotb.binary import BinaryValue
import logging
import math
import genrate_strobe as gs

class AXI4_master(BusDriver):

	_signals = ["AWVALID", "AWADDR", "AWREADY","AWSIZE","AWPROT","AWLEN","AWBURST","AWID",
				"WVALID", "WREADY", "WDATA", "WSTRB","WLAST","WID",
				"BVALID", "BREADY", "BRESP", "BID",
				"ARVALID", "ARADDR", "ARREADY","ARSIZE","ARPROT","ARLEN","ARBURST","ARID",
				"RVALID", "RREADY", "RRESP", "RDATA","RLAST","RID"] 
	def __init__(self, entity, name, clock):
		BusDriver.__init__(self, entity, name, clock)
		"""
		Deasserting the AXI4 signals
		"""
		self.bus.AWVALID.setimmediatevalue(0)
		self.bus.WVALID.setimmediatevalue(0)
		self.bus.ARVALID.setimmediatevalue(0)
		self.bus.BREADY.setimmediatevalue(0)
		self.bus.RREADY.setimmediatevalue(0)
		
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
	def send_write_address(self,_AWADDR,_AWID,_AWPROT,_AWLEN,_AWSIZE,_AWBURST):
		"""
		sending write address to DUT
		"""
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
		else:
			raise TestFailure("number of data transfers that occur within each burst is greater than the limit(256)")
		
		"""
		AWSIZE signal specifies the maximum number of data
		bytes to transfer in each beat, or data transfer, within a burst
		"""
		y=int(math.log(_AWSIZE, 2.0))
		if y>128:
			raise TestFailure("the maximum number of data bytes to transfer in each beat, or data transfer, within a burst is greater than the limit of 128 bytes")
		else:
			self.bus.AWSIZE <= y
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
	def send_write_data(self,_WDATA,_WID,_WSTRB):
		"""
		sending write data to DUT
		"""
		
		n=len(_WDATA)
		self.bus.WID <= _WID
		self.bus.WSTRB <= _WSTRB
		for x in range(n):
			self.bus.WVALID <= 0
			while True:
				yield RisingEdge(self.clock)
				if self.bus.WREADY.value:
					break
			
			self.bus.WDATA <= _WDATA[x]
			if x==n-1:
				self.bus.WLAST <= 1
			else:
				self.bus.WLAST <= 0
			self.bus.WVALID <= 1
		
	
	@cocotb.coroutine
	def get_write_response(self):
		"""
		to recieve the Write response from the DUT
		BRESP = 0b00 (OKAY)
				0b01 (EXOKAY)
				0b10 (SLVERR)
				0b11 (DECERR)
		"""
		
		self.bus.BREADY <= 1
		while True:
			yield RisingEdge(self.clock)
			if self.bus.BVALID.value:
				break
		
		
		_BRESP= self.bus.BRESP
		raise ReturnValue(_BRESP)

	@cocotb.coroutine
	def send_Read_address(self,_ARADDR,_ARID,_ARPROT,_ARLEN,_ARSIZE,_ARBURST):
		"""
		sending Read address to DUT. The read address gives the address of the first transfer in a read burst
		transaction
		"""
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
			self.bus.ARLEN <= _ARLEN - 1
		else:
			raise TestFailure("number of data transfers that occur within each burst is greater than the limit(256)")
		
		"""
		ARSIZE signal specifies the maximum number of data
		bytes to transfer in each beat, or data transfer, within a burst
		"""
		y=int(math.log(_ARSIZE, 2.0))
		if y>128:
			raise TestFailure("the maximum number of data bytes to transfer in each beat, or data transfer, within a burst is greater than the limit of 128 bytes")
		else:
			self.bus.ARSIZE <= y
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
	def get_Read_data(self):
		"""
		To recieve Read data from DUT
		"""
		self.bus.RREADY <= 1
		
		while True:
			yield RisingEdge(self.clock)
			if self.bus.RVALID.value:
				break
		
		_RDATA= self.bus.RDATA
		raise ReturnValue(_RDATA)

	@cocotb.coroutine
	def reset_handshaking_signals(self):
		"""
		De-assertng the master handshaking signals
		"""
		yield RisingEdge(self.clock)
		self.bus.AWVALID <= 0
		self.bus.WVALID <= 0
		self.bus.BREADY <= 0
		self.bus.ARVALID <= 0

	@cocotb.coroutine
	def write_transaction(self,_AWADDR,_AWID,_AWPROT,_AWLEN,_AWSIZE,_AWBURST,DATA,_WID):
		"""
		write transaction in AXI4 , sending write address,write data to DUT and recieving write response from DUT
		"""
		n=len(DATA)
		x=0
		"""
		Generating th strobe signal for different burst of size and shifting the data based on the strobe signals
		"""
		if _AWBURST == "FIXED":
			WSTRB=gs.for_fixed_burst(_AWLEN,_AWSIZE)
			_WDATA=DATA	
		elif _AWBURST == "INCR":
			if _AWSIZE==1:
				WSTRB,_WDATA=gs.for_size_1_byte(_AWLEN,_AWADDR,DATA)
			if _AWSIZE==2:
				WSTRB,_WDATA=gs.for_size_2_bytes(_AWLEN,_AWADDR,DATA)
			if _AWSIZE==4:
				WSTRB,_WDATA=gs.for_size_4_bytes(_AWLEN,_AWADDR,DATA)
			if _AWSIZE==8:
				WSTRB=gs.for_size_8_bytes(_AWLEN,_AWADDR)
				_WDATA=DATA
		elif _AWBURST == "WRAP":
			Aligned_Address = (int(_AWADDR/ _AWSIZE) ) * _AWSIZE
			if _AWADDR==Aligned_Address:
				if _AWLEN==2 or _AWLEN==4 or _AWLEN==8 or _AWLEN==16:
					if _AWSIZE==1:
						WSTRB,_WDATA=gs.wrap_size_1_byte(_AWLEN,_AWADDR,DATA)
					if _AWSIZE==2:
						WSTRB,_WDATA=gs.wrap_size_2_bytes(_AWLEN,_AWADDR,DATA)
					if _AWSIZE==4:
						WSTRB,_WDATA=gs.wrap_size_4_bytes(_AWLEN,_AWADDR,DATA)
					if _AWSIZE==8:
						WSTRB=gs.wrap_size_8_bytes(_AWLEN,_AWADDR)
						_WDATA=DATA
				else:
					raise TestFailure("wrapping burst restriction was not satisfied (length of the burst must be 2, 4, 8, or 16 transfers)") 
			else:
				raise TestFailure("wrapping burst restriction was not satisfied (start address must be aligned to the size of each transfer)")



		while True:
			yield RisingEdge(self.clock)
			if self.bus.AWREADY.value and self.bus.WREADY.value:
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
		else:
			raise TestFailure("number of data transfers that occur within each burst is greater than the limit(256)")
		
		"""
		AWSIZE signal specifies the maximum number of data
		bytes to transfer in each beat, or data transfer, within a burst
		"""
		y=int(math.log(_AWSIZE, 2.0))
		if y>128:
			raise TestFailure("the maximum number of data bytes to transfer in each beat, or data transfer, within a burst is greater than the limit of 128 bytes")
		else:
			self.bus.AWSIZE <= y
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

		self.bus.WID <= _WID
		self.bus.WSTRB <= WSTRB[0]
		self.bus.WDATA <= _WDATA[0]
		print('_WDATA[0] = %d'%_WDATA[0])
		if n== 1:
			self.bus.WLAST <= 1
		else:
			self.bus.WLAST <= 0
			
		self.bus.AWVALID <= 1
		self.bus.WVALID <= 1

		x = x + 1
		while(x < n):			
			self.bus.WID <= _WID
			while True:
				yield RisingEdge(self.clock)
				self.bus.AWVALID <= 0
				if self.bus.WREADY.value:
					break
			
			self.bus.WDATA <= _WDATA[x]
			self.bus.WSTRB <= WSTRB[x]
			if (x == (n-1)):
				self.bus.WLAST <= 1
			else:
				self.bus.WLAST <= 0
			self.bus.WVALID <= 1
			print("_WDATA[%d] = %d" %(x,_WDATA[x]))
			x = x+1

		if x == n:
			yield RisingEdge(self.clock)
			self.bus.AWVALID <= 0
			self.bus.WVALID <= 0
			self.bus.WLAST <= 0
			self.bus.WSTRB <= 0
			
		self.bus.BREADY <= 1
		while True:
			yield RisingEdge(self.clock)
			if self.bus.BVALID.value:
				break
		_BRESP= self.bus.BRESP
		self.bus.BREADY <= 0
		raise ReturnValue(_BRESP)
	
	@cocotb.coroutine
	def read_transaction(self,_ARADDR,_ARID,_ARPROT,_ARLEN,_ARSIZE,_ARBURST):
		"""
		Read transaction in AXI4,sending Read address to DUT and recieving Read data from DUT 
		"""
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
			# self.log.info("_ARLEN = %d" %_ARLEN)
			self.bus.ARLEN <= _ARLEN - 1
		else:
			raise TestFailure("number of data transfers that occur within each burst is greater than the limit(256)")
		
		"""
		ARSIZE signal specifies the maximum number of data
		bytes to transfer in each beat, or data transfer, within a burst
		"""
		y=int(math.log(_ARSIZE, 2.0))
		if y>128:
			raise TestFailure("the maximum number of data bytes to transfer in each beat, or data transfer, within a burst is greater than the limit of 128 bytes")
		else:
			self.bus.ARSIZE <= y
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

		self.bus.RREADY <= 1
		_RDATA=[]
		while True:
			while True:
				yield RisingEdge(self.clock)
				self.bus.ARVALID <= 0
				if self.bus.RVALID.value:
					break
			r = str(self.bus.RDATA)
			_RDATA.append(r)

			if int(self.bus.RLAST)==1:
				self.bus.RREADY <= 0
				break
		raise ReturnValue(_RDATA)