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

## Verilog bootcamp — learning and handoff

- [Exercise-by-exercise learning log](logbook/verilog-bootcamp.md): graded exercises, recurring syntax/RTL misconceptions, verification status, and open work.
- [New-chat continuation handoff](docs/ELE455-NEW-CHAT-HANDOFF.md): complete tutoring protocol, current Exercise 21, technical context, and next steps.

Bootcamp grades represent static chat reviews unless a terminal/simulator run is explicitly documented; they are not automatically build or test evidence.
