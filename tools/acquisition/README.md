# Multimodal acquisition

`capture_multimodal.py` records two RGB streams and one WT61C-TTL IMU stream.

Install hardware dependencies from the repository root:

```bash
python -m pip install -r requirements.txt
```

Example:

```bash
python tools/acquisition/capture_multimodal.py \
  --subject subject14 \
  --scene scene1 \
  --recording 1 \
  --palm-camera 0 \
  --dorsal-camera 1 \
  --imu-port /dev/ttyUSB0 \
  --fps 12 \
  --width 1920 \
  --height 1080 \
  --duration 10 \
  --output captures
```

The program refuses to overwrite an existing recording. Camera threads continuously update latest-frame buffers; a shared polling loop writes an approximate pair at the requested cadence. `frames.csv` records each camera read timestamp and the observed offset. IMU rows include host-generated nanosecond timestamps.

Camera indexes, serial ports, actual resolution, and achieved frame rate are system-dependent and must be checked before a collection session.
