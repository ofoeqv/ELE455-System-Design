`timescale 1ns/1ps
module tb_byte_key_xor;
    reg [7:0] state_byte, key_byte;
    wire [7:0] result;
    integer s, k;
    byte_key_xor dut(.state_byte(state_byte), .key_byte(key_byte), .result(result));
    initial begin
        for (s=0; s<256; s=s+1)
            for (k=0; k<256; k=k+1) begin
                state_byte = s[7:0]; key_byte = k[7:0];
                #1;
                if (result !== (state_byte ^ key_byte))
                    $fatal(1, "XOR mismatch state=%h key=%h result=%h", state_byte, key_byte, result);
            end
        $display("PASS preparation exhaustive byte XOR");
        $finish;
    end
    initial begin #70000; $fatal(1, "Watchdog timeout"); end
endmodule
