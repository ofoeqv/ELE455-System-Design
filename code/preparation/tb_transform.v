`timescale 1ns/1ps
`ifndef DUT
`define DUT byte_transform
`endif
module tb_transform;
parameter integer WIDTH=8, LATENCY=1, LANES=4;
reg clk=0, rst=0, in_valid=0;
reg [WIDTH-1:0] in_data=0;
wire in_ready, out_valid;
wire [WIDTH-1:0] out_data;
`ifdef STATE_DUT
`DUT #(.LANES(LANES)) dut(.clk(clk), .rst(rst), .in_valid(in_valid),
  .in_data(in_data), .in_ready(in_ready), .out_valid(out_valid), .out_data(out_data));
`else
`DUT dut(.clk(clk), .rst(rst), .in_valid(in_valid), .in_data(in_data),
  .in_ready(in_ready), .out_valid(out_valid), .out_data(out_data));
`endif
integer cycle, byte_index, due=-1, last_accept=-1, results=0;
reg accepted, expected_valid;
reg [WIDTH-1:0] expected_data=0, pending_data=0;
reg [8:0] product;
integer stimulus_byte;
initial begin
  for (cycle=0; cycle<100; cycle=cycle+1) begin
    clk=0;
    rst=(cycle==0 || cycle==7 || cycle==28);
    in_valid=(cycle<82);
    for (byte_index=0; byte_index<WIDTH/8; byte_index=byte_index+1) begin
      stimulus_byte=(cycle*37+byte_index*19)%256;
      in_data[8*byte_index +: 8]=stimulus_byte[7:0];
    end
    #5;
    if (in_ready !== (!rst && due==-1)) $fatal(1,"Ready mismatch");
    accepted=in_valid && in_ready;
    expected_valid=0;
    if (rst) begin due=-1; last_accept=-1; expected_data=0; end
    else begin
      if (due==cycle) begin
        expected_valid=1; expected_data=pending_data; due=-1;
      end
      if (accepted) begin
        if (last_accept!=-1 && cycle-last_accept!=LATENCY+1)
          $fatal(1,"Wrong initiation interval");
        last_accept=cycle;
        due=cycle+LATENCY;
        for (byte_index=0; byte_index<WIDTH/8; byte_index=byte_index+1) begin
          product={1'b0,in_data[8*byte_index +: 8]} << 1;
          if (product[8]) product=product ^ 9'h11b;
          pending_data[8*byte_index +: 8]=product[7:0];
        end
      end
    end
    clk=1; #5;
    if (out_valid !== expected_valid) $fatal(1,"Wrong valid at edge %0d",cycle);
    if ((expected_valid || rst || WIDTH==8) && out_data !== expected_data)
      $fatal(1,"Wrong data at edge %0d",cycle);
    if (out_valid) results=results+1;
  end
  if (due!=-1 || results<6) $fatal(1,"Missing results");
  $display("PASS preparation latency=%0d II=%0d results=%0d",LATENCY,LATENCY+1,results);
  $finish;
end
initial begin #1500; $fatal(1,"Watchdog timeout"); end
endmodule
