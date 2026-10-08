import os
import random
import cocotb
from cocotb.triggers import Timer


def reference(value, width):
    result = 0
    for shift in range(0, width, 8):
        byte = (value >> shift) & 255
        # Polynomial multiply followed by reduction; independent of RTL slices.
        product = byte * 2
        if product & 256:
            product ^= 0x11b
        result |= product << shift
    return result


@cocotb.test()
async def accepted_values_and_schedule(dut):
    width = int(os.environ['PREP_WIDTH'])
    latency = int(os.environ['PREP_LATENCY'])
    rng = random.Random(455)
    pending = None
    last_accept = None
    intervals = []
    publications = 0
    previous_output = 0
    for edge in range(100):
        dut.clk.value = 0
        reset = edge in (0, 7, 28)  # Cancels accepted work in both schedules.
        offered = edge < 82
        value = rng.getrandbits(width)  # Changes even while busy.
        if edge == 1:
            value = int('83' * (width // 8), 16)
        dut.rst.value = int(reset)
        dut.in_valid.value = int(offered)
        dut.in_data.value = value
        await Timer(5, unit='ns')
        ready = int(dut.in_ready.value)
        assert ready == int(not reset and pending is None)
        expected_valid = False
        if reset:
            pending = None
            previous_output = 0
            last_accept = None
        else:
            if pending is not None and edge == pending[0]:
                expected_valid = True
                previous_output = pending[1]
                pending = None
            if offered and ready:
                if last_accept is not None:
                    intervals.append(edge - last_accept)
                last_accept = edge
                pending = (edge + latency, reference(value, width))
        dut.clk.value = 1
        await Timer(5, unit='ns')
        assert int(dut.out_valid.value) == expected_valid, f'valid at edge {edge}'
        if expected_valid or reset or width == 8:
            assert int(dut.out_data.value) == previous_output, f'data at edge {edge}'
        if expected_valid:
            publications += 1
    assert pending is None, 'Missing result at end'
    assert publications > 5
    assert intervals and all(gap == latency + 1 for gap in intervals)
    dut._log.info('Measured latency=%d, II=%d, publications=%d', latency,
                  latency + 1, publications)
