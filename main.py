import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

# ---------- 核心业务逻辑 (适配 UI) ----------
class TimeUtil:
    FMT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def parse(dt_str: str) -> Optional[datetime]:
        try:
            return datetime.strptime(dt_str, TimeUtil.FMT)
        except ValueError:
            return None

    @staticmethod
    def format(dt: datetime) -> str:
        return dt.strftime(TimeUtil.FMT)

    @staticmethod
    def rand_sec(max_sec: int = 59) -> timedelta:
        return timedelta(seconds=random.randint(0, max_sec))

class InspectionAutomator:
    def __init__(self, data_dir: str, logger_func):
        self.data_dir = Path(data_dir)
        self.logger = logger_func
        self.checker_list = []
        self.task_list = []
        self.user_info = {}

    def log(self, message: str):
        # 确保在主线程更新 UI
        Clock.schedule_once(lambda dt: self.logger(message))

    def load_data(self) -> bool:
        self.checker_list = self._load_json("CHECKERLIST.txt") or []
        self.task_list = self._load_json("TASK.txt") or []
        return bool(self.checker_list and self.task_list)

    def _load_json(self, filename: str) -> Optional[List[Dict]]:
        path = self.data_dir / filename
        try:
            with path.open(encoding="utf-8") as f:
                data = json.loads(f.read().strip())
            self.log(f"✓ 已加载 {filename}")
            return data
        except Exception as e:
            self.log(f"✗ 读取 {filename} 失败: {str(e)}")
            return None

    def find_user(self, username: str, usercode: str) -> bool:
        for chk in self.checker_list:
            if chk.get("username") == username and chk.get("usercode") == usercode:
                self.user_info = {"userid": chk["userid"], "username": username, "usercode": usercode}
                return True
        return False

    def process_all(self):
        updated_tasks = []
        ok_cnt = 0
        for tsk in self.task_list:
            res = self.process_single_task(tsk)
            if res:
                updated_tasks.append(res)
                ok_cnt += 1
        
        if updated_tasks:
            self._save_json("TASK.txt", updated_tasks)
            self.log(f"\n=== 完成 ===\n成功处理: {ok_cnt} 个任务")
    def process_single_task(self, task: Dict) -> Optional[Dict]:
        code = task.get("taskcode")
        plan_start = TimeUtil.parse(task.get("planstartdate", ""))
        plan_end = TimeUtil.parse(task.get("planenddate", ""))

        if not (code and plan_start and plan_end): return None

        # 加载任务项
        items = self._load_json(f"TASKITEMLIST{code}.txt")
        if not items: return None

        # 分组与排序
        groups = {}
        for it in items:
            groups.setdefault(it.get("areacode"), []).append(it)
        sorted_areas = sorted(groups.keys(), key=lambda x: int(x) if x.isdigit() else 999)

        # 时间计算逻辑
        duration = plan_end - plan_start
        if duration >= timedelta(hours=4):
            start = plan_start + timedelta(hours=random.randint(1, 3)) + TimeUtil.rand_sec()
        else:
            start = plan_start + timedelta(minutes=random.randint(1, 5)) + TimeUtil.rand_sec()

        # 生成序列
        check_times = [start.replace(second=random.randint(0, 59))]
        for _ in range(len(sorted_areas) - 1):
            check_times.append(check_times[-1] + timedelta(minutes=random.randint(2, 4)) + TimeUtil.rand_sec())
        
        end = check_times[-1] + timedelta(minutes=random.randint(1, 2)) + TimeUtil.rand_sec()
        if end > plan_end: end = plan_end - TimeUtil.rand_sec(30)

        # 赋值
        for area, chk_time in zip(sorted_areas, check_times):
            for it in groups[area]:
                it.update({
                    "checkusrid": self.user_info["userid"],
                    "checkusrname": self.user_info["username"],
                    "checktime": TimeUtil.format(chk_time),
                    "checkresult": "ZC", "fdesc": "正常",
                })

        if self._save_json(f"TASKITEMLIST{code}.txt", items):
            new_task = task.copy()
            new_task.update({"startdate": TimeUtil.format(start), "donedate": TimeUtil.format(end)})
            return new_task
        return None

    def _save_json(self, filename: str, data: List[Dict]) -> bool:
        path = self.data_dir / filename
        try:
            json_str = json.dumps(data, ensure_ascii=False, indent=None, separators=(",", ":"))
            path.write_text(json_str, encoding="utf-8")
            return True
        except Exception as e:
            self.log(f"✗ 保存 {filename} 失败")
            return False

# ---------- UI 界面层 ----------

class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        layout.add(Label(text="自动化巡检系统", font_size='24sp', bold=True))
        
        self.username = TextInput(hint_text="人员姓名 (username)", multiline=False, size_hint_y=None, height='50dp')
        self.usercode = TextInput(hint_text="人员代码 (usercode)", multiline=False, size_hint_y=None, height='50dp')
        self.password = TextInput(hint_text="默认密码 (12138)", password=True, multiline=False, size_hint_y=None, height='50dp')
        
        layout.add(self.username)
        layout.add(self.usercode)
        layout.add(self.password)
        
        btn = Button(text="进入系统", size_hint_y=None, height='60dp', background_color=get_color_from_hex('#2196F3'))
        btn.bind(on_press=self.check_login)
        layout.add(btn)
        
        self.error_label = Label(text="", color=(1, 0, 0, 1))
        layout.add(self.error_label)
        self.add_widget(layout)

    def check_login(self, instance):
        if self.password.text == "12138" and self.username.text and self.usercode.text:
            app = App.get_running_app()
            app.user_data = (self.username.text, self.usercode.text)
            self.manager.current = 'main'
        else:
            self.error_label.text = "信息不全或密码错误"

class MainScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.info_label = Label(text="准备就绪", size_hint_y=None, height='40dp')
        self.layout.add(self.info_label)
        
        # 日志显示区域
        scroll = ScrollView(size_hint=(1, 1))
        self.log_output = Label(text="-- 操作日志 --\n", size_hint_y=None, halign='left', valign='top', markup=True)
        self.log_output.bind(size=self._update_text_size)
        scroll.add_widget(self.log_output)
        self.layout.add(scroll)
        
        self.run_btn = Button(text="开始执行自动化巡检", size_hint_y=None, height='70dp', background_color=get_color_from_hex('#4CAF50'))
        self.run_btn.bind(on_press=self.execute_script)
        self.layout.add(self.run_btn)
        
        self.add_widget(self.layout)

    def _update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)
        instance.height = instance.texture_size[1]

    def write_log(self, text):
        self.log_output.text += text + "\n"

    def execute_script(self, instance):
        self.run_btn.disabled = True
        self.log_output.text = "[b]开始运行...[/b]\n"
        
        # 安卓数据路径
        data_path = "/storage/emulated/0/widgetone/apps/NormalPIM/data"
        
        app = App.get_running_app()
        uname, ucode = app.user_data
        
        automator = InspectionAutomator(data_path, self.write_log)
        
        if not automator.load_data():
            self.write_log("✗ 基础数据加载失败，请检查目录权限")
            self.run_btn.disabled = False
            return
            
        if not automator.find_user(uname, ucode):
            self.write_log(f"✗ 在列表中未找到用户: {uname}")
            self.run_btn.disabled = False
            return
            
        automator.process_all()
        self.run_btn.disabled = False

class InspectionApp(App):
    def build(self):
        self.user_data = ("", "")
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    InspectionApp().run()