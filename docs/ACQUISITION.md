# Multimodal acquisition guide

The acquisition utility records two wrist-mounted RGB streams and one WT61C-TTL IMU stream.

## Hardware

- Two HBVCAM-1466 V22 cameras with 160° fixed-focus, 1.66 mm lenses
- One WT61C-TTL IMU
- A computer exposing both cameras and the IMU serial interface
- A stable right-wrist mounting assembly

The collection system and synchronization limitations are specified in [HARDWARE.md](HARDWARE.md).

## Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Check camera indexes

```bash
python tools/acquisition/camera_check.py \
  --camera-a 0 \
  --camera-b 1 \
  --width 1920 \
  --height 1080
```

Press `q` or Escape to close the preview. Check view orientation, focus, exposure, obstruction, actual resolution, and observed frame rate.

## Identify the IMU serial port

Typical port names are `/dev/ttyUSB0` on Linux, `/dev/tty.usbserial-*` on macOS, and `COM15` on Windows. The standard acquisition configuration uses 115200 baud.

## Capture a recording

```bash
python tools/acquisition/capture_multimodal.py \
  --subject subject14 \
  --scene scene1 \
  --recording 1 \
  --palm-camera 0 \
  --dorsal-camera 1 \
  --imu-port /dev/ttyUSB0 \
  --imu-baudrate 115200 \
  --fps 12 \
  --width 1920 \
  --height 1080 \
  --duration 10 \
  --output captures
```

The command creates:

```text
captures/subject14/scene1/1/
├── palm/                        # sequential JPEG frames
├── dorsal/                      # sequential JPEG frames
├── sensor/sensor.csv            # timestamped WT61C-TTL measurements
└── frames.csv                   # polling and camera read timestamps
```

Existing recording directories are not overwritten. Camera threads maintain independent latest-frame buffers, and a shared loop writes the most recent pair at the requested cadence. This is approximate software synchronization, not hardware triggering.

## Inspect IMU output

```bash
python tools/acquisition/inspect_imu.py \
  captures/subject14/scene1/1/sensor/sensor.csv
```

Before accepting a recording, verify:

- both image streams are complete and visually usable;
- achieved resolution and frame rate match the protocol;
- camera offsets in `frames.csv` are within the study tolerance;
- IMU rows contain valid acceleration, angular velocity, and angle values;
- the performed gesture and recording identity are correct.

Recordings created with this utility include host timestamps for synchronization analysis. The timestamps do not imply hardware-level RGB–IMU synchronization.
