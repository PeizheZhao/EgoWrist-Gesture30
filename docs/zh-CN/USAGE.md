# 使用指南

本指南说明标注读取、仓库验证和外部数据检查。采集流程见 [ACQUISITION.md](ACQUISITION.md)。

## 安装环境

标注验证只需 Python 3.10 或更高版本；图像、串口和 Web 工具需要安装可选依赖：

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

## 验证仓库

```bash
python tools/validation/validate_release.py
python -m unittest discover -s tools/validation/tests
```

规范统计为 30 类、336 个录制、2,751 条原始区间和 4,255 条 balanced 派生区间。

## 读取标注

原始 CSV 位于 `annotations/original/csv/`，列为 `begin,end,label`。起止帧均包含在区间内，类别编号范围是 0–29。聚合 JSON 提供相同原始标注，balanced JSON 是通用派生标注，不包含训练、验证或测试划分。

## 获取并验证外部数据

首先提交[数据集访问申请表](https://forms.office.com/r/EqiJNLWgtF)。申请获批后，请按照收到的分发说明获取数据，并将数据包解压到 Git 仓库之外。申请地址及已发布数据包的完整性元数据记录在 `data/download_links.json`。

然后验证解压后的数据包：

```bash
python tools/validation/validate_external_data.py /path/to/dataset-root \
  --dorsal-name dorsal \
  --palm-name palm \
  --sensor-relative sensor/sensor.csv
```

验证工具检查目录层级、两路 RGB、标注引用帧、IMU 文件及字段。

完整命令、Python 读取示例和标注再生成方法见 [英文使用指南](../USAGE.md)。
