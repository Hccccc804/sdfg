# 企业数字化转型指数查询与可视化

## 项目简介

这是一个基于Streamlit的企业数字化转型指数查询与可视化应用。该应用允许用户查询和分析企业的数字化转型指数，通过多种可视化图表展示数据趋势和分布情况。

## 功能特点

- **企业数字化转型指数查询**：根据股票代码和企业名称查询企业的数字化转型指数
- **历年指数趋势分析**：展示企业历年数字化转型指数和排名变化
- **统计排行展示**：
  - 当年数字化转型指数Top 10企业
  - 企业历年指数排名变化
- **数据概览**：
  - 数据集统计信息
  - 当前企业详细数据
- **数据可视化**：
  - 数字化转型指数整体分布直方图
  - 历年平均数字化转型指数趋势折线图
  - 数字化转型指数级别分布饼图
  - 技术维度与应用维度相关性散点图
  - 各年份数字化转型指数分布箱线图
- **详细统计分析**：提供数字化转型指数的详细统计信息

## 数据来源

数据来自于"两版合并后的年报数据_完整版.xlsx"文件，包含了中国上市公司的数字化转型相关数据，主要字段包括：

- 股票代码
- 企业名称
- 年份
- 人工智能词频数
- 大数据词频数
- 云计算词频数
- 区块链词频数
- 数字技术运用词频数
- 技术维度
- 应用维度
- 词总
- 数字化转型指数

## 技术栈

- **Streamlit**：Web应用框架
- **Pandas**：数据处理
- **Plotly**：数据可视化

## 环境要求

- Python 3.7+
- pip

## 安装与运行

### 1. 克隆仓库

```bash
git clone <your-repository-url>
cd <repository-directory>
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行应用

```bash
streamlit run digital_transformation_app.py
```

应用将在本地启动，访问地址为：http://localhost:8501

## 部署到Streamline Code

### 1. 在GitHub上创建仓库

将项目文件提交到GitHub仓库：

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repository-url>
git push -u origin main
```

### 2. 在Streamline Code上部署

1. 登录Streamline Code
2. 创建新的应用
3. 连接到你的GitHub仓库
4. 选择部署分支（通常为main）
5. 设置部署命令：
   ```bash
   pip install -r requirements.txt && streamlit run digital_transformation_app.py --server.port 8000 --server.headless true
   ```
6. 配置环境变量（如果需要）
7. 点击部署按钮

## 项目结构

```
.
├── digital_transformation_app.py  # 主应用文件
├── test_data.py                  # 数据测试文件
├── 两版合并后的年报数据_完整版.xlsx    # 数据源文件
├── requirements.txt              # 依赖列表
├── README.md                     # 项目说明文档
└── .gitignore                    # Git忽略文件
```

## 使用说明

1. 在侧边栏输入股票代码或企业名称进行搜索
2. 选择查询年份
3. 点击查询按钮
4. 查看企业数字化转型指数和相关分析
5. 浏览统计排行、数据概览和可视化图表

## 注意事项

- 确保数据源文件"两版合并后的年报数据_完整版.xlsx"与应用程序在同一目录下
- 如果遇到数据加载问题，请检查文件路径和文件格式
- 首次运行时，应用程序会缓存数据以提高后续访问速度

## 许可证

MIT License
