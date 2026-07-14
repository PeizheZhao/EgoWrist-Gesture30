# 数据获取

GitHub 仓库提供标注、文档和工具。由于体积较大，手背侧 RGB、手掌侧 RGB 和 WT61C-TTL 测量数据通过独立数据包分发。

数据获取地址、版本、文件大小和 SHA-256 校验值记录在 [`../../data/download_links.json`](../../data/download_links.json)。数据包应解压到 Git 仓库之外。

```text
dataset-root/subjectXX/sceneY/recording_id/
├── dorsal/*.jpg
├── palm/*.jpg
└── sensor/sensor.csv
```

下载后的完整性验证方法见 [USAGE.md](USAGE.md)。数据分发问题可发送至 `zhaopeizhepro@outlook.com`。
