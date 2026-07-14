<div align="center">
  <h1>EgoWrist-Gesture30</h1>
  <h3>面向动态手势识别的双视角腕戴式 RGB–IMU 数据集</h3>
  <p>
    <a href="https://peizhezhao.github.io/EgoWrist-Gesture30/"><img src="https://img.shields.io/badge/Webpage-EgoWrist--Gesture30-1f883d?logo=googlechrome&amp;style=flat-square" alt="项目网页"></a>
    <a href="https://forms.office.com/r/EqiJNLWgtF"><img src="https://img.shields.io/badge/Data_Access-申请获取-0969da?logo=microsoftforms&amp;style=flat-square" alt="申请获取数据"></a>
    <a href="docs/zh-CN/USAGE.md"><img src="https://img.shields.io/badge/Documentation-使用指南-8250df?logo=readthedocs&amp;style=flat-square" alt="使用指南"></a>
    <a href="README.md"><img src="https://img.shields.io/badge/README-English-d73a49?style=flat-square" alt="English README"></a>
  </p>
</div>

## 数据集简介

EgoWrist-Gesture30 使用两路互补的腕部 RGB 摄像头和 WT61C-TTL IMU 记录动态手势，包含 30 个手势类别、13 位参与者和 336 段室内外录制，设备佩戴于右腕。

EgoWrist 论文使用 RGB 模态开展实验；完整数据集同时保留 IMU 数据，便于多模态与传感器融合研究。两路摄像头采用软件近似同步，历史 IMU 文件不支持精确的 RGB 帧级对齐。

本 GitHub 仓库提供标注、文档、采集程序、处理工具和验证工具。RGB 图片与已采集的 IMU 文件通过外部数据包分发；如需获取录制数据，请提交[数据集访问申请表](https://forms.office.com/r/EqiJNLWgtF)。

![30 类动态手势的手背侧与手掌侧腕部视角](docs/assets/gesture_overview.gif)

*30 个手势类别示例。每个单元同时展示一段标注录制的手背侧（dorsal）与手掌侧（palm）视角。*

## 核心统计

| 项目 | 数量或配置 |
|---|---:|
| 参与者 | 13 |
| 手势类别 | 30 |
| 原始录制 | 336 |
| 规范原始标注区间 | 2,751 |
| balanced 派生区间 | 4,255 |
| RGB 数据流 | 手背侧与手掌侧腕部视角 |
| 名义帧率 | 12 FPS |
| IMU | WT61C-TTL |
| 摄像头同步 | 软件近似同步 |
| 官方训练/验证/测试划分 | 无 |

2,751 条原始区间构成规范标注集；4,255 条 balanced 区间支持类别均衡采样，但不规定实验划分。跨用户评估建议采用参与者互斥划分。

## 数据分布

![balanced 手势类别分布](docs/assets/Gesture%20Label%20Occurrences_Balanced.png)

![balanced 手势平均持续帧数](docs/assets/Average%20Duration%20Frames_Balanced.png)

balanced 标注集包含 30 个手势类别和 4,255 个时间区间。图中分别给出各类别的区间数量和平均持续帧数。

## 数据组织

```text
EgoWrist-Gesture30/
├── annotations/                  # CSV 与聚合 JSON 标注
├── data/                         # 外部数据获取元数据
├── docs/                         # 数据规范和操作指南
└── tools/                        # 采集、处理、复核和验证工具
```

外部录制数据与标注使用相同的身份层级：

```text
dataset-root/subjectXX/sceneY/recording_id/
├── dorsal/*.jpg                  # 手背侧腕部视角
├── palm/*.jpg                    # 手掌侧腕部视角
└── sensor/sensor.csv
```

原始 CSV 标注采用 `begin,end,label` 三列，起止帧均包含在区间内，类别编号为 0–29。完整类别表见 [`annotations/classes.csv`](annotations/classes.csv)，详细格式见 [`docs/DATA_FORMAT.md`](docs/DATA_FORMAT.md)。

## 文档导航

| | 文档入口 |
|---:|---|
| 📐 | **[数据格式](docs/DATA_FORMAT.md)**<br><sub>标注语义、RGB 目录与 IMU 字段</sub> |
| 📦 | **[数据获取](docs/zh-CN/DATA_ACCESS.md)**<br><sub>访问申请、外部数据包与完整性信息</sub> |
| 🚀 | **[使用指南](docs/zh-CN/USAGE.md)**<br><sub>环境安装、标注读取、验证与处理</sub> |
| 📷 | **[采集指南](docs/zh-CN/ACQUISITION.md)**<br><sub>双摄像头与 WT61C-TTL 采集流程</sub> |
| 🔍 | **[质量复核](docs/REVIEW.md)**<br><sub>视频生成与本地 Web 标注复核</sub> |
| 🔧 | **[硬件与同步](docs/HARDWARE.md)**<br><sub>设备参数、测量单位与同步限制</sub> |

## 使用范围与许可证

本仓库不包含已采集图片、已采集传感器 CSV、生成视频、预定义论文划分、训练代码或模型权重。

数据集用于手势识别研究，不应用于身份识别、生物特征画像或监控。仓库工具采用 [MIT License](LICENSE-CODE)；标注与外部录制数据的使用条款随数据分发提供。
