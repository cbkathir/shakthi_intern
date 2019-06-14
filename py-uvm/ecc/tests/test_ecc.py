# Simple tests for an adder module
import cocotb
from cocotb.triggers import Timer
from cocotb.result import TestFailure
from hamming import hamming_encode_nbit
import random


@cocotb.test()
def ecc_encode_basic_test(dut):
    """Test for ecc(5,64)"""
    yield Timer(2)
    data = 5
    data_width = 64

    dut.ecc_encode_data_word_in = data

    yield Timer(2)
    dut_output = int(dut.ecc_encode)
    expected_output = int(hamming_encode_nbit(data,data_width),2)
    if dut_output != expected_output:
        raise TestFailure(
            "Adder result is incorrect: %s != %s" % (str(dut_output), str(expected_output)))
    else:  # these last two lines are not strictly necessary
        dut._log.info("TEST PASSED")


@cocotb.test()
def ecc_encode_randomised_test(dut):
    """Test for adding 2 random numbers multiple times"""
    yield Timer(2)

    for i in range(10):
        data = random.randint(0,18446744073709551614)
        data_width = 64

        dut.ecc_encode_data_word_in = data
        dut._log.info("DATA tested: %s" % (str(data)))
        yield Timer(2)
        dut_output = int(dut.ecc_encode)
        expected_output = int(hamming_encode_nbit(data,data_width),2)

        if dut_output != expected_output:
            raise TestFailure(
                "Adder result is incorrect: %s != %s" % (str(dut_output), str(expected_output)))
        else:  # these last two lines are not strictly necessary
            dut._log.info("TEST PASSED")
