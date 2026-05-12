# Hardware Image Filter (AXI4-Stream) 📷⚙️

This project demonstrates a hardware-level image processing accelerator written in **SystemVerilog**, verified using **Python** and **Cocotb** (Hardware/Software Co-simulation). 

The module receives colored pixels via the **AXI4-Stream** protocol, converts them to grayscale in real-time using hardware arithmetic (without floating-point operations), and streams the result back.

## 🛠️ Architecture & Technologies
* **RTL Design:** SystemVerilog (`rgb2gray.sv`)
* **Verification / Testbench:** Python (`test_rgb2gray.py`) using **Cocotb** framework.
* **Verification IP (VIP):** `cocotbext-axi` (Open-source AXI Bus Functional Models).
* **Simulator:** Icarus Verilog.

## 🚀 How it works
1. The Python testbench uses the `Pillow` library to open a real `.jpg` image.
2. The image is flattened into a raw byte array and transmitted pixel-by-pixel to the SystemVerilog module via an AXI4-Stream Master BFM.
3. The FPGA hardware applies the grayscale formula: `Y = (R*77 + G*150 + B*29) >> 8` in a single clock cycle.
4. The AXI4-Stream Slave BFM receives the processed pixels.
5. Python reconstructs the received byte array and saves it as `output_gray.jpg`.

## ⚙️ How to run the simulation

### Prerequisites
You need a Linux environment with Icarus Verilog and Python 3 installed.
```bash
sudo apt install iverilog make
pip3 install cocotb cocotbext-axi numpy pillow
```

### Running the test
1. Place your color image (e.g., `pikachu.jpg`) in the root directory (ensure the name matches the python script).
2. Run the simulation using `make`:
```bash
make
```
3. Check the root directory for the hardware-processed `output_gray.jpg`!

## 🖼️ Before & After (Hardware Processing)

Here is the result of the image being processed pixel-by-pixel through the SystemVerilog hardware accelerator via AXI4-Stream:

| Original Input (`pikachu.jpg`) | Hardware Output (`output_gray.jpg`) |
| :---: | :---: |
| <img src="pikachu.jpg" width="400"> | <img src="output_gray.jpg" width="400"> |