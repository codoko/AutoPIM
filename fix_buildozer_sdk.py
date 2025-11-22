#!/usr/bin/env python3
"""
修复 Buildozer SDK 路径问题的脚本
"""

import os
import sys
import shutil
from pathlib import Path

def fix_buildozer_sdk():
    """修复 Buildozer SDK 路径问题"""
    
    # 获取当前用户的主目录
    home_dir = Path.home()
    
    # 实际的 SDK 安装路径
    real_sdk_path = home_dir / "android-sdk"
    
    # Buildozer 期望的 SDK 路径
    buildozer_sdk_path = home_dir / ".buildozer" / "android" / "platform" / "android-sdk"
    
    print(f"实际 SDK 路径: {real_sdk_path}")
    print(f"Buildozer SDK 路径: {buildozer_sdk_path}")
    
    # 确保 Buildozer 目录存在
    buildozer_sdk_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 如果符号链接已存在，先删除
    if buildozer_sdk_path.exists():
        if buildozer_sdk_path.is_symlink():
            buildozer_sdk_path.unlink()
            print("已删除旧的符号链接")
        else:
            print("警告: Buildozer SDK 路径已存在且不是符号链接")
            return False
    
    # 创建符号链接
    try:
        buildozer_sdk_path.symlink_to(real_sdk_path)
        print(f"✓ 成功创建符号链接: {buildozer_sdk_path} -> {real_sdk_path}")
    except Exception as e:
        print(f"✗ 创建符号链接失败: {e}")
        return False
    
    # 验证符号链接
    if buildozer_sdk_path.is_symlink() and buildozer_sdk_path.resolve() == real_sdk_path:
        print("✓ 符号链接验证通过")
    else:
        print("✗ 符号链接验证失败")
        return False
    
    # 验证 build-tools 目录
    build_tools_path = buildozer_sdk_path / "build-tools"
    if build_tools_path.exists():
        print(f"✓ build-tools 目录存在: {build_tools_path}")
        print("可用的 build-tools 版本:")
        for version_dir in build_tools_path.iterdir():
            if version_dir.is_dir():
                print(f"  - {version_dir.name}")
    else:
        print("✗ build-tools 目录不存在")
        return False
    
    # 验证 aidl 工具
    aidl_paths = [
        buildozer_sdk_path / "build-tools" / "33.0.0" / "aidl",
        buildozer_sdk_path / "build-tools" / "36.1.0" / "aidl",
    ]
    
    aidl_found = False
    for aidl_path in aidl_paths:
        if aidl_path.exists():
            print(f"✓ aidl 工具找到: {aidl_path}")
            aidl_found = True
            break
    
    if not aidl_found:
        print("✗ aidl 工具未找到，搜索中...")
        aidl_files = list(buildozer_sdk_path.rglob("aidl"))
        if aidl_files:
            print("找到的 aidl 文件:")
            for aidl_file in aidl_files:
                print(f"  - {aidl_file}")
        else:
            print("  未找到任何 aidl 文件")
            return False
    
    # 设置环境变量
    os.environ["ANDROID_SDK_ROOT"] = str(real_sdk_path)
    os.environ["ANDROID_HOME"] = str(real_sdk_path)
    os.environ["PATH"] = f"{real_sdk_path}/cmdline-tools/latest/bin:{real_sdk_path}/platform-tools:{real_sdk_path}/build-tools/33.0.0:{os.environ.get('PATH', '')}"
    
    print(f"✓ 环境变量已设置:")
    print(f"  ANDROID_SDK_ROOT = {os.environ.get('ANDROID_SDK_ROOT')}")
    print(f"  ANDROID_HOME = {os.environ.get('ANDROID_HOME')}")
    
    return True

if __name__ == "__main__":
    print("开始修复 Buildozer SDK 路径问题...")
    success = fix_buildozer_sdk()
    
    if success:
        print("\n🎉 Buildozer SDK 路径修复完成！")
        print("现在可以运行 buildozer android debug 了")
    else:
        print("\n❌ Buildozer SDK 路径修复失败")
        print("请检查错误信息并手动修复")
        sys.exit(1)