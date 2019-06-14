// Copyright (c) 2018 IIT Madras. See IITM_LICENSE.txt file for more details

//
// Generated by Bluespec Compiler, version 2018.10.beta1 (build e1df8052c, 2018-10-17)
//
// On Thu Feb 21 12:44:07 IST 2019
//
//
// Ports:
// Name                         I/O  size props
// ecc_encode                     O     8
// ecc_encode_data_word_in        I    64
//
// Combinational paths from inputs to outputs:
//   ecc_encode_data_word_in -> ecc_encode
//
//

`ifdef BSV_ASSIGNMENT_DELAY
`else
  `define BSV_ASSIGNMENT_DELAY
`endif

`ifdef BSV_POSITIVE_RESET
  `define BSV_RESET_VALUE 1'b1
  `define BSV_RESET_EDGE posedge
`else
  `define BSV_RESET_VALUE 1'b0
  `define BSV_RESET_EDGE negedge
`endif

module module_ecc_encode(ecc_encode_data_word_in,
			 ecc_encode);
  // value method ecc_encode
  input  [63 : 0] ecc_encode_data_word_in;
  output [7 : 0] ecc_encode;

  // signals for module outputs
  wire [7 : 0] ecc_encode;

  // remaining internal signals
  wire [72 : 0] IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELSE_0___d128;
  wire [6 : 0] IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d130,
	       _theResult_____1__h25;
  wire IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d136,
       IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d173,
       IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d350,
       extra_parity_ded__h26,
       y__h1890,
       y__h1891,
       y__h1892,
       y__h1893,
       y__h1894,
       z__h104,
       z__h111,
       z__h118,
       z__h125,
       z__h132,
       z__h139,
       z__h146,
       z__h153,
       z__h160,
       z__h167,
       z__h174,
       z__h181,
       z__h1842,
       z__h1849,
       z__h1856,
       z__h1863,
       z__h1870,
       z__h1877,
       z__h188,
       z__h1884,
       z__h195,
       z__h202,
       z__h209,
       z__h216,
       z__h223,
       z__h230,
       z__h237,
       z__h244,
       z__h251,
       z__h258,
       z__h265,
       z__h272,
       z__h279,
       z__h286,
       z__h293,
       z__h300,
       z__h307,
       z__h314,
       z__h321,
       z__h328,
       z__h335,
       z__h342,
       z__h349,
       z__h356,
       z__h363,
       z__h370,
       z__h377,
       z__h384,
       z__h391,
       z__h398,
       z__h405,
       z__h412,
       z__h419,
       z__h426,
       z__h433,
       z__h440,
       z__h447,
       z__h454,
       z__h461,
       z__h468,
       z__h475,
       z__h48,
       z__h482,
       z__h55,
       z__h62,
       z__h69,
       z__h76,
       z__h83,
       z__h90,
       z__h97;

  // value method ecc_encode
  assign ecc_encode = { extra_parity_ded__h26, _theResult_____1__h25 } ;

  // remaining internal signals
  assign IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d130 =
	     IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELSE_0___d128[1] ?
	       7'd1 :
	       7'd0 ;
  assign IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d136 =
	     IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d130[0] ^
	     IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELSE_0___d128[3] ^
	     ecc_encode_data_word_in[1] ^
	     ecc_encode_data_word_in[3] ^
	     ecc_encode_data_word_in[4] ;
  assign IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d173 =
	     IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d130[1] ^
	     IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELSE_0___d128[2] ^
	     IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELSE_0___d128[3] ^
	     ecc_encode_data_word_in[2] ^
	     ecc_encode_data_word_in[3] ;
  assign IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d350 =
	     IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d130[6] ^
	     ecc_encode_data_word_in[57] ^
	     ecc_encode_data_word_in[58] ^
	     ecc_encode_data_word_in[59] ^
	     ecc_encode_data_word_in[60] ^
	     ecc_encode_data_word_in[61] ^
	     ecc_encode_data_word_in[62] ^
	     ecc_encode_data_word_in[63] ;
  assign IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELSE_0___d128 =
	     ecc_encode_data_word_in[0] ? 73'd8 : 73'd0 ;
  assign _theResult_____1__h25 =
	     { IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d350,
	       y__h1890,
	       y__h1891,
	       y__h1892,
	       y__h1893,
	       y__h1894,
	       z__h1842 } ;
  assign extra_parity_ded__h26 = z__h482 ^ z__h1884 ;
  assign y__h1890 =
	     IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d130[5] ^
	     ecc_encode_data_word_in[26] ^
	     ecc_encode_data_word_in[27] ^
	     ecc_encode_data_word_in[28] ^
	     ecc_encode_data_word_in[29] ^
	     ecc_encode_data_word_in[30] ^
	     ecc_encode_data_word_in[31] ^
	     ecc_encode_data_word_in[32] ^
	     ecc_encode_data_word_in[33] ^
	     ecc_encode_data_word_in[34] ^
	     ecc_encode_data_word_in[35] ^
	     ecc_encode_data_word_in[36] ^
	     ecc_encode_data_word_in[37] ^
	     ecc_encode_data_word_in[38] ^
	     ecc_encode_data_word_in[39] ^
	     ecc_encode_data_word_in[40] ^
	     ecc_encode_data_word_in[41] ^
	     ecc_encode_data_word_in[42] ^
	     ecc_encode_data_word_in[43] ^
	     ecc_encode_data_word_in[44] ^
	     ecc_encode_data_word_in[45] ^
	     ecc_encode_data_word_in[46] ^
	     ecc_encode_data_word_in[47] ^
	     ecc_encode_data_word_in[48] ^
	     ecc_encode_data_word_in[49] ^
	     ecc_encode_data_word_in[50] ^
	     ecc_encode_data_word_in[51] ^
	     ecc_encode_data_word_in[52] ^
	     ecc_encode_data_word_in[53] ^
	     ecc_encode_data_word_in[54] ^
	     ecc_encode_data_word_in[55] ^
	     ecc_encode_data_word_in[56] ;
  assign y__h1891 =
	     IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d130[4] ^
	     ecc_encode_data_word_in[11] ^
	     ecc_encode_data_word_in[12] ^
	     ecc_encode_data_word_in[13] ^
	     ecc_encode_data_word_in[14] ^
	     ecc_encode_data_word_in[15] ^
	     ecc_encode_data_word_in[16] ^
	     ecc_encode_data_word_in[17] ^
	     ecc_encode_data_word_in[18] ^
	     ecc_encode_data_word_in[19] ^
	     ecc_encode_data_word_in[20] ^
	     ecc_encode_data_word_in[21] ^
	     ecc_encode_data_word_in[22] ^
	     ecc_encode_data_word_in[23] ^
	     ecc_encode_data_word_in[24] ^
	     ecc_encode_data_word_in[25] ^
	     ecc_encode_data_word_in[41] ^
	     ecc_encode_data_word_in[42] ^
	     ecc_encode_data_word_in[43] ^
	     ecc_encode_data_word_in[44] ^
	     ecc_encode_data_word_in[45] ^
	     ecc_encode_data_word_in[46] ^
	     ecc_encode_data_word_in[47] ^
	     ecc_encode_data_word_in[48] ^
	     ecc_encode_data_word_in[49] ^
	     ecc_encode_data_word_in[50] ^
	     ecc_encode_data_word_in[51] ^
	     ecc_encode_data_word_in[52] ^
	     ecc_encode_data_word_in[53] ^
	     ecc_encode_data_word_in[54] ^
	     ecc_encode_data_word_in[55] ^
	     ecc_encode_data_word_in[56] ;
  assign y__h1892 =
	     IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d130[3] ^
	     ecc_encode_data_word_in[4] ^
	     ecc_encode_data_word_in[5] ^
	     ecc_encode_data_word_in[6] ^
	     ecc_encode_data_word_in[7] ^
	     ecc_encode_data_word_in[8] ^
	     ecc_encode_data_word_in[9] ^
	     ecc_encode_data_word_in[10] ^
	     ecc_encode_data_word_in[18] ^
	     ecc_encode_data_word_in[19] ^
	     ecc_encode_data_word_in[20] ^
	     ecc_encode_data_word_in[21] ^
	     ecc_encode_data_word_in[22] ^
	     ecc_encode_data_word_in[23] ^
	     ecc_encode_data_word_in[24] ^
	     ecc_encode_data_word_in[25] ^
	     ecc_encode_data_word_in[33] ^
	     ecc_encode_data_word_in[34] ^
	     ecc_encode_data_word_in[35] ^
	     ecc_encode_data_word_in[36] ^
	     ecc_encode_data_word_in[37] ^
	     ecc_encode_data_word_in[38] ^
	     ecc_encode_data_word_in[39] ^
	     ecc_encode_data_word_in[40] ^
	     ecc_encode_data_word_in[49] ^
	     ecc_encode_data_word_in[50] ^
	     ecc_encode_data_word_in[51] ^
	     ecc_encode_data_word_in[52] ^
	     ecc_encode_data_word_in[53] ^
	     ecc_encode_data_word_in[54] ^
	     ecc_encode_data_word_in[55] ^
	     ecc_encode_data_word_in[56] ;
  assign y__h1893 =
	     IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d130[2] ^
	     ecc_encode_data_word_in[1] ^
	     ecc_encode_data_word_in[2] ^
	     ecc_encode_data_word_in[3] ^
	     ecc_encode_data_word_in[7] ^
	     ecc_encode_data_word_in[8] ^
	     ecc_encode_data_word_in[9] ^
	     ecc_encode_data_word_in[10] ^
	     ecc_encode_data_word_in[14] ^
	     ecc_encode_data_word_in[15] ^
	     ecc_encode_data_word_in[16] ^
	     ecc_encode_data_word_in[17] ^
	     ecc_encode_data_word_in[22] ^
	     ecc_encode_data_word_in[23] ^
	     ecc_encode_data_word_in[24] ^
	     ecc_encode_data_word_in[25] ^
	     ecc_encode_data_word_in[29] ^
	     ecc_encode_data_word_in[30] ^
	     ecc_encode_data_word_in[31] ^
	     ecc_encode_data_word_in[32] ^
	     ecc_encode_data_word_in[37] ^
	     ecc_encode_data_word_in[38] ^
	     ecc_encode_data_word_in[39] ^
	     ecc_encode_data_word_in[40] ^
	     ecc_encode_data_word_in[45] ^
	     ecc_encode_data_word_in[46] ^
	     ecc_encode_data_word_in[47] ^
	     ecc_encode_data_word_in[48] ^
	     ecc_encode_data_word_in[53] ^
	     ecc_encode_data_word_in[54] ^
	     ecc_encode_data_word_in[55] ^
	     ecc_encode_data_word_in[56] ^
	     ecc_encode_data_word_in[60] ^
	     ecc_encode_data_word_in[61] ^
	     ecc_encode_data_word_in[62] ^
	     ecc_encode_data_word_in[63] ;
  assign y__h1894 =
	     IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d173 ^
	     ecc_encode_data_word_in[5] ^
	     ecc_encode_data_word_in[6] ^
	     ecc_encode_data_word_in[9] ^
	     ecc_encode_data_word_in[10] ^
	     ecc_encode_data_word_in[12] ^
	     ecc_encode_data_word_in[13] ^
	     ecc_encode_data_word_in[16] ^
	     ecc_encode_data_word_in[17] ^
	     ecc_encode_data_word_in[20] ^
	     ecc_encode_data_word_in[21] ^
	     ecc_encode_data_word_in[24] ^
	     ecc_encode_data_word_in[25] ^
	     ecc_encode_data_word_in[27] ^
	     ecc_encode_data_word_in[28] ^
	     ecc_encode_data_word_in[31] ^
	     ecc_encode_data_word_in[32] ^
	     ecc_encode_data_word_in[35] ^
	     ecc_encode_data_word_in[36] ^
	     ecc_encode_data_word_in[39] ^
	     ecc_encode_data_word_in[40] ^
	     ecc_encode_data_word_in[43] ^
	     ecc_encode_data_word_in[44] ^
	     ecc_encode_data_word_in[47] ^
	     ecc_encode_data_word_in[48] ^
	     ecc_encode_data_word_in[51] ^
	     ecc_encode_data_word_in[52] ^
	     ecc_encode_data_word_in[55] ^
	     ecc_encode_data_word_in[56] ^
	     ecc_encode_data_word_in[58] ^
	     ecc_encode_data_word_in[59] ^
	     ecc_encode_data_word_in[62] ^
	     ecc_encode_data_word_in[63] ;
  assign z__h104 = z__h97 ^ ecc_encode_data_word_in[9] ;
  assign z__h111 = z__h104 ^ ecc_encode_data_word_in[10] ;
  assign z__h118 = z__h111 ^ ecc_encode_data_word_in[11] ;
  assign z__h125 = z__h118 ^ ecc_encode_data_word_in[12] ;
  assign z__h132 = z__h125 ^ ecc_encode_data_word_in[13] ;
  assign z__h139 = z__h132 ^ ecc_encode_data_word_in[14] ;
  assign z__h146 = z__h139 ^ ecc_encode_data_word_in[15] ;
  assign z__h153 = z__h146 ^ ecc_encode_data_word_in[16] ;
  assign z__h160 = z__h153 ^ ecc_encode_data_word_in[17] ;
  assign z__h167 = z__h160 ^ ecc_encode_data_word_in[18] ;
  assign z__h174 = z__h167 ^ ecc_encode_data_word_in[19] ;
  assign z__h181 = z__h174 ^ ecc_encode_data_word_in[20] ;
  assign z__h1842 =
	     IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d136 ^
	     ecc_encode_data_word_in[6] ^
	     ecc_encode_data_word_in[8] ^
	     ecc_encode_data_word_in[10] ^
	     ecc_encode_data_word_in[11] ^
	     ecc_encode_data_word_in[13] ^
	     ecc_encode_data_word_in[15] ^
	     ecc_encode_data_word_in[17] ^
	     ecc_encode_data_word_in[19] ^
	     ecc_encode_data_word_in[21] ^
	     ecc_encode_data_word_in[23] ^
	     ecc_encode_data_word_in[25] ^
	     ecc_encode_data_word_in[26] ^
	     ecc_encode_data_word_in[28] ^
	     ecc_encode_data_word_in[30] ^
	     ecc_encode_data_word_in[32] ^
	     ecc_encode_data_word_in[34] ^
	     ecc_encode_data_word_in[36] ^
	     ecc_encode_data_word_in[38] ^
	     ecc_encode_data_word_in[40] ^
	     ecc_encode_data_word_in[42] ^
	     ecc_encode_data_word_in[44] ^
	     ecc_encode_data_word_in[46] ^
	     ecc_encode_data_word_in[48] ^
	     ecc_encode_data_word_in[50] ^
	     ecc_encode_data_word_in[52] ^
	     ecc_encode_data_word_in[54] ^
	     ecc_encode_data_word_in[56] ^
	     ecc_encode_data_word_in[57] ^
	     ecc_encode_data_word_in[59] ^
	     ecc_encode_data_word_in[61] ^
	     ecc_encode_data_word_in[63] ;
  assign z__h1849 = z__h1842 ^ y__h1894 ;
  assign z__h1856 = z__h1849 ^ y__h1893 ;
  assign z__h1863 = z__h1856 ^ y__h1892 ;
  assign z__h1870 = z__h1863 ^ y__h1891 ;
  assign z__h1877 = z__h1870 ^ y__h1890 ;
  assign z__h188 = z__h181 ^ ecc_encode_data_word_in[21] ;
  assign z__h1884 =
	     z__h1877 ^
	     IF_IF_ecc_encode_data_word_in_BIT_0_THEN_8_ELS_ETC___d350 ;
  assign z__h195 = z__h188 ^ ecc_encode_data_word_in[22] ;
  assign z__h202 = z__h195 ^ ecc_encode_data_word_in[23] ;
  assign z__h209 = z__h202 ^ ecc_encode_data_word_in[24] ;
  assign z__h216 = z__h209 ^ ecc_encode_data_word_in[25] ;
  assign z__h223 = z__h216 ^ ecc_encode_data_word_in[26] ;
  assign z__h230 = z__h223 ^ ecc_encode_data_word_in[27] ;
  assign z__h237 = z__h230 ^ ecc_encode_data_word_in[28] ;
  assign z__h244 = z__h237 ^ ecc_encode_data_word_in[29] ;
  assign z__h251 = z__h244 ^ ecc_encode_data_word_in[30] ;
  assign z__h258 = z__h251 ^ ecc_encode_data_word_in[31] ;
  assign z__h265 = z__h258 ^ ecc_encode_data_word_in[32] ;
  assign z__h272 = z__h265 ^ ecc_encode_data_word_in[33] ;
  assign z__h279 = z__h272 ^ ecc_encode_data_word_in[34] ;
  assign z__h286 = z__h279 ^ ecc_encode_data_word_in[35] ;
  assign z__h293 = z__h286 ^ ecc_encode_data_word_in[36] ;
  assign z__h300 = z__h293 ^ ecc_encode_data_word_in[37] ;
  assign z__h307 = z__h300 ^ ecc_encode_data_word_in[38] ;
  assign z__h314 = z__h307 ^ ecc_encode_data_word_in[39] ;
  assign z__h321 = z__h314 ^ ecc_encode_data_word_in[40] ;
  assign z__h328 = z__h321 ^ ecc_encode_data_word_in[41] ;
  assign z__h335 = z__h328 ^ ecc_encode_data_word_in[42] ;
  assign z__h342 = z__h335 ^ ecc_encode_data_word_in[43] ;
  assign z__h349 = z__h342 ^ ecc_encode_data_word_in[44] ;
  assign z__h356 = z__h349 ^ ecc_encode_data_word_in[45] ;
  assign z__h363 = z__h356 ^ ecc_encode_data_word_in[46] ;
  assign z__h370 = z__h363 ^ ecc_encode_data_word_in[47] ;
  assign z__h377 = z__h370 ^ ecc_encode_data_word_in[48] ;
  assign z__h384 = z__h377 ^ ecc_encode_data_word_in[49] ;
  assign z__h391 = z__h384 ^ ecc_encode_data_word_in[50] ;
  assign z__h398 = z__h391 ^ ecc_encode_data_word_in[51] ;
  assign z__h405 = z__h398 ^ ecc_encode_data_word_in[52] ;
  assign z__h412 = z__h405 ^ ecc_encode_data_word_in[53] ;
  assign z__h419 = z__h412 ^ ecc_encode_data_word_in[54] ;
  assign z__h426 = z__h419 ^ ecc_encode_data_word_in[55] ;
  assign z__h433 = z__h426 ^ ecc_encode_data_word_in[56] ;
  assign z__h440 = z__h433 ^ ecc_encode_data_word_in[57] ;
  assign z__h447 = z__h440 ^ ecc_encode_data_word_in[58] ;
  assign z__h454 = z__h447 ^ ecc_encode_data_word_in[59] ;
  assign z__h461 = z__h454 ^ ecc_encode_data_word_in[60] ;
  assign z__h468 = z__h461 ^ ecc_encode_data_word_in[61] ;
  assign z__h475 = z__h468 ^ ecc_encode_data_word_in[62] ;
  assign z__h48 = ecc_encode_data_word_in[0] ^ ecc_encode_data_word_in[1] ;
  assign z__h482 = z__h475 ^ ecc_encode_data_word_in[63] ;
  assign z__h55 = z__h48 ^ ecc_encode_data_word_in[2] ;
  assign z__h62 = z__h55 ^ ecc_encode_data_word_in[3] ;
  assign z__h69 = z__h62 ^ ecc_encode_data_word_in[4] ;
  assign z__h76 = z__h69 ^ ecc_encode_data_word_in[5] ;
  assign z__h83 = z__h76 ^ ecc_encode_data_word_in[6] ;
  assign z__h90 = z__h83 ^ ecc_encode_data_word_in[7] ;
  assign z__h97 = z__h90 ^ ecc_encode_data_word_in[8] ;
endmodule  // module_ecc_encode
