import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def byte_key_addition(dut):
    # W1D: add a named directed pair and explain the defect it distinguishes.
    for state, key in [(0x53, 0xca), (0x80, 0x01), (0xff, 0xff)]:
        dut.state_byte.value = state
        dut.key_byte.value = key
        await Timer(1, unit='ns')
        assert int(dut.result.value) == state ^ key

    # Every possible pair is practical for this small combinational function.
    for state in range(256):
        for key in range(256):
            dut.state_byte.value = state
            dut.key_byte.value = key
            await Timer(1, unit='ns')
            assert int(dut.result.value) == state ^ key
