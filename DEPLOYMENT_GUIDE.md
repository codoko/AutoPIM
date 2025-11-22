# 巡检自动化APK部署指南

## 概述

本指南将帮助您将Python巡检脚本成功打包成Android APK，并通过GitHub Actions实现自动构建。

## 快速开始

### 1. 项目准备

将所有文件上传到GitHub仓库：

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: Inspection automation Android app"

# 添加远程仓库
git remote add origin https://github.com/yourusername/inspection-automation-app.git

# 推送到GitHub
git push -u origin main
```

### 2. GitHub Actions自动构建

项目已配置GitHub Actions工作流，当代码推送到main分支时会自动构建APK。

#### 触发构建

1. 推送代码到main分支：
```bash
git push origin main
```

2. 在GitHub仓库的"Actions"标签页查看构建进度

3. 构建完成后，在"Actions"页面下载APK文件

#### 手动触发构建

1. 进入GitHub仓库的"Actions"页面
2. 选择"Build Android APK"工作流
3. 点击"Run workflow"按钮

### 3. 本地构建（可选）

如果您想在本地构建APK：

#### 环境准备

1. 安装系统依赖（Ubuntu/Debian）：
```bash
sudo apt-get update
sudo apt-get install -y python3-setuptools git zip unzip openjdk-8-jdk
```

2. 安装Python依赖：
```bash
pip install -r requirements.txt
```

3. 安装Android SDK：
```bash
# 下载Android SDK
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip commandlinetools-linux-9477386_latest.zip

# 设置环境变量
export ANDROID_SDK_ROOT=$HOME/android-sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools

# 接受许可证
yes | sdkmanager --licenses

# 安装SDK组件
sdkmanager "platforms;android-33" "build-tools;33.0.0" "platform-tools"
```

#### 构建APK

```bash
# 构建调试版APK
buildozer android debug

# 构建发布版APK
buildozer android release
```

构建完成后，APK文件将在`bin/`目录中。

## 应用安装和使用

### 1. 安装APK

1. 在Android设备上启用"未知来源"应用安装：
   - 设置 → 安全 → 未知来源 → 允许

2. 将APK文件传输到Android设备

3. 点击APK文件进行安装

### 2. 首次运行设置

1. 启动应用
2. 授予文件存储权限（重要）
3. 准备数据文件：
   - 在设备上创建目录：`/sdcard/Documents/inspection_data/`
   - 将CHECKERLIST.txt和TASK.txt文件放入该目录

### 3. 使用应用

1. **登录界面**：
   - 输入用户名
   - 输入用户代码
   - 输入默认密码：`12138`
   - 点击"登录"

2. **主界面**：
   - 确认数据目录路径
   - 点击"加载数据文件"
   - 点击"处理巡检任务"
   - 点击"生成报告"

## 故障排除

### 构建失败

#### GitHub Actions构建失败

1. 检查buildozer.spec配置是否正确
2. 查看Actions日志获取详细错误信息
3. 确保requirements.txt中的依赖版本兼容

#### 本地构建失败

1. 检查Java版本（需要JDK 8）
2. 确认Android SDK路径设置正确
3. 检查网络连接（构建过程需要下载依赖）

### 应用运行问题

#### 无法加载数据文件

1. 确认文件路径：`/sdcard/Documents/inspection_data/`
2. 检查文件权限（需要存储权限）
3. 验证JSON文件格式是否正确

#### 登录失败

1. 确认默认密码：`12138`
2. 检查用户名和用户代码是否在CHECKERLIST.txt中
3. 验证CHECKERLIST.txt格式

## 自定义配置

### 修改应用信息

编辑`buildozer.spec`文件：

```ini
# 应用名称
title = 您的应用名称

# 包名
package.name = yourappname

# 版本号
version = 1.0.0

# 权限
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
```

### 添加新功能

1. 修改`main.py`添加新功能
2. 更新`requirements.txt`添加新依赖
3. 重新构建APK

## 安全注意事项

1. **默认密码**：生产环境中建议修改默认密码
2. **数据安全**：敏感数据建议加密存储
3. **权限管理**：只申请必要的权限

## 最佳实践

1. **版本管理**：使用Git标签管理版本
2. **测试**：在多个Android版本上测试
3. **备份**：定期备份数据文件
4. **更新**：建立应用更新机制

## 技术支持

如有问题，请：

1. 查看GitHub Issues
2. 检查应用日志
3. 查看构建日志
4. 联系开发团队

## 更新日志

### v1.0.0
- 初始版本发布
- 基础登录功能
- 数据文件处理
- 任务自动化处理
- 报告生成功能