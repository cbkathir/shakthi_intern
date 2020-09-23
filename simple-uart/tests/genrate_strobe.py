

"""
Generating th strobe signal for different burst of size and shifting the data based on the strobe signals

WSTRB : Write strobes.
		The WSTRB[n:0] signals when HIGH, specify the byte lanes of the data bus that contain valid information. There
		is one write strobe for each eight bits of the write data bus, therefore WSTRB[n] corresponds to
		WDATA[(8n)+7: (8n)]
		A master must ensure that the write strobes are HIGH only for byte lanes that contain valid data

Start_Address: The start address issued by the master.

Number_Bytes: The maximum number of bytes in each data transfer.

Data_Bus_Bytes: The number of byte lanes in the data bus.

Aligned_Address: The aligned version of the start address.

len_of_burst: The total number of data transfers within a burst.

ru(Upper_Byte_Lane): The byte lane of the lowest addressed byte of a transfer.

rl(Lower_Byte_Lane): The byte lane of the highest addressed byte of a transfer.

"""

Data_Bus_Bytes=8

"""
generating th strobe signal for beat of size 1 byte
"""
def for_size_1_byte(len_of_burst,Start_Address,data):
	y= Start_Address - (8*(int(Start_Address/8)))
	WSTRB=[]
	d=0
	data[0]=data[0]<<(y*8)
	WSTRB.append(pow(2,y))
	if y==7:
		y=0
	else:
		y=y+1
	for x in range(1,len_of_burst):
		d=d+1
		WSTRB.append(pow(2,y))
		data[d]=data[d]<<(y*8)
		y=y+1
		if y>7:
			y=0
	# print(WSTRB)
	# print(data)
	return(WSTRB,data)

"""
generating th strobe signal for beat of size 2 bytes
"""
def for_size_2_bytes(len_of_burst,Start_Address,data):
	Number_Bytes = 2
	Aligned_Address = (int(Start_Address / Number_Bytes) ) * Number_Bytes
	lb = Start_Address - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ub=Aligned_Address + (Number_Bytes - 1) - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ru=(8 * ub) + 7
	rl=(8 * lb)
	WSTRB=[]
	d=0
	t=0
	if Start_Address == Aligned_Address:
		if rl==0:
			WSTRB.append(0b00000011)
			t=0b00001100
		if rl==16:
			WSTRB.append(0b00001100)
			t=0b00110000
		if rl==32:
			WSTRB.append(0b00110000)
			t=0b11000000
		if rl==48:
			WSTRB.append(0b11000000)
			t=0b00000011
	else:
		if rl==8:
			WSTRB.append(0b00000010)
			t=0b00001100
		if rl==24:
			WSTRB.append(0b00001000)
			t=0b00110000
		if rl==40:
			WSTRB.append(0b00100000)
			t=0b11000000
		if rl==56:
			WSTRB.append(0b10000000)
			t=0b00000011
	data[d]=data[d]<<rl
	for x in range(1,len_of_burst):
		WSTRB.append(t)
		d=d+1
		while True:
			if t==0b00000011:
				data[d]=data[d]<<(0)
				t=0b00001100
				break
			if t==0b00001100:
				data[d]=data[d]<<(16)
				t=0b00110000
				break
			if t==0b00110000:
				data[d]=data[d]<<(32)
				t=0b11000000
				break
			if t==0b11000000:
				data[d]=data[d]<<(48)
				t=0b00000011
				break
	# print(WSTRB)
	# print(data)
	return(WSTRB,data)

"""
generating th strobe signal for beat of size 4 bytes
"""
def for_size_4_bytes(len_of_burst,Start_Address,data):
	Number_Bytes = 4
	Aligned_Address = (int(Start_Address / Number_Bytes) ) * Number_Bytes
	lb = Start_Address - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ub=Aligned_Address + (Number_Bytes - 1) - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ru=(8 * ub) + 7
	rl=(8 * lb)
	WSTRB=[]
	d=0
	i=0
	if Start_Address == Aligned_Address:
		if lb==4:
			WSTRB.append(0xf0)
			i=0
		else:
			WSTRB.append(0x0f)
			i=1
	else:
		if lb>3:
			if ru==63 and rl==56:
				WSTRB.append(0b10000000)
			if ru==63 and rl==48:
				WSTRB.append(0b11000000)
			if ru==63 and rl==40:
				WSTRB.append(0b11100000)
			i=0
		else:
			if ru==31 and rl==24:
				WSTRB.append(0b00001000)
			if ru==31 and rl==16:
				WSTRB.append(0b00001100)
			if ru==31 and rl==8:
				WSTRB.append(0b00001110)
			i=1
	data[d]=data[d]<<rl
	for x in range(1,len_of_burst):
		d=d+1
		if i%2 == 0:
			WSTRB.append(0x0f)
			data[d]=data[d]<<0
		else:
			WSTRB.append(0xf0)
			data[d]=data[d]<<32
		i=i+1
			
	# print(WSTRB)
	# print(data)
	return(WSTRB,data)
"""
generating th strobe signal for beat of size 8 bytes
"""
def for_size_8_bytes(len_of_burst,Start_Address):
	Number_Bytes = 8
	Aligned_Address = (int(Start_Address / Number_Bytes) ) * Number_Bytes
	lb = Start_Address - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ub=Aligned_Address + (Number_Bytes - 1) - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ru=(8 * ub) + 7
	rl=(8 * lb)
	WSTRB=[]
	if Start_Address == Aligned_Address:
		WSTRB.append(0xff)
	else:
		if ru==63 and rl==56:
			WSTRB.append(0b10000000)
		if ru==63 and rl==48:
			WSTRB.append(0b11000000)
		if ru==63 and rl==40:
			WSTRB.append(0b11100000)
		if ru==63 and rl==32:
			WSTRB.append(0b11110000)
		if ru==63 and rl==24:
			WSTRB.append(0b11111000)
		if ru==63 and rl==16:
			WSTRB.append(0b11111100)
		if ru==63 and rl==8:
			WSTRB.append(0b11111110)
	for x in range(1,len_of_burst):
		WSTRB.append(0xff)
	# print(WSTRB)
	return(WSTRB)
"""
generating th strobe signal for fixed burst
"""
def for_fixed_burst(len_of_burst,burst_size):
	WSTRB=[]
	t=0
	if burst_size==1:
		t=1
	if burst_size==2:
		t=3
	if burst_size==4:
		t=0x0f
	if burst_size==8:
		t=0xff
	for x in range(len_of_burst):
		WSTRB.append(t)
	# print(WSTRB)
	return(WSTRB)

"""
For wrap burst
"""


Data_Bus_Bytes=8

"""
generating th strobe signal for beat of size 1 byte
"""
def wrap_size_1_byte(len_of_burst,Start_Address,data):
	y= Start_Address - (8*(int(Start_Address/8)))
	Number_Bytes = 1
	total_transfer_size=Number_Bytes*len_of_burst
	Wrap_Boundary = (int(Start_Address / (Number_Bytes * len_of_burst)))*(Number_Bytes * len_of_burst)
	WSTRB=[]
	t=0
	d=0
	if Wrap_Boundary==Start_Address:
		t=1
	data[0]=data[0]<<(y*8)
	WSTRB.append(pow(2,y))
	next_address=Start_Address+1
	if y==7:
		y=0
	else:
		y=y+1
	for x in range(1,len_of_burst):
		if next_address==(Wrap_Boundary+total_transfer_size):
			break	
		d=d+1
		WSTRB.append(pow(2,y))
		next_address=next_address+1
		data[d]=data[d]<<(y*8)
		y=y+1
		if y>7:
			y=0
	if t==0:
		w=Wrap_Boundary- (8*(int(Wrap_Boundary/8)))
		d=d+1
		data[d]=data[d]<<(w*8)
		WSTRB.append(pow(2,w))
		if w==7:
			w=0
		else:
			w=w+1
		for x in range(d+1,len_of_burst):
			d=d+1
			WSTRB.append(pow(2,w))
			data[d]=data[d]<<(w*8)
			w=w+1
			if w>7:
				w=0
	# print(WSTRB)
	# print(data)
	return(WSTRB,data)

"""
generating th strobe signal for beat of size 2 bytes
"""
def wrap_size_2_bytes(len_of_burst,Start_Address,data):
	Number_Bytes = 2
	Aligned_Address = (int(Start_Address / Number_Bytes) ) * Number_Bytes
	lb = Start_Address - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ub=Aligned_Address + (Number_Bytes - 1) - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	total_transfer_size=Number_Bytes*len_of_burst
	Wrap_Boundary = (int(Start_Address / (Number_Bytes * len_of_burst)))*(Number_Bytes * len_of_burst)
	ru=(8 * ub) + 7
	rl=(8 * lb)
	p=0
	if Wrap_Boundary==Start_Address:
		p=1
	WSTRB=[]
	d=0
	t=0
	
	if rl==0:
		WSTRB.append(0b00000011)
		t=0b00001100
	if rl==16:
		WSTRB.append(0b00001100)
		t=0b00110000
	if rl==32:
		WSTRB.append(0b00110000)
		t=0b11000000
	if rl==48:
		WSTRB.append(0b11000000)
		t=0b00000011
	data[d]=data[d]<<rl
	next_address=Start_Address+2
	print('t=%d'%t)
	for x in range(1,len_of_burst):
		if next_address==(Wrap_Boundary+total_transfer_size):
			break
		WSTRB.append(t)
		d=d+1
		next_address=next_address+2
		while True:
			if t==0b00000011:
				data[d]=data[d]<<(0)
				t=0b00001100
				break
			if t==0b00001100:
				data[d]=data[d]<<(16)
				t=0b00110000
				break
			if t==0b00110000:
				data[d]=data[d]<<(32)
				t=0b11000000
				break
			if t==0b11000000:
				data[d]=data[d]<<(48)
				t=0b00000011
				break
	if p==0:
		print('in wrap')
		lb = Wrap_Boundary- ((int(Wrap_Boundary / Data_Bus_Bytes)) * Data_Bus_Bytes)
		ub=Wrap_Boundary + (Number_Bytes - 1) - ((int(Wrap_Boundary / Data_Bus_Bytes)) * Data_Bus_Bytes)
		ru=(8 * ub) + 7
		rl=(8 * lb)
		if rl==0:
			WSTRB.append(0b00000011)
			t=0b00001100
		if rl==16:
			WSTRB.append(0b00001100)
			t=0b00110000
		if rl==32:
			WSTRB.append(0b00110000)
			t=0b11000000
		if rl==48:
			WSTRB.append(0b11000000)
			t=0b00000011
		d=d+1
		data[d]=data[d]<<rl
		for x in range(d+1,len_of_burst):
			WSTRB.append(t)
			d=d+1
			while True:
				if t==0b00000011:
					data[d]=data[d]<<(0)
					t=0b00001100
					break
				if t==0b00001100:
					data[d]=data[d]<<(16)
					t=0b00110000
					break
				if t==0b00110000:
					data[d]=data[d]<<(32)
					t=0b11000000
					break
				if t==0b11000000:
					data[d]=data[d]<<(48)
					t=0b000000111
					break	
	# print(WSTRB)
	# print(data)
	return(WSTRB,data)

"""
generating th strobe signal for beat of size 4 bytes
"""
def wrap_size_4_bytes(len_of_burst,Start_Address,data):
	Number_Bytes = 4
	Aligned_Address = (int(Start_Address / Number_Bytes) ) * Number_Bytes
	lb = Start_Address - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ub=Aligned_Address + (Number_Bytes - 1) - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	total_transfer_size=Number_Bytes*len_of_burst
	Wrap_Boundary = (int(Start_Address / (Number_Bytes * len_of_burst)))*(Number_Bytes * len_of_burst)
	ru=(8 * ub) + 7
	rl=(8 * lb)
	WSTRB=[]
	p=0
	d=0
	i=0
	if Wrap_Boundary==Start_Address:
		p=1
	if lb==4:
		WSTRB.append(0xf0)
		i=0
	else:
		WSTRB.append(0x0f)
		i=1
	data[d]=data[d]<<rl
	next_address=Start_Address+4
	for x in range(1,len_of_burst):
		if next_address==(Wrap_Boundary+total_transfer_size):
			break
		d=d+1
		if i%2 == 0:
			WSTRB.append(0x0f)
			data[d]=data[d]<<0
		else:
			WSTRB.append(0xf0)
			data[d]=data[d]<<32
		i=i+1
		next_address=next_address+4
	if p==0:
		print('in wrap')
		lb = Wrap_Boundary- ((int(Wrap_Boundary / Data_Bus_Bytes)) * Data_Bus_Bytes)
		rl=(8 * lb)
		i=0
		if lb==4:
			WSTRB.append(0xf0)
			i=0
		else:
			WSTRB.append(0x0f)
			i=1
		d=d+1
		data[d]=data[d]<<rl
		for x in range(d+1,len_of_burst):
			d=d+1
			if i%2 == 0:
				WSTRB.append(0x0f)
				data[d]=data[d]<<0
			else:
				WSTRB.append(0xf0)
				data[d]=data[d]<<32
			i=i+1
			
	# print(WSTRB)
	# print(data)
	return(WSTRB,data)
"""
generating th strobe signal for beat of size 8 bytes
"""
def wrap_size_8_bytes(len_of_burst,Start_Address):
	Number_Bytes = 8
	Aligned_Address = (int(Start_Address / Number_Bytes) ) * Number_Bytes
	lb = Start_Address - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ub=Aligned_Address + (Number_Bytes - 1) - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ru=(8 * ub) + 7
	rl=(8 * lb)
	WSTRB=[]
	for x in range(len_of_burst):
		WSTRB.append(0xff)
	# print(WSTRB)
	return(WSTRB)


