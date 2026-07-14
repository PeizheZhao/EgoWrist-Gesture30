# Hardware and synchronization

## RGB cameras

- Model: HBVCAM-1466 V22
- Lens: fixed focus
- Focal length: 1.66 mm
- Nominal field of view: 160 degrees
- Product page: https://e.tb.cn/h.S0l7eVvCDHxlfDv?tk=0iQq4IfSHVQ

Two wrist-mounted cameras observe complementary palm and dorsal views. Capture operates at a nominal 12 FPS with a 1080p camera module. Distributed frame resolution is recorded in the data-package metadata and should be reported in experimental protocols.

## IMU

- Model: WT61C-TTL
- Serial protocol: WitMotion 0x51 acceleration, 0x52 angular velocity, and 0x53 Euler-angle packets
- Default serial baud rate in the acquisition utility: 115200
- Product page: https://e.tb.cn/h.SbiCjhPnVgCFaaa?tk=2XMT4IfORwJ

The WT61C-TTL protocol implementation decodes acceleration in `g`, angular velocity in `deg/s`, Euler angles in `deg`, and temperature in degrees Celsius. Dataset CSV files contain acceleration, angular velocity, and angle fields; files created by the acquisition utility also include temperature and host timestamps.

## Software-based approximate synchronization

The cameras are not hardware-trigger synchronized. Acquisition continuously updates a latest-frame buffer for each camera. A shared polling loop then obtains the most recently available frame from both buffers at a nominal common cadence. The resulting frame pairs are approximately synchronized in software and may have a non-zero temporal offset.

The IMU is collected during the same recording session. Dataset IMU CSV files use a row index and do not provide a trustworthy wall-clock timestamp, so exact frame-to-IMU alignment is not claimed. New recordings created with the acquisition utility include host timestamps for synchronization analysis.
