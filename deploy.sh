#!/bin/bash

# GitHub仓库部署脚本
# 使用方法: bash deploy.sh

echo "🚀 开始部署到GitHub..."

# 1. 初始化Git仓库（如果还没有初始化）
if [ ! -d ".git" ]; then
    echo "📦 初始化Git仓库..."
    git init
    echo "✅ Git仓库初始化完成"
else
    echo "✅ Git仓库已存在"
fi

# 2. 添加所有文件
echo "📁 添加文件到Git..."
git add .

# 3. 输入提交信息
echo "💬 请输入提交信息（直接回车使用默认信息）:"
read commit_message
if [ -z "$commit_message" ]; then
    commit_message="🚀 更新企业数字化转型指数查询系统 - $(date +'%Y-%m-%d %H:%M:%S')"
fi

echo "📝 提交更改: $commit_message"
git commit -m "$commit_message"

# 4. 获取远程仓库URL
echo "🔗 请输入您的GitHub仓库URL（例如: https://github.com/用户名/仓库名.git）:"
read repo_url

if [ -z "$repo_url" ]; then
    echo "❌ 错误: 必须提供GitHub仓库URL"
    exit 1
fi

# 5. 添加远程仓库
echo "🔧 配置远程仓库..."
git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"

# 6. 推送代码
echo "🚀 推送到GitHub..."
echo "请选择要推送的分支:"
echo "1. main"
echo "2. master"
read branch_choice

if [ "$branch_choice" = "2" ]; then
    branch="master"
else
    branch="main"
fi

echo "🌿 推送到 $branch 分支..."
git push -u origin "$branch"

echo ""
echo "✅ 部署完成！"
echo ""
echo "📋 下一步操作:"
echo "1. 访问 https://streamlit.io/cloud"
2. 使用GitHub账号登录
3. 点击'New app'选择您的仓库
4. 主文件路径填写: streamlit_app.py
5. 点击'Deploy'开始部署
echo ""
echo "🔗 GitHub仓库链接: $repo_url"
