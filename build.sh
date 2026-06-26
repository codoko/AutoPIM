#!/bin/bash
# ============================================
# 巡检自动化 APK 构建脚本
# 支持: Linux (Ubuntu/Debian) 或 GitHub Actions
# ============================================

set -e

echo "========================================="
echo "  巡检自动化 APK 构建"
echo "========================================="

# 1. 系统依赖
echo "[1/5] 安装系统依赖..."
sudo apt-get update -qq
sudo apt-get install -y -qq \
    git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev \
    libncurses5-dev libncursesw5-dev cmake \
    libffi-dev libssl-dev 2>/dev/null

# 2. Python 依赖
echo "[2/5] 安装 Python 依赖..."
pip3 install --upgrade pip buildozer cython 2>/dev/null

# 3. 构建 APK
echo "[3/5] 开始构建 APK (首次约 30-60 分钟)..."
cd "$(dirname "$0")"
buildozer android debug

# 4. 输出
APK_PATH=$(find bin -name "*.apk" | head -1)
if [ -n "$APK_PATH" ]; then
    echo ""
    echo "========================================="
    echo "  ✅ 构建成功!"
    echo "  APK: $APK_PATH"
    echo "  大小: $(du -h "$APK_PATH" | cut -f1)"
    echo "========================================="
else
    echo "❌ 构建失败，请检查日志"
    exit 1
fi
