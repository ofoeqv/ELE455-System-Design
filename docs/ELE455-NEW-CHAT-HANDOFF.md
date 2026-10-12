# ELE455 New-Chat Handoff — Verilog, Verification, AES FPGA

**As of 2026-10-12.** This handoff records the tutoring state and repository conventions. The primary durable exercise history is [the bootcamp learning log](../logbook/verilog-bootcamp.md).

## Mission
Guide the user through ELE455 System Design, an AES-128 FPGA project (Nexys A7 100T / Vivado). Priority is independent RTL design, simulation, verification and eventual synthesis/FPGA work. User prefers a demanding, **one-exercise-at-a-time** tutor: grade each submission, explain *first error* and then other errors, explain reasoning behind Verilog, revisit weaknesses for spaced repetition, and do not jump ahead. Show only one next challenge each time.

## Exact current stopping point
**Exercise 21 is assigned and not yet answered.** The user is to write their first self-checking **Verilog testbench** for a combinational eight-bit XOR DUT, starting from:

```verilog
module xor8 (
    input wire [7:0] a, b,
    output wire [7:0] y
);
    assign y = a ^ b;
endmodule
```

Testbench skeleton presented:
```verilog
module tb_xor8;
    reg [7:0] a;
    reg [7:0] b;
    wire [7:0] y;

    xor8 dut (.a(a), .b(b), .y(y));

    initial begin
        // TODO 1: Set a = 8'h53 and b = 8'hCA
        #1;
        // TODO 2: if y differs from 8'h99, $fatal(1, "XOR failed")
        // TODO 3: $finish;
    end
endmodule
```
Check assigned stimulus, delayed check, correct `if (y != 8'h99)`, `$fatal(1, "XOR failed");`, and `$finish;`. Explain that `initial` and `#1` are testbench constructs, not synthesizable hardware. **Do not reveal a full solution unless user needs corrective teaching.** If the user instead asks to resume generally, present only Exercise 21.

## Previous milestone
- Exercise 17: correctly wrote PROCESS-gated, resettable 8-bit XOR result register.
- Exercise 18: 12/12 correct FSM/result/done edge predictions.
- Exercise 19: correctly wrote two input capture registers on `IDLE && start`.
- Exercise 20: 10/12 correct; incorrectly cleared captures on DONE→IDLE.
- Exercise 20B: 2/2 correct retest. Captured bytes hold without explicit assignment.
- Earlier: FSM problems with case/endcase, block nesting, state vs constants, and output decoding; Exercise 16D corrected nesting, but standalone syntax fluency still merits spaced repetition.
- See [full learning log](../logbook/verilog-bootcamp.md) for Exercises 1–21 grades and missteps.

## Learning roadmap / next work
1. **Now**: Exercise 21 self-checking XOR Verilog testbench.
2. Extend to multiple directed vectors, good error messages, and mutation testing (XOR→AND).
3. Test clocked and FSM-controlled modules: `posedge`, reset, acceptance, latency, changing external inputs and cancellation; consider cocotb and Verilator.
4. Implement/verify individual AES datapath units: AddRoundKey, ShiftRows, SubBytes, xtime and MixColumns; compare to Python golden model.
5. Explore sequencing/area vs throughput and FPGA build: Vivado simulation/synthesis, utilisation, timing, hardware targets, maintain module logbook and evidence.
This is an intended progression, **not** a claim these later steps were completed.

## Critical technical concepts to reinforce
- `assign y = a ^ b;`: combinational continuous assignment.
- `always @(posedge clk)` and `<=`: edge-driven state; RHS sampled from pre-edge values.
- Sync `rst` wins over `enable` through `if (rst) ... else if (enable)`.
- No clocked assignment means a flip-flop holds; missing combinational assignment may infer a latch.
- Three-state Moore FSM: IDLE (await start), PROCESS (compute), DONE (pulse done), then IDLE. `assign done = (state == DONE);`.
- FSM and datapath are separate processes. On PROCESS→DONE edge, datapath sees old state PROCESS and stores result while `done` reflects new DONE.
- Capture inputs in IDLE on acceptance so changing external values during PROCESS cannot corrupt result.
- `state` is mutable register; `IDLE/PROCESS/DONE` are immutable `localparam` constants. Capitalisation is significant.
- Need explicit `default: state <= IDLE;`, `endcase`, matching `begin/end`.

## Project environment and important prior context
Repository: https://github.com/ofoeqv/ELE455-System-Design (main branch observed on 2026-10-12). Existing paths: `README.md`, `logbook/week01.md`, `evidence/week01/README.md`, `code/` (the latter referenced in README). User earlier requested branch name `modules/ele455-system-design`, but GitHub branch lookup returned only main at documentation time; do not claim that branch exists.

Local home path reported: `C:\Users\manas\ProjectUltra\projects\ELE455\code` (may differ from cloned standalone repo). University PC path previously `U:\ELE455\ELE455-System-Design-main\code`. Tools previously reported: Python 3.9.x, WSL Ubuntu, make 4.4.1, g++ 15.2.0, Verilator 5.032. Do not assume the new chat can directly access these machines; ask for terminal logs and command output as needed.

Earlier course study (separate from chat bootcamp): Week 1 Python golden model and byte-XOR verification, Week 2 Python AES transformation exploration; read [logbook](../logbook/verilog-bootcamp.md) caveats before calling these complete. **Do not mark incomplete logbook templates or absent evidence as completed.**

Previous resources: ELE455 intro lecture, AES lecture, Week 1/2 worksheets; user also had a 63-page Verilog and Cocotb Crash Course and HDLBits problem set. If resources are not present in the new chat, retrieve the user's files/Drive appropriately or ask for them; do not assume source bytes were committed to GitHub.

## Rules for continuing
- First response in new chat: acknowledge stopping point and show only Exercise 21, unless user already supplies its answer.
- Keep questions tightly scoped, step-by-step. Offer rationale after grading; do not solve exercise prematurely.
- Distinguish **static-reviewed RTL** from **simulation-confirmed functionality**. Most bootcamp passes so far are tutor-reviewed only.
- Whenever tests run, document command, observed PASS/FAIL, exact failure and restoration before asserting verified.
- Update repository learning log after a meaningful milestone; do not erase user evidence or falsely claim older coursework done.
- When current testing involves `#1`, explain simulation timescale if needed and delta cycles accurately.
- After testbench basics, return to transaction-changing-input tests and reset cancellation (Week 2 goals).

## Suggested next-chat seed
"Continue ELE455 Verilog bootcamp using the GitHub handoff at `docs/ELE455-NEW-CHAT-HANDOFF.md` and learning log `logbook/verilog-bootcamp.md` in `ofoeqv/ELE455-System-Design`. I'm at Exercise 21, the first self-checking XOR testbench. Grade my work strictly, explain syntax and timing, track weaknesses for spaced repetition, and provide exactly one next exercise."
