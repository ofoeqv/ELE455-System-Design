# ELE455 Verilog Bootcamp — Learning Log (through Exercise 21)

**Updated:** 2026-10-12  
**Source:** tutoring conversation, exercises 1–20; Exercise 21 assigned but not submitted.  
**Evidence standard:** "passed" in this document means *reviewed in chat* unless an explicit tool run is described. No code in this bootcamp was compiled/simulated as part of these chats. Do not mistake tutor review for toolchain evidence.

## Objective
Develop independent Verilog RTL, verification and AES-on-FPGA competence for the ELE455 System Design project (AES-128 implementation on Nexys A7 100T using Vivado). The user prefers one exercise at a time, direct grading, first-error explanations, targeted retests, and spaced-repetition tracking. Avoid jumping to advanced material without checking mastery.

## Exercise-by-exercise chronology

| Exercise | Topic | Submission and result | What was learned / recurring error |
|---|---|---|---|
| Diagnostic | 8-bit clocked XOR module | 2.5/5 | Could identify sequential logic; needed clock vs combinational, `<=` vs `=` explanation. |
| 1 | Combinational byte XOR | Invalid procedural syntax | Learned `assign y = a ^ b;`. |
| 2–3 | Byte AND; logical vs bitwise | Used `&&` rather than `&`; corrected prediction | `&&` yields one-bit truth value, `&` works bitwise. |
| 4 | Ternary MUX | Omitted `assign y =` and semicolon | `assign y = sel ? b : a;`. |
| 5 | Combinational MUX `always @*` | Multiple invalid `begin/end` attempts; ultimately 5/5 | Correct procedural `if/else`, blocking `=`; nesting was fragile. |
| 6 | Synchronous-reset 8-bit register | 4/5, missing final `end` | Correct reset logic and `<=`. |
| 7 | Register timing prediction | Initial 0/4 | Misunderstood edge capture, synchronous reset, state retention. |
| 7B | Register timing retest | 4/4 | Correct `q = 11, 00, 33, 44` after edges. |
| 8 | Clock-enabled register | 4/5 | Functionally correct, wrote `always @posedge (clk)` instead of `always @(posedge clk)`. |
| 9 | Enable/register timing | 5/5 | Correct `53,53,F1,00,00`, including reset priority. |
| 10 | Two-stage pipeline prediction | 8/8 | Correct old-value semantics of nonblocking assignments. |
| 11 | Write pipeline RTL | 4/5 | Correct behaviour; missed four assignment semicolons. |
| 12 | Write enabled pipeline RTL | 5/5 | Correct reset, load/hold, pipeline, syntax. |
| 13 | Three-state FSM prediction | 6/6 | Correct IDLE/PROCESS/DONE transitions and reset. |
| 14 | Write FSM | 2/5 | Mistook `case` for an assignment; `case (IDLE) <= ...`; structural errors. |
| 14B | Fill FSM transition assignments | 2/5 | Assigned to immutable `IDLE/PROCESS/DONE` constants rather than `state`. |
| 14C | Independent rewrite | 2/5 | Invalid `case` syntax, missing blocks, incorrect transition and input condition. |
| 14D | Rewrite clocked FSM | 2/5 | Missing reset `else`; `if (state)` vs `if (start)`; typo `PROCEED`; colon/semicolon; closing delimiters. |
| 14E | FSM rewrite | 4/5 | Logic and branch nesting improved; missing last two `end` tokens. |
| 14F | FSM rewrite | 5/5 | Completed correct clocked state machine with reset and default. |
| 15 | Add Moore `done` output | 2/5 | Confused state constant `DONE` with output `done`; had missing `end`. |
| 15B | Single `assign` | 4/5 | Wrote `assign done (state == DONE);`, omitted `=`. |
| 15C | Single `assign` retest | 5/5 | Correct `assign done = (state == DONE);`. |
| 16 | Whole Moore FSM | 2/5 | `begin;`, missing IDLE `end`, invalid default, uppercase `STATE` error. |
| 16B | Whole Moore FSM rewrite | 4/5 | FSM logic correct, accidentally duplicated module declaration. |
| 16C | Whole FSM rewrite | 2/5 | Again missing IDLE `end`, default and final two closes. |
| 16D | Targeted FSM correction | 5/5 | Corrected all nested closures and default; still needs independent no-scaffold retest. |
| 17 | FSM-controlled XOR result register | 5/5 | Wrote correct reset-priority, PROCESS-gated `result <= a ^ b;`; result holds otherwise. |
| 18 | Predict FSM/datapath timing | 12/12 | Verified result updates on PROCESS->DONE edge, `done` decodes updated state. |
| 19 | Capture `a` and `b` on acceptance | 5/5 | Correct registered inputs when `state==IDLE && start`, reset priority, implicit hold; used valid `case` form. |
| 20 | Captured-input timing | 10/12 (83.3%) | Correct edge 1 and 2; incorrectly assumed captured registers clear at DONE->IDLE. An earlier response headline said 9/10 but actual count is 10/12. |
| 20B | Hold across DONE->IDLE retest | 2/2 | Correct retained `captured_a=53`, `captured_b=CA`. |
| 21 | Self-checking XOR testbench | **ASSIGNED; NO SUBMISSION YET** | Next task is to complete stimulus, `#1`, `if (y != 8'h99) $fatal(1, ...);`, and `$finish;`. |

## What the learner can currently explain/do
- Byte-vector declarations, `assign`, bitwise XOR/AND, muxes, `always @*`.
- `always @(posedge clk)`, sync reset, enable, hold, `<=` timing, 2-register pipelines.
- FSM state transitions; `case (state)`, Moore `done` output.
- FSM-controlled register updates; accepting and storing transaction inputs before processing; outputs valid on DONE entry edge.
- Predict edge-by-edge behaviour when external inputs change.

## Gaps requiring spaced repetition
1. **Nested syntax:** Every `begin` needs `end`; `case` needs `endcase`, and a clocked `always` needs its closing delimiter. Prefer indentation and compiler feedback.
2. **Exact syntax:** `;` on assignments, no `begin;`, spelling/case-sensitive identifiers, `assign lhs = rhs;`.
3. **FSM independence:** Exercise 16D was a targeted correction; independent full FSM code should be periodically retested.
4. **State vs constant:** `state <= PROCESS;` changes the stored state; constants like `PROCESS` are never assignment targets.
5. **Hold semantics:** Registers do not clear on DONE->IDLE without an explicit reset or assignment.
6. **Verification:** No independently written, simulated self-checking testbench yet. First pending is Exercise 21.
7. **Transaction integrity:** Capturing inputs works on paper, but no changing-input regression test has run.
8. **AES RTL + FPGA flow:** Full AES components, cocotb testbench authoring, Vivado implementation, area/timing metrics and FPGA programming remain to be demonstrated in this bootcamp.

## Technical reference: accepted transaction XOR controller
Typical behavioural arrangement (illustrative reference, not claimed tested):

```verilog
module xor_controller (
    input wire clk, rst, start,
    input wire [7:0] a, b,
    output reg [7:0] result,
    output wire done
);
    reg [1:0] state;
    reg [7:0] captured_a, captured_b;
    localparam IDLE = 2'd0, PROCESS = 2'd1, DONE = 2'd2;

    always @(posedge clk) begin
        if (rst) state <= IDLE;
        else case (state)
            IDLE: if (start) state <= PROCESS;
            PROCESS: state <= DONE;
            DONE: state <= IDLE;
            default: state <= IDLE;
        endcase
    end
    always @(posedge clk) begin
        if (rst) begin
            captured_a <= 8'h00;
            captured_b <= 8'h00;
        end else if ((state == IDLE) && start) begin
            captured_a <= a;
            captured_b <= b;
        end
    end
    always @(posedge clk) begin
        if (rst) result <= 8'h00;
        else if (state == PROCESS) result <= captured_a ^ captured_b;
    end
    assign done = (state == DONE);
endmodule
```

### Timing example
Initially IDLE and zero registers. Edge 1: start=1, inputs 53/CA → enter PROCESS, capture 53/CA, result remains zero. Inputs then change to FF/FF. Edge 2: PROCESS→DONE, result=53^CA=99, done asserts. Edge 3: DONE→IDLE, result and captured bytes hold, done deasserts. No automatic clear on returning to IDLE.

## Existing repo Week 1/2 work vs this bootcamp
Earlier separate course preparation (reported in chat, **not verified by current repository tool calls**):
- `python -m unittest discover -s model -v` passed four Python golden-model tests.
- WSL + Verilator 5.032 + GNU Make 4.4.1 + g++ 15.2.0 installed on home PC; earlier Week 1 Verilog bench reportedly passed.
- Python AES explorations: ShiftRows mapping, SubBytes(53)=ED, MixColumns sample, xtime reduction including 80→1B.
- Week 2 investigated ready/valid accept, capture, reset cancellation, result due-edge and changing-input mutation tests.
- Existing `logbook/week01.md` is a template with many unfilled fields and checkboxes; do not claim the listed artifacts were committed or all benchmarks finished. Week 2 logbook was not found in repo at documentation time.

## Learning protocol
1. Grade code for **compilability** separately from **logical intent**; do not label uncompiled code as tested.
2. Explain first error, then remainder briefly.
3. Advance by exactly **one exercise** per response, checking targeted mastery.
4. Demand one explicit stimulus/expected output/failure assertion before introducing broader verification.
5. Ask for actual terminal output when simulation is performed; keep commands and evidence.
6. Append future successes and failures to this file (or a dated continuation) once confirmed.

## Exercise 21 — first submission (2026-10-12)
**Status: 2/5 tutor-reviewed, not compiled or simulated. Retest required.**
- Correct DUT instantiation, initial block and delay, intended 53/CA → 99 check.
- First error: wrote `assign a = 0x53;` and `assign b = 0xCA;` inside `initial`. Use procedural `a = 8'h53;` and `b = 8'hCA;`; `0x` is not Verilog literal syntax. Legacy procedural continuous assignment exists but is inappropriate here.
- `!==` is acceptable and catches X/Z, but comparison literal should be `8'h99`.
- Unterminated string in `$fatal(1, "XOR failed);`; missing `$finish;`.
- Nesting balanced; retest exact syntax and success/failure simulation termination. Do not mark as passed until revised.

### Exercise 21B — second submission (2026-10-12)
**3/5 static review, NOT compiled/simulated; correction still required.** Fixed `8'h99` comparison and closed `$fatal` message; blocks balanced. Repeated `assign a = 0x53;` / `assign b = 0xCA;` in procedural `initial`: must change to `a = 8'h53;` / `b = 8'hCA;`. `$finish` missing semicolon. Did not answer why `#1;` is needed (simulation scheduling/settling). Prioritize procedural vs continuous assignment and literal syntax for spaced repetition. Next task: corrected complete TB and conceptual explanation, no progression yet.

### Exercise 21C — third submission (2026-10-12)
**4/5 provisional static review; not compiled or simulated.** Corrected procedural assignments (removed `assign`), comparison `!== 8'h99`, `$fatal` quoting, `$finish;`, and balanced block structure. **Remaining compilation blocker:** inputs still use C/Python literals `0x53`, `0xCA` instead of Verilog `8'h53`, `8'hCA`. **Conceptual gap:** interpreted `#1` as check duration; taught that it advances simulation time by one timescale unit to allow event propagation/settling before checking. Retest literal syntax and `#1` explanation; keep Exercise 21 open.
