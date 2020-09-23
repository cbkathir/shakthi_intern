"""
To retrive back the correct data from the data which has been sent by the DUT after Read transaction
"""
Data_Bus_Bytes = 8

def for_1_byte(Start_Address):
	Number_Bytes = 1
	Aligned_Address = (int(Start_Address / Number_Bytes) ) * Number_Bytes
	lb = Start_Address - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ub=Aligned_Address + (Number_Bytes - 1) - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ru=(8 * ub) + 7
	rl=(8 * lb)
	if ru==7 and rl==0:
		return(56,64)
	if ru==15 and rl==8:
		return(48,56)
	if ru==23 and rl==16:
		return(40,48)
	if ru==31 and rl==24:
		return(32,40)
	if ru==39 and rl==32:
		return(24,32)
	if ru==47 and rl==40:
		return(16,24)
	if ru==55 and rl==48:
		return(8,16)
	if ru==63 and rl==56:
		return(0,8)

def for_2_bytes(Start_Address):
	Number_Bytes = 2
	Aligned_Address = (int(Start_Address / Number_Bytes) ) * Number_Bytes
	lb = Start_Address - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ub=Aligned_Address + (Number_Bytes - 1) - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ru=(8 * ub) + 7
	rl=(8 * lb)
	align=0
	if Start_Address==Aligned_Address:
		align=1
	if ru==15 :
		return(48,64,align)
	if ru==31 :
		return(32,48,align)
	if ru==47 :
		return(16,32,align)
	if ru==63 :
		return(0,16,align)

def for_4_bytes(Start_Address):
	Number_Bytes = 4
	Aligned_Address = (int(Start_Address / Number_Bytes) ) * Number_Bytes
	lb = Start_Address - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ub=Aligned_Address + (Number_Bytes - 1) - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ru=(8 * ub) + 7
	rl=(8 * lb)
	align=0
	if Start_Address==Aligned_Address:
		align=1
	if ru==31 :
		return(32,64,align)
	if ru==63 :
		return(0,32,align)

def for_8_bytes(Start_Address):
	Number_Bytes = 4
	Aligned_Address = (int(Start_Address / Number_Bytes) ) * Number_Bytes
	lb = Start_Address - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ub=Aligned_Address + (Number_Bytes - 1) - ((int(Start_Address / Data_Bus_Bytes)) * Data_Bus_Bytes)
	ru=(8 * ub) + 7
	rl=(8 * lb)
	align=0
	if Start_Address==Aligned_Address:
		align=1
	return(0,64,align)
