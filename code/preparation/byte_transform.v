`timescale 1ns/1ps
module byte_transform(
 input wire clk, rst, in_valid,
 input wire [7:0] in_data,
 output wire in_ready,
 output reg out_valid,
 output reg [7:0] out_data
);
 reg busy;
 reg [7:0] captured;
 assign in_ready = !rst && !busy;
 // Supplied AES field operation. Study it; do not change it for W2C.
 function [7:0] xtime;
  input [7:0] x;
  begin xtime = {x[6:0],1'b0} ^ (x[7] ? 8'h1b : 8'h00); end
 endfunction
 always @(posedge clk) begin
  if (rst) begin
   busy <= 0;
   captured <= 0;
   out_valid <= 0;
   out_data <= 0;
  end else begin
   out_valid <= 0;
   if (busy) begin
    out_data <= xtime(captured);
    out_valid <= 0; // W2C: publish a one-cycle pulse here.
    busy <= 0;
   end else if (in_valid && in_ready) begin
    captured <= 0; // W2C: capture the accepted input here.
    busy <= 1;
   end
  end
 end
endmodule
