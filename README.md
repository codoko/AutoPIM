# 巡检自动化Android应用

这是一个基于Kivy框架的Android应用，用于自动化巡检任务处理。该应用将原始的Python巡检脚本打包成APK，方便在没有Termux和Python环境的Android设备上运行。

## 功能特性

- **安全登录界面**：需要输入用户名、用户代码和默认密码（12138）
- **数据文件管理**：支持加载CHECKERLIST.txt和TASK.txt文件
- **任务处理**：自动化处理巡检任务
- **报告生成**：生成巡检报告并保存
- **用户友好界面**：基于Kivy的现代UI设计

## 项目结构

```
.
├── main.py              # 主应用程序文件
├── buildozer.spec       # Buildozer配置文件
├── requirements.txt     # Python依赖包列表
├── README.md           # 项目说明文档
└── .github/
    └── workflows/
        └── build-apk.yml  # GitHub Actions工作流
```

## 登录信息

- **默认密码**: `12138`
- **用户名**: 您的巡检系统用户名
- **用户代码**: 您的巡检系统用户代码

## 数据文件要求

应用需要以下数据文件（放置在/sdcard/Documents/inspection_data/目录下）：

1. **CHECKERLIST.txt**: 检查员列表文件，JSON格式
2. **TASK.txt**: 巡检任务文件，JSON格式

## 构建APK

### 本地构建

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 构建APK：
```bash
buildozer android debug
```

### GitHub Actions自动构建

项目已配置GitHub Actions工作流，当推送到main分支时会自动构建APK。

1. 将项目推送到GitHub
2. 在GitHub的Actions标签页查看构建进度
3. 构建完成后，在Artifacts中下载APK文件

## 安装和运行

1. 在Android设备上启用"未知来源"应用安装
2. 下载并安装生成的APK文件
3. 首次运行时授予文件存储权限
4. 将数据文件放置在指定目录
5. 启动应用并登录

## 技术栈

- **Kivy**: 跨平台Python GUI框架
- **Buildozer**: Android应用打包工具
- **GitHub Actions**: 持续集成和自动构建

## 开发环境要求

- Python 3.9+
- Android SDK
- Buildozer
- Java JDK 8+

## 注意事项

1. 确保Android设备有足够的存储空间
2. 数据文件必须是有效的JSON格式
3. 应用需要文件读写权限来访问数据文件
4. 建议在使用前备份重要数据

## 故障排除

### 构建失败
- 检查requirements.txt中的依赖版本
- 确保buildozer.spec配置正确
- 查看GitHub Actions日志获取详细信息

### 应用运行问题
- 确认数据文件路径和格式正确
- 检查Android设备存储权限
- 查看应用日志获取错误信息

## 更新日志

### v1.0.0
- 初始版本
- 基础登录功能
- 数据文件加载
- 任务处理和报告生成