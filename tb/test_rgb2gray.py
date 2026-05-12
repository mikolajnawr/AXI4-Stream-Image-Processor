import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotbext.axi import AxiStreamBus, AxiStreamSource, AxiStreamSink
from PIL import Image

@cocotb.test()
async def test_image_filter(dut):
    # 1. Generate clock for the DUT (100 MHz)
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # 2. Attach open-source BFM models to the SystemVerilog pins
    # NOTE: reset_active_level=False is required because we use rst_n (active low)
    source = AxiStreamSource(AxiStreamBus.from_prefix(dut, "s_axis"), dut.clk, dut.rst_n, reset_active_level=False)
    sink   = AxiStreamSink(AxiStreamBus.from_prefix(dut, "m_axis"), dut.clk, dut.rst_n, reset_active_level=False)

    # 3. Reset procedure
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1

    # 4. Load the physical image
    dut._log.info("Loading input.jpg image...")
    img = Image.open("input.jpg").convert("RGBA")
    
    # AXI sends data byte by byte. 
    # SystemVerilog expects: a=[31:24], r=[23:16], g=[15:8], b=[7:0]
    # We arrange channels in B, G, R, A order so B falls into the lowest bits.
    r, g, b, a = img.split()
    img_bgra = Image.merge("RGBA", (b, g, r, a))
    
    # Convert the entire image into a raw byte stream
    byte_data = img_bgra.tobytes()

    # 5. TEST: Send the pixel stream via AXI bus to the FPGA
    dut._log.info(f"Sending a {img.width}x{img.height} image to the hardware...")
    await source.send(byte_data)

    # 6. TEST: Receive the filtered pixels from the FPGA
    received_frame = await sink.recv()
    dut._log.info("Result received from hardware! Creating the output file...")

    # 7. Save the output
    received_bytes = bytes(received_frame.tdata)
    
    # Recreate the BGRA image
    out_img_bgra = Image.frombytes("RGBA", (img.width, img.height), received_bytes)
    
    # Swap colors back to RGB to save as JPG
    b_out, g_out, r_out, a_out = out_img_bgra.split()
    final_img = Image.merge("RGB", (r_out, g_out, b_out))
    
    final_img.save("output_gray.jpg")
    dut._log.info("SUCCESS! output_gray.jpg generated successfully.")