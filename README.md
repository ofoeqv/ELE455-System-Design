# ELE455 — System Design Workspace

## Purpose
Working area for the ELE455 AES FPGA design project.

## Structure

```text
ELE455-System-Design/
├── README.md
├── logbook/
│   └── week01.md
├── evidence/
│   └── week01/
│       └── README.md
├── code/
│   ├── model/
│   └── preparation/
├── references/
└── milestones/
```

## Week 1 objective
Establish the AES byte/state representation and the verification workflow before implementing assessed AES modules.

Core sequence:
1. Establish the Python golden reference.
2. Draw and verify the AES state mapping.
3. Predict the initial AddRoundKey result.
4. Run the intentionally incomplete byte-XOR RTL and retain the failure.
5. Complete the byte-XOR RTL and verify it with Verilog and cocotb.
6. Introduce an intentional mutation (XOR → AND), show that the tests catch it, then restore the correct RTL.
7. Record evidence and reflection in the logbook.

## Rule
Do not modify the supplied golden model or its reference tests during the core Week 1 exercise.
