#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巡检自动化Android应用主程序
使用Kivy框架构建GUI界面
基于inspection_script2.py的完整功能实现
"""

import os
import json
import random
from datetime import datetime, timedelta
import re
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty

class LoginScreen(Screen):
    """登录界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """构建登录界面UI"""
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # 标题
        title_label = Label(
            text='巡检自动化系统',
            font_size=32,
            size_hint_y=None,
            height=60,
            color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(title_label)
        
        # 用户名输入
        username_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        username_layout.add_widget(Label(text='用户名:', size_hint_x=0.3, font_size=18))
        self.username_input = TextInput(
            multiline=False,
            size_hint_x=0.7,
            font_size=16,
            hint_text='请输入用户名'
        )
        username_layout.add_widget(self.username_input)
        layout.add_widget(username_layout)
        
        # 用户代码输入
        usercode_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        usercode_layout.add_widget(Label(text='用户代码:', size_hint_x=0.3, font_size=18))
        self.usercode_input = TextInput(
            multiline=False,
            size_hint_x=0.7,
            font_size=16,
            hint_text='请输入用户代码'
        )
        usercode_layout.add_widget(self.usercode_input)
        layout.add_widget(usercode_layout)
        
        # 默认密码输入
        password_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        password_layout.add_widget(Label(text='默认密码:', size_hint_x=0.3, font_size=18))
        self.password_input = TextInput(
            multiline=False,
            password=True,
            size_hint_x=0.7,
            font_size=16,
            hint_text='请输入默认密码'
        )
        password_layout.add_widget(self.password_input)
        layout.add_widget(password_layout)
        
        # 登录按钮
        login_button = Button(
            text='登录',
            size_hint_y=None,
            height=60,
            font_size=20,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        login_button.bind(on_press=self.validate_login)
        layout.add_widget(login_button)
        
        self.add_widget(layout)
    
    def validate_login(self, instance):
        """验证登录信息"""
        username = self.username_input.text.strip()
        usercode = self.usercode_input.text.strip()
        password = self.password_input.text.strip()
        
        if not username:
            self.show_error("用户名不能为空")
            return
        
        if not usercode:
            self.show_error("用户代码不能为空")
            return
        
        if password != "12138":
            self.show_error("默认密码错误")
            return
        
        # 验证通过，跳转到主界面
        app = App.get_running_app()
        app.user_info = {
            'username': username,
            'usercode': usercode
        }
        app.screen_manager.current = 'main'
    
    def show_error(self, message):
        """显示错误信息"""
        popup = Popup(
            title='错误',
            content=Label(text=message),
            size_hint=(0.8, 0.3),
            auto_dismiss=True
        )
        popup.open()

class MainScreen(Screen):
    """主功能界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inspection_app = None
        self.build_ui()
    
    def build_ui(self):
        """构建主界面UI"""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 用户信息显示
        app = App.get_running_app()
        user_info_label = Label(
            text=f'当前用户: {app.user_info.get("username", "")} ({app.user_info.get("usercode", "")})',
            font_size=16,
            size_hint_y=None,
            height=40,
            color=(0.2, 0.6, 1, 1)
        )
        layout.add_widget(user_info_label)
        
        # 数据目录显示（固定路径）
        dir_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        dir_layout.add_widget(Label(text='数据路径:', size_hint_x=0.3, font_size=16))
        self.dir_label = Label(
            text='/storage/emulated/0/widgetone/apps/NormalPIM/data',
            size_hint_x=0.7,
            font_size=14,
            halign='left',
            color=(0.3, 0.3, 0.3, 1)
        )
        dir_layout.add_widget(self.dir_label)
        layout.add_widget(dir_layout)
        
        # 操作按钮
        buttons_layout = BoxLayout(orientation='vertical', spacing=10)
        
        load_data_btn = Button(
            text='加载数据文件',
            size_hint_y=None,
            height=50,
            font_size=16,
            background_color=(0.3, 0.7, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        load_data_btn.bind(on_press=self.load_data)
        buttons_layout.add_widget(load_data_btn)
        
        process_tasks_btn = Button(
            text='处理巡检任务',
            size_hint_y=None,
            height=50,
            font_size=16,
            background_color=(0.7, 0.5, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        process_tasks_btn.bind(on_press=self.process_tasks)
        buttons_layout.add_widget(process_tasks_btn)
        
        generate_report_btn = Button(
            text='生成报告',
            size_hint_y=None,
            height=50,
            font_size=16,
            background_color=(0.5, 0.3, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        generate_report_btn.bind(on_press=self.generate_report)
        buttons_layout.add_widget(generate_report_btn)
        
        layout.add_widget(buttons_layout)
        
        # 状态显示
        self.status_label = Label(
            text='准备就绪',
            font_size=14,
            size_hint_y=None,
            height=120,
            color=(0.3, 0.3, 0.3, 1),
            halign='left',
            valign='top'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        layout.add_widget(self.status_label)
        
        # 退出按钮
        exit_btn = Button(
            text='退出登录',
            size_hint_y=None,
            height=40,
            font_size=14,
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        exit_btn.bind(on_press=self.logout)
        layout.add_widget(exit_btn)
        
        self.add_widget(layout)
    
    def load_data(self, instance):
        """加载数据文件"""
        # 使用固定的数据路径
        data_dir = '/storage/emulated/0/widgetone/apps/NormalPIM/data'
        
        if not os.path.exists(data_dir):
            self.show_status(f"错误: 数据目录不存在: {data_dir}\n")
            self.show_status("请确认路径 /storage/emulated/0/widgetone/apps/NormalPIM/data 是否存在\n")
            return
        
        try:
            self.inspection_app = InspectionAutomation(data_dir)
            
            # 加载CHECKERLIST
            if self.inspection_app.load_checker_list():
                self.show_status("✓ CHECKERLIST加载成功\n")
            else:
                self.show_status("✗ CHECKERLIST加载失败\n")
                return
            
            # 加载TASK文件
            if self.inspection_app.load_task_data():
                self.show_status("✓ TASK文件加载成功\n")
            else:
                self.show_status("✗ TASK文件加载失败\n")
                return
            
            # 设置当前用户信息
            app = App.get_running_app()
            self.inspection_app.user_info = app.user_info.copy()
            
            # 查找用户ID
            if self.inspection_app.find_user_id():
                self.show_status("✓ 用户验证成功，数据加载完成\n")
                self.show_status(f"当前数据目录: {data_dir}\n")
            else:
                self.show_status("✗ 用户验证失败，请检查用户信息\n")
                
        except Exception as e:
            self.show_status(f"错误: {str(e)}\n")
    
    def process_tasks(self, instance):
        """处理巡检任务"""
        if not self.inspection_app:
            self.show_status("请先加载数据文件\n")
            return
        
        try:
            self.show_status("开始处理巡检任务...\n")
            
            # 创建任务处理器
            processor = TaskProcessor(self.inspection_app)
            result = processor.process_all_tasks()
            
            # 保存处理结果到应用实例
            self.inspection_app.processed_tasks = processor.results
            
            self.show_status(result)
            
        except Exception as e:
            self.show_status(f"处理任务时出错: {str(e)}\n")
    
    def generate_report(self, instance):
        """生成报告"""
        if not self.inspection_app:
            self.show_status("请先加载数据文件\n")
            return
        
        try:
            self.show_status("正在生成报告...\n")
            
            # 生成完整的巡检报告
            report_generator = ReportGenerator(self.inspection_app)
            report_content = report_generator.generate_inspection_report()
            
            # 保存报告到文件
            report_file = os.path.join('/storage/emulated/0/widgetone/apps/NormalPIM/data', 'inspection_report.txt')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            self.show_status(f"✓ 报告已生成: {report_file}\n")
            
        except Exception as e:
            self.show_status(f"生成报告时出错: {str(e)}\n")
    
    def show_status(self, message):
        """显示状态信息"""
        current_text = self.status_label.text
        if current_text == '准备就绪':
            self.status_label.text = message
        else:
            self.status_label.text = current_text + message
    
    def logout(self, instance):
        """退出登录"""
        app = App.get_running_app()
        app.user_info = {}
        self.inspection_app = None
        self.status_label.text = '准备就绪'
        app.screen_manager.current = 'login'

# 以下是基于inspection_script2.py的核心功能类

class InspectionAutomation:
    """巡检自动化核心类 - 基于inspection_script2.py"""
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.checker_list = None
        self.task_data = None
        self.user_info = {}
        self.processed_tasks = []
        
    def load_checker_list(self):
        """加载CHECKERLIST文件"""
        checker_path = os.path.join(self.data_dir, "CHECKERLIST.txt")
        try:
            with open(checker_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                self.checker_list = json.loads(content)
                print(f"✓ 成功加载CHECKERLIST，共{len(self.checker_list)}个检查员")
                return True
        except Exception as e:
            print(f"✗ 加载CHECKERLIST失败: {e}")
            return False
    
    def load_task_data(self):
        """加载TASK文件"""
        task_path = os.path.join(self.data_dir, "TASK.txt")
        try:
            with open(task_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                self.task_data = json.loads(content)
                print(f"✓ 成功加载TASK文件，共{len(self.task_data)}个任务")
                return True
        except Exception as e:
            print(f"✗ 加载TASK文件失败: {e}")
            return False
    
    def find_user_id(self):
        """在CHECKERLIST中查找对应的userid"""
        if not self.checker_list:
            return False
            
        for checker in self.checker_list:
            if (checker.get('username') == self.user_info['username'] and 
                checker.get('usercode') == self.user_info['usercode']):
                self.user_info['userid'] = checker.get('userid')
                print(f"✓ 找到匹配的用户ID: {self.user_info['userid']}")
                return True
        
        print(f"✗ 在CHECKERLIST中未找到用户 {self.user_info['username']} ({self.user_info['usercode']})")
        return False
    
    def generate_random_time_offset(self, min_minutes, max_minutes):
        """生成随机时间偏移（分钟）"""
        return random.randint(min_minutes, max_minutes)
    
    def parse_datetime(self, datetime_str):
        """解析日期时间字符串"""
        try:
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        except:
            return None
    
    def format_datetime(self, dt):
        """格式化日期时间为字符串"""
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def process_task_item_file(self, task_code):
        """处理任务项文件"""
        try:
            task_item_path = os.path.join(self.data_dir, f"{task_code}_ITEM.txt")
            if os.path.exists(task_item_path):
                with open(task_item_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    return json.loads(content)
            return None
        except Exception as e:
            print(f"处理任务项文件时出错: {e}")
            return None
    
    def generate_inspection_time(self, base_time, task_offset):
        """生成巡检时间"""
        try:
            base_dt = self.parse_datetime(base_time)
            if not base_dt:
                return None
            
            # 添加任务偏移和随机偏移
            random_offset = self.generate_random_time_offset(-30, 30)
            final_dt = base_dt + timedelta(minutes=task_offset + random_offset)
            return self.format_datetime(final_dt)
        except Exception as e:
            print(f"生成巡检时间时出错: {e}")
            return None
    
    def get_user_input(self):
        """获取用户输入的username和usercode - 原始方法保留"""
        print("\n=== 巡检自动化脚本 ===")
        print("请输入您的用户信息:")
        
        # 这个方法在GUI中不会直接使用，但保留以保持一致性
        return self.user_info

class TaskProcessor:
    """任务处理器"""
    
    def __init__(self, inspection_app):
        self.inspection_app = inspection_app
        self.processed_count = 0
        self.total_count = 0
        self.results = []
    
    def process_all_tasks(self):
        """处理所有任务"""
        if not self.inspection_app.task_data:
            return "没有任务数据需要处理"
        
        self.total_count = len(self.inspection_app.task_data)
        self.processed_count = 0
        self.results = []
        
        result_text = f"开始处理 {self.total_count} 个巡检任务...\n"
        
        for i, task in enumerate(self.inspection_app.task_data):
            try:
                result = self.process_single_task(task, i)
                self.results.append(result)
                
                if result["success"]:
                    self.processed_count += 1
                    result_text += f"✓ 任务 {task.get('task_code', 'Unknown')} 处理成功\n"
                else:
                    result_text += f"✗ 任务 {task.get('task_code', 'Unknown')} 处理失败: {result.get('error', '未知错误')}\n"
                    
            except Exception as e:
                result_text += f"✗ 处理任务时出错: {str(e)}\n"
        
        result_text += f"\n任务处理完成: {self.processed_count}/{self.total_count} 个任务已处理"
        return result_text
    
    def process_single_task(self, task, index):
        """处理单个任务"""
        try:
            task_code = task.get('task_code')
            scheduled_time = task.get('scheduled_time')
            
            if not task_code or not scheduled_time:
                return {"success": False, "error": "任务信息不完整"}
            
            # 生成巡检时间（使用任务索引作为偏移）
            inspection_time = self.inspection_app.generate_inspection_time(scheduled_time, index * 5)
            
            if not inspection_time:
                return {"success": False, "error": "无法生成巡检时间"}
            
            # 处理任务项文件
            task_items = self.inspection_app.process_task_item_file(task_code)
            
            # 构建处理后的任务数据
            processed_task = {
                "task_id": task.get('task_id'),
                "task_code": task_code,
                "task_name": task.get('task_name', 'Unknown'),
                "scheduled_time": scheduled_time,
                "inspection_time": inspection_time,
                "inspector": self.inspection_app.user_info.get('username'),
                "status": "completed",
                "items_processed": len(task_items) if task_items else 0,
                "result": "巡检完成",
                "data_source": task
            }
            
            return {"success": True, "task": processed_task}
            
        except Exception as e:
            return {"success": False, "error": str(e)}

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, inspection_app):
        self.inspection_app = inspection_app
    
    def generate_inspection_report(self):
        """生成完整的巡检报告"""
        report = []
        report.append("=" * 60)
        report.append("巡检自动化系统报告")
        report.append("=" * 60)
        report.append(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # 操作人员信息
        if self.inspection_app.user_info:
            report.append("【操作人员信息】")
            report.append(f"用户名: {self.inspection_app.user_info.get('username', 'Unknown')}")
            report.append(f"用户代码: {self.inspection_app.user_info.get('usercode', 'Unknown')}")
            report.append(f"用户ID: {self.inspection_app.user_info.get('userid', 'Unknown')}")
            report.append("")
        
        # 数据文件信息
        report.append("【数据文件信息】")
        if self.inspection_app.checker_list:
            report.append(f"检查员总数: {len(self.inspection_app.checker_list)}")
        
        if self.inspection_app.task_data:
            report.append(f"任务总数: {len(self.inspection_app.task_data)}")
        
        report.append("")
        
        # 任务处理结果
        report.append("【任务处理结果】")
        if hasattr(self.inspection_app, 'processed_tasks') and self.inspection_app.processed_tasks:
            completed_tasks = [t for t in self.inspection_app.processed_tasks if t.get('success', False)]
            report.append(f"完成任务数: {len(completed_tasks)}")
            report.append(f"总任务数: {len(self.inspection_app.processed_tasks)}")
            report.append(f"完成率: {len(completed_tasks)/len(self.inspection_app.processed_tasks)*100:.1f}%")
        else:
            report.append("暂无处理完成的任务")
        
        report.append("")
        
        # 详细任务列表
        if hasattr(self.inspection_app, 'processed_tasks') and self.inspection_app.processed_tasks:
            report.append("【详细任务列表】")
            for i, task_result in enumerate(self.inspection_app.processed_tasks, 1):
                if task_result.get('success', False):
                    task = task_result['task']
                    report.append(f"任务 {i}: {task.get('task_code', 'Unknown')}")
                    report.append(f"  任务名称: {task.get('task_name', 'Unknown')}")
                    report.append(f"  计划时间: {task.get('scheduled_time', 'Unknown')}")
                    report.append(f"  巡检时间: {task.get('inspection_time', 'Unknown')}")
                    report.append(f"  处理状态: {task.get('status', 'Unknown')}")
                    report.append(f"  处理项目: {task.get('items_processed', 0)} 项")
                    report.append(f"  处理结果: {task.get('result', 'Unknown')}")
                    report.append("-" * 40)
        
        report.append("")
        report.append("报告生成完成")
        report.append("=" * 60)
        
        return "\n".join(report)

class InspectionApp(App):
    """主应用类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_info = {}
        self.screen_manager = None
    
    def build(self):
        """构建应用界面"""
        self.screen_manager = ScreenManager()
        
        # 添加登录界面
        login_screen = LoginScreen(name='login')
        self.screen_manager.add_widget(login_screen)
        
        # 添加主界面
        main_screen = MainScreen(name='main')
        self.screen_manager.add_widget(main_screen)
        
        return self.screen_manager

if __name__ == '__main__':
    InspectionApp().run()