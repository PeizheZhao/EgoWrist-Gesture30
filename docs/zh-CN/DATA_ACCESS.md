# 数据获取

GitHub 仓库提供标注、文档和工具。由于体积较大，手背侧 RGB、手掌侧 RGB 和 WT61C-TTL 测量数据通过独立数据包分发。

## 申请访问

请填写 [EgoWrist Gesture 30 数据集访问申请表](https://forms.office.com/r/EqiJNLWgtF) 以申请录制数据包。表单需要填写姓名、机构或单位、联系邮箱，并确认数据集及其派生数据仅用于非商业的学术与科学研究，同时承诺不向第三方重新分发数据集。

数据访问将依据提交的信息进行审核。申请获批后，录制数据的分发说明将另行提供。[`../../data/download_links.json`](../../data/download_links.json) 以机器可读形式记录申请地址，以及已发布数据包的版本、文件大小和 SHA-256 信息。数据包应解压到 Git 仓库之外。

```text
dataset-root/subjectXX/sceneY/recording_id/
├── dorsal/*.jpg
├── palm/*.jpg
└── sensor/sensor.csv
```

收到并解压数据包后，完整性验证方法见 [USAGE.md](USAGE.md)。申请或数据分发问题可发送至 `zhaopeizhepro@outlook.com`。
