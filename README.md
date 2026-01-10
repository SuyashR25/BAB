# 2-DoF Planar Scribe Bot - ROS2 & CoppeliaSim Integration

Event: IIT Dharwad PARSEC | Build-a-Bot Senior PS (Round 1)

Project: The Virtual Scribe

System: ROS2 jazzy (WSL2) + CoppeliaSim Edu (Windows)

## 1. Project Overview

This project implements a 2-Degree-of-Freedom (2-DoF) Planar Plotter simulation capable of writing/drawing on a 2D surface. The system bridges two distinct environments: ROS2 jazzy running on WSL (Ubuntu 24.04)  and CoppeliaSim running on Windows. Control is achieved via standard keyboard teleoperation, with a custom Python bridge translating ROS messages into ZeroMQ (ZMQ) commands to drive the simulation in real-time.

## 2. Prerequisites

### Windows Side

- Simulator: CoppeliaSim Edu (Version 4.5 or later)
- Network: Firewall must allow incoming connections on port 23000 (default ZMQ port).
 {if needed turn off the firewall or add a new rule for port 23000 in Advanced network settings}

### WSL Side (Ubuntu 24.04)

- ROS2 Distribution:  Jazzy Jalisco
- Python: 3.10+
- Dependencies:

```bash
sudo apt install ros-jazzy-teleop-twist-keyboard
python3 -m venv venv ( Virtual Environment Setup )
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Directory Structure

Ensure your workspace is organized as follows:

```
BAB_SUBMISSION/
├─ src/
│  └─ scribe_bot/
│     ├─ resource/
│     │  └─ scribe_bot/
│     ├─ scribe_bot/
│     │  ├─ __init__.py
│     │  └─ scribe_bridge.py
│     └─ test/
│        ├─ test_copyright.py
│        ├─ test_flake8.py
│        └─ test_pep257.py
├─ package.xml
├─ setup.cfg
├─ setup.py
├─ README.md
├─ requirements.txt
├─ Screen Recording 2026-01-09 235402.mp4
└─ Sketcher-2-dof.ttt
```

## 4. Installation & Setup
Ensure ROS2 Jazzy is installed. If not then install by following this link:
https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html

### Step 1: Configure the Network Bridge (Critical)

Since WSL and Windows communicate over a virtual network, you must tell the Python script where Windows is located.

**Find Windows IP:**

Run this command inside your powershell terminal:

ipconfig

Copy the IP address listed next to IPV4 (e.g., 172.23.112.1).

**Update the Bridge Script:**

Open BAB_sbmission/src/scribe_bot/scribe_bot/scribe_bridge.py and update line 10:

```python
WINDOWS_IP = '172.xx.xx.1' 
```

> Note: This IP may change if you restart your computer/WSL.

### Step 2: Configure CoppeliaSim

Open Scribe_Bot_Scene.ttt in CoppeliaSim.

Ensure the Object Hierarchy matches the script's expectations:

```
Base -> X_joint -> X_link -> Y_joint -> ...
```

Attach the Lua Script (provided in submission) to the Base object to handle pen tracing and drawing.

### Step 3: Build the ROS2 Package

```bash
cd ~/BAB_submission
source /opt/ros/jazzy/setup.bash
```

## 5. Execution Guide

Follow this specific order to avoid connection errors.

1. **Start Simulation (Windows)**
   - Open CoppeliaSim and press the Play button.
   - Verification: The bottom status bar should display "SCRIBE BOT: System Initialization...".

2. **Start the Bridge (WSL Terminal 1)**
   - This node connects ROS to the Simulator.

```bash
colcon build
source install/setup.bash
ros2 run scribe_bot scribe_bridge
```

Verification: Output should say ✅ Connected to Windows... and ✅ Joint Handles Found.

3. **Start Controller (WSL Terminal 2)**
   - This node captures your keyboard input.

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

## 6. Control Guide (Custom Remapping)

The inputs have been remapped to function as a 2D Planar Plotter rather than a driving robot. You do not need to hold Shift.

### Basic Movement

| Key | Direction | Logic Map |
| --- | --- | --- |
| i | Move UP | Maps Linear.X to Y-Axis (+) |
| , | Move DOWN | Maps Linear.X to Y-Axis (-) |
| l | Move RIGHT | Maps Angular.Z to X-Axis (+) |
| j | Move LEFT | Maps Angular.Z to X-Axis (-) |
| k | STOP | Halts all motors |

### Advanced Shapes (Diagonal Drawing)

Use these keys to draw stars, diamonds, or diagonals.

| Key | Direction |
| --- | --- |
| o | Diagonal Up-Right ↗️ |
| u | Diagonal Up-Left ↖️ |
| . | Diagonal Down-Right ↘️ |
| m | Diagonal Down-Left ↙️ |

## 7. Troubleshooting

"Connection Refused":

- Did you update the WINDOWS_IP in the Python script?
- Is CoppeliaSim running (Play button pressed)?
- Is Windows Firewall blocking python?

"Joints Not Found":

- Check the Scene Hierarchy in CoppeliaSim. The script looks for /Base/X_joint and /Base/X_joint/X_link/Y_joint. If your hierarchy differs, update the paths in scribe_bridge.py.

Robot moves erratically:

- Ensure you aren't holding the key down if the repeat rate is too high. Tap k to stabilize.

## 8. Submission Checklist

- [x] ROS2 Package (scribe_bot)
- [x] CoppeliaSim Scene (.ttt) with Lua scripts
- [x] Python Bridge Code (scribe_bridge.py)
- [x] README.md (This file)
- [x] 2-Minute Demo Video Link

- Submitted by: BT_ke_bacche
- Track : senior
- Link To the Demonstration : https://youtu.be/Vq_coAOnuz4