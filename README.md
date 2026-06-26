# 巡检自动化 - Android APK

将 `kimi.py` 打包为 Android APK，带图形界面。

## 项目结构

```
kimi_apk/
├── main.py              # Kivy GUI 主程序（原 kimi.py 的 Android 版）
├── buildozer.spec       # APK 构建配置
├── build.sh             # 一键构建脚本
├── icon.png             # 应用图标
├── presplash.png        # 启动画面
├── .github/workflows/
│   └── build.yml        # GitHub Actions 自动构建
└── README.md
```

## 构建方式

### 方式一：GitHub Actions 云构建（推荐，无需本地环境）

1. 创建 GitHub 仓库，将 `kimi_apk/` 目录内容推送到仓库根目录
2. 推送后自动触发构建，或手动在 Actions 页面触发
3. 构建完成后在 Actions → Artifacts 下载 APK

### 方式二：本地构建（Linux/WSL）

```bash
# 1. 安装依赖
sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev cmake \
    libffi-dev libssl-dev
pip3 install buildozer cython

# 2. 构建
cd kimi_apk
chmod +x build.sh
./build.sh

# 3. APK 输出在 bin/ 目录
```

### 方式三：Google Colab（免费云端）

```python
# 在 Colab notebook 中执行：
!pip install buildozer cython
!sudo apt-get install -y autoconf libtool pkg-config zlib1g-dev \
    libncurses5-dev cmake libffi-dev libssl-dev openjdk-17-jdk
!git clone <你的仓库地址>
%cd <仓库目录>
!buildozer android debug
# 下载 bin/ 下的 .apk 文件
```

## 使用说明

1. 安装 APK 到安卓手机
2. 将巡检数据文件放到手机目录：
   ```
   /storage/emulated/0/widgetone/apps/NormalPIM/data/
   ├── CHECKERLIST.txt          # 用户列表 (JSON)
   ├── TASK.txt                 # 任务列表 (JSON)
   └── TASKITEMLIST<code>.txt   # 任务项 (JSON)
   ```
3. 打开应用，输入用户名和用户代码
4. 点击「开始执行巡检」

## 权限说明

APK 需要以下权限：
- `READ_EXTERNAL_STORAGE` - 读取数据文件
- `WRITE_EXTERNAL_STORAGE` - 写入更新后的数据文件
- `MANAGE_EXTERNAL_STORAGE` - Android 11+ 完整文件访问

> Android 11+ 首次运行需在设置中授予「所有文件访问权限」
