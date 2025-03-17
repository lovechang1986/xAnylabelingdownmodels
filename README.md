# X-AnyLabeling 模型下载器

这是一个用于批量下载 [X-AnyLabeling](https://github.com/CVHub520/X-AnyLabeling) 项目中所有预训练模型的Python脚本。

## 功能特点

- 自动克隆X-AnyLabeling仓库
- 解析所有yaml配置文件
- 自动下载所有模型文件
- 支持断点续传（已下载的文件会自动跳过）
- 显示下载进度条
- 自动创建对应的模型文件夹

## 使用方法

### 1. 安装依赖

```bash
pip install gitpython pyyaml requests tqdm
```

### 2. 运行脚本

```bash
python download_models.py
```

### 3. 文件结构

下载完成后，文件结构如下：
```
.
├── download_models.py
├── X-AnyLabeling/          # 克隆的原始仓库
└── downloaded_models/      # 下载的模型文件
    ├── model_name_1/      # 按yaml中的name分类
    │   ├── encoder.onnx
    │   └── decoder.onnx
    └── model_name_2/
        ├── encoder.onnx
        └── decoder.onnx
```

## 注意事项

- 确保有足够的磁盘空间
- 需要稳定的网络连接
- 部分模型文件较大，下载时间可能较长
- 如果下载中断，可以直接重新运行脚本继续下载

