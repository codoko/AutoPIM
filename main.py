import json
import random
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
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

# ---------- 核心逻辑类 (从原脚本迁移并适配 UI) ----------
class TimeUtil:
    FMT = "%Y-%m-%d %H:%M:%S"
    @staticmethod
    def parse(dt_str: str):
        try: return datetime.strptime(dt_str, TimeUtil.FMT)
        except: return None
    @staticmethod
    def format(dt: datetime):
        return dt.strftime(TimeUtil.FMT)
    @staticmethod
    def rand_sec(max_sec: int = 59):
        return timedelta(seconds=random.randint(0, max_sec))

class InspectionAutomator:
    def __init__(self, data_dir, username, usercode, log_func):
        self.data_dir = Path(data_dir)
        self.username = username
        self.usercode = usercode
        self.userid = None
        self.log = log_func # 用于向界面发送日志

    def execute(self):
        self.log(f"开始执行巡检: {self.username}")
        
        # 1. [span_2](start_span)加载检查者列表[span_2](end_span)
        checker_path = self.data_dir / "CHECKERLIST.txt"
        if not checker_path.exists():
            return "错误: 找不到 CHECKERLIST.txt"
        
        with open(checker_path, 'r', encoding='utf-8') as f:
            [span_3](start_span)checkers = json.loads(f.read().strip())[span_3](end_span)
        
        # 2. [span_4](start_span)匹配用户 ID[span_4](end_span)
        match = next((c for c in checkers if c.get("username") == self.username and c.get("usercode") == self.usercode), None)
        if not match:
            return f"错误: 未找到匹配用户 {self.username}"
        self.userid = match["userid"]
        self.log(f"匹配成功 ID: {self.userid}")

        # 3. [span_5](start_span)加载任务列表[span_5](end_span)
        task_path = self.data_dir / "TASK.txt"
        with open(task_path, 'r', encoding='utf-8') as f:
            tasks = json.loads(f.read().strip())

        updated_tasks = []
        for tsk in tasks:
            code = tsk.get("taskcode")
            # [span_6](start_span)处理任务项文件[span_6](end_span)
            item_file = self.data_dir / f"TASKITEMLIST{code}.txt"
            if item_file.exists():
                with open(item_file, 'r', encoding='utf-8') as f:
                    items = json.loads(f.read().strip())
                
                # [span_7](start_span)模拟时间偏移[span_7](end_span)
                p_start = TimeUtil.parse(tsk.get("planstartdate"))
                start_time = p_start + timedelta(minutes=random.randint(5, 15))
                
                # [span_8](start_span)更新条目数据[span_8](end_span)
                for it in items:
                    it.update({
                        "checkusrid": self.userid,
                        "checkusrname": self.username,
                        "checktime": TimeUtil.format(start_time),
                        "checkresult": "ZC",
                        "fdesc": "正常"
                    })
                
                # [span_9](start_span)写回任务项[span_9](end_span)
                with open(item_file, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(items, ensure_ascii=False, separators=(",", ":")))
                
                # [span_10](start_span)更新任务主表时间[span_10](end_span)
                new_tsk = tsk.copy()
                new_tsk.update({"startdate": TimeUtil.format(start_time), "donedate": TimeUtil.format(start_time + timedelta(minutes=5))})
                updated_tasks.append(new_tsk)
                self.log(f"任务 {code} 处理完成")

        # [span_11](start_span)保存总任务表[span_11](end_span)
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(updated_tasks, ensure_ascii=False, separators=(",", ":")))
        
        return "全部巡检任务执行成功！"

# ---------- UI 界面部分 ----------

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        layout.add_widget(Label(text="自动巡检系统登录", font_size='24sp', color=(1, 1, 1, 1)))
        
        self.username = TextInput(hint_text="用户名 (Username)", multiline=False, size_hint_y=None, height=100)
        self.usercode = TextInput(hint_text="用户代码 (Usercode)", multiline=False, size_hint_y=None, height=100)
        self.password = TextInput(hint_text="密码 (默认: 12138)", password=True, multiline=False, size_hint_y=None, height=100)
        
        btn = Button(text="登录", background_color=(0.2, 0.6, 1, 1), size_hint_y=None, height=120)
        btn.bind(on_press=self.do_login)
        
        layout.add_widget(self.username)
        layout.add_widget(self.usercode)
        layout.add_widget(self.password)
        layout.add_widget(btn)
        self.add_widget(layout)

    def do_login(self, instance):
        if self.password.text == "12138" and self.username.text and self.usercode.text:
            # [span_12](start_span)登录成功，将信息传递给控制面板并切换[span_12](end_span)
            app = App.get_running_app()
            app.user_info = {"name": self.username.text, "code": self.usercode.text}
            self.manager.current = 'control'
        else:
            self.password.text = ""
            self.password.hint_text = "验证失败，请重新输入"

class ControlPanel(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.log_label = Label(text="等待执行...", size_hint_y=None, height=400, halign="left", valign="top")
        self.log_label.bind(size=self.log_label.setter('text_size'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.log_label)
        
        run_btn = Button(text="开始一键巡检", size_hint_y=None, height=140, background_color=(0.1, 0.8, 0.1, 1))
        run_btn.bind(on_press=self.run_process)
        
        layout.add_widget(Label(text="控制面板", size_hint_y=None, height=50))
        layout.add_widget(scroll)
        layout.add_widget(run_btn)
        self.add_widget(layout)

    def update_log(self, text):
        self.log_label.text += f"\n> {text}"

    def run_process(self, instance):
        app = App.get_running_app()
        # [span_13](start_span)Android 数据存储路径[span_13](end_span)
        data_dir = "/storage/emulated/0/widgetone/apps/NormalPIM/data"
        
        automator = InspectionAutomator(
            data_dir, 
            app.user_info["name"], 
            app.user_info["code"], 
            self.update_log
        )
        
        try:
            result = automator.execute()
            self.update_log(result)
        except Exception as e:
            self.update_log(f"异常: {str(e)}")

class InspectionApp(App):
    def build(self):
        self.user_info = {}
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(ControlPanel(name='control'))
        return sm

if __name__ == '__main__':
    InspectionApp().run()