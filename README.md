# 企业数字化转型指数查询系统

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 📊 项目介绍

本项目是一个基于Streamlit的企业数字化转型指数查询系统，可以可视化分析企业数字化转型指数数据，支持按股票代码和年份查询，展示数字化转型指数的趋势变化和分布情况。

### 主要功能

- **数据概览**：展示整体数据的统计信息，包括平均指数、最大值、企业数量和年份范围
- **企业查询**：通过股票代码搜索特定企业，查看其数字化转型指数
- **趋势分析**：展示企业历年的数字化转型指数变化趋势
- **指数分布**：展示企业数字化转型指数的区间分布和各年份的平均水平
- **排名对比**：展示企业平均数字化转型指数的排名情况（TOP20）

## 🚀 部署说明

### 方法一：Streamlit Cloud部署（推荐）

1. **准备GitHub仓库**
   - 创建新的GitHub仓库
   - 将本项目文件上传到仓库

2. **配置Streamlit Cloud**
   - 访问 [Streamlit Cloud](https://streamlit.io/cloud)
   - 使用GitHub账号登录
   - 点击"New app"
   - 选择您的GitHub仓库
   - 选择分支（通常为main或master）
   - 主文件路径填写：`streamlit_app.py`
   - 点击"Deploy"

3. **配置数据文件**
   - 将 `两版合并后的年报数据_完整版.xlsx` 上传到GitHub仓库
   - 代码会自动从仓库加载数据

### 方法二：本地运行

```bash
# 1. 克隆仓库
git clone <your-repository-url>
cd <repository-name>

# 2. 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行应用
streamlit run streamlit_app.py
```

## 📁 项目结构

```
年报合并数据/
├── streamlit_app.py           # Streamlit主应用文件
├── requirements.txt           # Python依赖包列表
├── 两版合并后的年报数据_完整版.xlsx  # 数据文件
├── README.md                  # 项目说明文档
├── .gitignore                 # Git忽略文件配置
└── .streamlit/
    └── config.toml            # Streamlit配置（可选）
```

## 🔧 配置说明

### Streamlit配置（可选）

在项目根目录创建 `.streamlit/config.toml` 文件：

```toml
[server]
port = 8501
headless = true

[browser]
gatherUsageStats = false
```

### 数据文件要求

- 文件格式：Excel文件（.xlsx）
- 必需列：
  - `股票代码`：企业股票代码
  - `企业名称`：企业名称
  - `年份`：数据年份
  - `数字化转型指数`：数字化转型指数值

## 📦 依赖包

```
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
openpyxl>=3.1.0
```

## 🤝 贡献指南

1. Fork本项目
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

## 👨‍💻 作者

您的名字

## 📞 联系方式

如果您有任何问题或建议，请通过以下方式联系：
- 创建 [Issue](https://github.com/yourusername/your-repo/issues)
- 发送邮件至：your-email@example.com
