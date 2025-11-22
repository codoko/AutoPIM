#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的应用测试脚本
"""

import os
import sys
import json
from datetime import datetime

def create_test_data():
    """创建测试数据文件"""
    
    # 创建测试数据目录
    test_dir = "test_data"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # 创建CHECKERLIST.txt测试文件
    checker_list = [
        {
            "userid": "user001",
            "username": "testuser",
            "usercode": "testcode123",
            "name": "测试用户"
        },
        {
            "userid": "user002", 
            "username": "admin",
            "usercode": "admin456",
            "name": "管理员"
        }
    ]
    
    with open(os.path.join(test_dir, "CHECKERLIST.txt"), "w", encoding="utf-8") as f:
        json.dump(checker_list, f, ensure_ascii=False, indent=2)
    
    # 创建TASK.txt测试文件
    task_data = [
        {
            "task_id": "task001",
            "task_name": "设备巡检任务1",
            "task_code": "INS001",
            "scheduled_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending"
        },
        {
            "task_id": "task002",
            "task_name": "设备巡检任务2", 
            "task_code": "INS002",
            "scheduled_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending"
        }
    ]
    
    with open(os.path.join(test_dir, "TASK.txt"), "w", encoding="utf-8") as f:
        json.dump(task_data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 测试数据已创建在 {test_dir} 目录")
    return test_dir

def test_login_validation():
    """测试登录验证逻辑"""
    
    print("\n=== 测试登录验证 ===")
    
    # 模拟测试数据
    test_cases = [
        {"username": "", "usercode": "", "password": "", "expected": False},
        {"username": "testuser", "usercode": "", "password": "12138", "expected": False},
        {"username": "", "usercode": "testcode123", "password": "12138", "expected": False},
        {"username": "testuser", "usercode": "testcode123", "password": "wrong", "expected": False},
        {"username": "testuser", "usercode": "testcode123", "password": "12138", "expected": True},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        username = test_case["username"]
        usercode = test_case["usercode"]
        password = test_case["password"]
        expected = test_case["expected"]
        
        # 模拟验证逻辑
        is_valid = True
        if not username:
            is_valid = False
        elif not usercode:
            is_valid = False
        elif password != "12138":
            is_valid = False
        
        result = "✓ 通过" if is_valid == expected else "✗ 失败"
        print(f"测试 {i}: {result}")
        print(f"  输入: username={username}, usercode={usercode}, password={password}")
        print(f"  预期: {expected}, 实际: {is_valid}\n")

def test_data_loading():
    """测试数据加载功能"""
    
    print("=== 测试数据加载 ===")
    
    test_dir = create_test_data()
    
    # 测试CHECKERLIST加载
    try:
        checker_path = os.path.join(test_dir, "CHECKERLIST.txt")
        with open(checker_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            checker_list = json.loads(content)
        
        print(f"✓ CHECKERLIST加载成功，共{len(checker_list)}个检查员")
        
        # 测试用户查找
        test_username = "testuser"
        test_usercode = "testcode123"
        
        found = False
        for checker in checker_list:
            if (checker.get('username') == test_username and 
                checker.get('usercode') == test_usercode):
                found = True
                print(f"✓ 找到用户: {checker.get('name')} (ID: {checker.get('userid')})")
                break
        
        if not found:
            print("✗ 未找到测试用户")
            
    except Exception as e:
        print(f"✗ CHECKERLIST加载失败: {e}")
    
    # 测试TASK文件加载
    try:
        task_path = os.path.join(test_dir, "TASK.txt")
        with open(task_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            task_data = json.loads(content)
        
        print(f"✓ TASK文件加载成功，共{len(task_data)}个任务")
        
        for task in task_data:
            print(f"  - {task.get('task_name')} ({task.get('task_code')})")
            
    except Exception as e:
        print(f"✗ TASK文件加载失败: {e}")

def main():
    """主测试函数"""
    
    print("巡检自动化应用测试")
    print("=" * 50)
    
    # 测试登录验证
    test_login_validation()
    
    # 测试数据加载
    test_data_loading()
    
    print("\n测试完成！")
    print("\n下一步:")
    print("1. 将项目上传到GitHub")
    print("2. 配置GitHub Actions")
    print("3. 构建APK文件")
    print("4. 在Android设备上安装测试")

if __name__ == "__main__":
    main()