import json
import random
import os
from datetime import datetime, timedelta
from pathlib import Path

# Kivy 相关 UI 组件
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

# ---------- 核心逻辑类 ----------
class TimeUtil:
    FMT = "%Y-%m-%d %H:%M:%S"
    @staticmethod
    def parse(dt_str: str):
        try:
            return datetime.strptime(dt_str, TimeUtil.FMT)
        except:
            return None
    @staticmethod
    def format(dt: datetime):
        return dt.strftime(TimeUtil.FMT)

class InspectionAutomator:
    def __init__(self, data_dir, username, usercode, log_func):
        self.data_dir = Path(data_dir)
        self.username = username
        self.usercode = usercode
        self.userid = None
        self.log = log_func

    def execute(self):
        try:
            self.log(f"开始执行巡检: {self.username}")
            
            # 1. 加载检查者列表
            checker_path = self.data_dir / "CHECKERLIST.txt"
            if not checker_path.exists():
                return f"错误: 找不到文件 {checker_path}"
            
            with open(checker_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                checkers = json.loads(content)
            
            # 2. 匹配用户 ID
            match = next((c for c in checkers if c.get("username") == self.username and c.get("usercode") == self.usercode), None)
            if not match:
                return f"错误: 未找到匹配用户 {self.username}"
            
            self.userid = match["userid"]
            self.log(f"匹配成功 ID: {self.userid}")

            # 3. 加载任务列表
            task_path = self.data_dir / "TASK.txt"
            if not task_path.exists():
                return "错误: 找不到 TASK.txt"

            with open(task_path, 'r', encoding='utf-8') as f:
                tasks = json.loads(f.read().strip())

            updated_tasks = []
            for tsk in tasks:
                code = tsk.get("taskcode")
                item_file = self.data_dir / f"TASKITEMLIST{code}.txt"
                
                if item_file.exists():
                    with open(item_file, 'r', encoding='utf-8') as f:
                        items = json.loads(f.read().strip())
                    
                    p_start = TimeUtil.parse(tsk.get("planstartdate"))
                    if not p_start: p_start = datetime.now()
                    
                    # [span_0](start_span)模拟时间偏移[span_0](end_span)
                    start_time = p_start + timedelta(minutes=random.randint(5, 15))
                    
                    for it in items:
                        it.update({
                            "checkusrid": self.userid,
                            "checkusrname": self.username,
                            "checktime": TimeUtil.format(start_time),
                            "checkresult": "ZC",
                            "fdesc": "正常"
                        })
                    
                    with open(item_file, 'w', encoding='utf-8') as f:
                        f.write(json.dumps(items, ensure_ascii=False, separators=(",", ":")))
                    
                    new_tsk = tsk.copy()
                    new_tsk.update({
                        "startdate": TimeUtil.format(start_time), 
                        "donedate": TimeUtil.format(start_time + timedelta(minutes=5))
                    })
                    updated_tasks.append(new_tsk)
                    self.log(f"任务 {code} 处理完成")

            with open(task_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(updated_tasks, ensure_ascii=False, separators=(",", ":")))
            
            return "全部巡检任务执行成功！"
        except Exception as e:
            return f"执行出错: {str(e)}"

# ---------- UI 界面部分 ----------
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        layout.add_widget(Label(text="PIMSYS", font_size='24sp'))
        self.username = TextInput(hint_text="用户名", multiline=False, size_hint_y=None, height=100)
        self.usercode = TextInput(hint_text="代码", multiline=False, size_hint_y=None, height=100)
        self.password = TextInput(hint_text="密码", password=True, multiline=False, size_hint_y=None, height=100)
        btn = Button(text="登录", background_color=(0.2, 0.6, 1, 1), size_hint_y=None, height=120)
        btn.bind(on_press=self.do_login)
        layout.add_widget(self.username)
        layout.add_widget(self.usercode)
        layout.add_widget(self.password)
        layout.add_widget(btn)
        self.add_widget(layout)

    def do_login(self, instance):
        if self.password.text == "12138" and self.username.text and self.usercode.text:
            app = App.get_running_app()
            app.user_info = {"name": self.username.text.strip(), "code": self.usercode.text.strip()}
            self.manager.current = 'control'
        else:
            self.password.text = ""
            self.password.hint_text = "验证失败"

class ControlPanel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.log_label = Label(text="等待执行...", size_hint_y=None, height=500, halign="left", valign="top")
        self.log_label.bind(size=self.log_label.setter('text_size'))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.log_label)
        run_btn = Button(text="开始", size_hint_y=None, height=140, background_color=(0.1, 0.8, 0.1, 1))
        run_btn.bind(on_press=self.run_process)
        layout.add_widget(scroll)
        layout.add_widget(run_btn)
        self.add_widget(layout)

    def update_log(self, text):
        self.log_label.text += f"\n> {text}"

    def run_process(self, instance):
        app = App.get_running_app()
        data_dir = "/storage/emulated/0/widgetone/apps/NormalPIM/data"
        automator = InspectionAutomator(data_dir, app.user_info["name"], app.user_info["code"], self.update_log)
        result = automator.execute()
        self.update_log(result)

class InspectionApp(App):
    def build(self):
        self.user_info = {}
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ControlPanel(name='control'))
        return sm

if __name__ == '__main__':
    InspectionApp().run()
          