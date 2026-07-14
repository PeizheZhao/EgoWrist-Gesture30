# 多模态采集指南

采集程序记录手背侧 RGB、手掌侧 RGB 和 WT61C-TTL IMU。

## 设备与检查

- 两个 HBVCAM-1466 V22 摄像头，160° 定焦，焦距 1.66 mm；
- 一个 WT61C-TTL IMU，通常使用 115200 波特率；
- 稳定的右腕安装结构。

先运行摄像头预览并检查视角、焦点、曝光、分辨率和帧率：

```bash
python tools/acquisition/camera_check.py --camera-a 0 --camera-b 1
```

## 采集

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

程序输出两路连续图片、`sensor/sensor.csv` 和相机时间信息 `frames.csv`，并拒绝覆盖已有录制。两路摄像头采用软件近似同步，不是硬件触发同步。

完整参数、输出结构和质量检查要求见 [英文采集指南](../ACQUISITION.md)。
