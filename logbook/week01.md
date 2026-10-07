# ELE455 Logbook — Week 1

## Date
- Session date:
- Time spent:

## Goal
Represent and verify AES data correctly, then implement and test the scaffolded byte-wise key XOR circuit.

## W1A — Establish the reference

### Commands
```bash
python -m unittest discover -s model -v
python model/explore_preparation.py 1
```

### Evidence
- Test outcome:
- Exploration output:
- Screenshot / terminal capture reference:

### What this establishes
- 

---

## W1B — Predict before inspecting

### AES state mapping
Flat index rule:

```text
index = 4 * column + row
```

Packed-vector rule:

```text
byte i -> [127 - 8*i -: 8]
```

### Required checkpoint
For row 3, column 2:
- flat index =
- byte =
- packed slice =

### Four-by-four state drawing
```text
          c0   c1   c2   c3
row 0:    __   __   __   __
row 1:    __   __   __   __
row 2:    __   __   __   __
row 3:    __   __   __   __
```

### Initial AddRoundKey prediction
- Plaintext first column:
- Key first column:
- XOR result:
- Full expected initial state:

### my_week1.py
- Row 1 output:
- Why it is not the first four bytes of the input list:

### Last-byte experiment
- Changed plaintext byte:
- Predicted initial AddRoundKey byte affected:
- Observed result:
- Why full encryption affects more bytes:

---

## W1C — Complete and verify the byte XOR

### Before editing
Command:

```bash
python preparation/run.py week1 --bench verilog
```

- Starter failure retained:
- Failing input/result:

### RTL change
Only replace the RHS of the marked assignment in `preparation/byte_key_xor.v`.

### After editing
```bash
python preparation/run.py week1 --bench verilog
python preparation/run.py week1
```

- Verilog bench:
- cocotb bench:

### Exhaustive-test reasoning
- Why the nested loops cover all 65,536 input pairs:
- Why testing only `key_byte = 0` is inadequate:

---

## W1D — Mutation test

### Directed pair
- state =
- key =
- XOR =
- AND =
- truncated addition =

### Mutation
Temporary defect: replace XOR with AND.

- Verilog failure:
- cocotb failure:
- Failing directed/exhaustive input:
- Why the test detects the defect:

### Restoration
- XOR restored:
- Both benches pass again:

---

## W1E — Evidence and reflection

### Submission/evidence checklist
- [ ] State drawing
- [ ] Completed byte XOR circuit
- [ ] Named directed test case
- [ ] Passing Verilog summary
- [ ] Passing cocotb summary
- [ ] Mutation-failure summary
- [ ] Short explanation of why this does not yet verify full-state AddRoundKey wiring
- [ ] Week 1 quiz completed

### Reflection
What have I established?

What remains unverified?

What will matter for the Week 4 interface plan?
