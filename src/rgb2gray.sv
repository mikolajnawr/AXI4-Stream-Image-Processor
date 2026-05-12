`timescale 1ns/1ps

module rgb2gray (
    input  logic        clk,
    input  logic        rst_n,

    // AXI-Stream Input (Receives colored pixels)
    input  logic [31:0] s_axis_tdata,
    input  logic        s_axis_tvalid,
    input  logic        s_axis_tlast,
    output logic        s_axis_tready,

    // AXI-Stream Output (Sends grayscale pixels)
    output logic [31:0] m_axis_tdata,
    output logic        m_axis_tvalid,
    output logic        m_axis_tlast,
    input  logic        m_axis_tready
);

    // Internal color signals
    logic [7:0] r, g, b, a;
    logic [7:0] gray;

    // 1. Extract color channels from the 32-bit packet
    assign a = s_axis_tdata[31:24]; // Alpha channel (Transparency)
    assign r = s_axis_tdata[23:16]; // Red
    assign g = s_axis_tdata[15:8];  // Green
    assign b = s_axis_tdata[7:0];   // Blue

    // 2. HARDWARE MATH: Convert to grayscale
    // Formula: Y = 0.299*R + 0.587*G + 0.114*B
    // We multiply by 256 and divide using a logical right shift (>> 8) to avoid floating-point math
    assign gray = (r * 16'd77 + g * 16'd150 + b * 16'd29) >> 8;

    // 3. Drive the output data (all color channels receive the 'gray' value)
    assign m_axis_tdata = {a, gray, gray, gray};

    // 4. Pass the AXI control signals (Transparent Handshake)
    assign m_axis_tvalid = s_axis_tvalid;
    assign m_axis_tlast  = s_axis_tlast;
    assign s_axis_tready = m_axis_tready;

endmodule