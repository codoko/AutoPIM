from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window

import sys
from io import StringIO
from threading import Thread

from automator import InspectionAutomator


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        layout.add_widget(Label(text='巡检自动化登录', font_size='24sp', size_hint_y=None, height=60))

        self.username_input = TextInput(hint_text='用户名', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.username_input)

        self.usercode_input = TextInput(hint_text='用户代码', multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.usercode_input)

        self.password_input = TextInput(hint_text='密码', password=True, multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.password_input)

        login_btn = Button(text='登录', size_hint_y=None, height=60)
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)

        self.status_label = Label(text='', color=(1, 0, 0, 1), size_hint_y=None, height=40)
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def login(self, instance):
        username = self.username_input.text.strip()
        usercode = self.usercode_input.text.strip()
        password = self.password_input.text

        if password != '12138':
            self.status_label.text = '密码错误（默认密码：12138）'
            return

        if not username or not usercode:
            self.status_label.text = '用户名和用户代码不能为空'
            return

        app = App.get_running_app()
        app.automator.user_info["username"] = username
        app.automator.user_info["usercode"] = usercode

        if app.automator.find_user_id():
            self.manager.current = 'main'
        else:
            self.status_label.text = '未找到匹配的用户信息'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.scroll = ScrollView()
        self.log_label = Label(
            text='登录成功，准备就绪。\n点击下方按钮开始执行巡检。\n',
            size_hint=(1, None),
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top',
            markup=True
        )
        self.log_label.bind(texture_size=self.log_label.setter('height'))
        self.scroll.add_widget(self.log_label)
        layout.add_widget(self.scroll)

        execute_btn = Button(text='执行巡检自动化', size_hint_y=None, height=80, background_normal='', background_color=(0, 0.6, 0, 1))
        execute_btn.bind(on_press=self.execute)
        layout.add_widget(execute_btn)

        self.add_widget(layout)

    def execute(self, instance):
        app = App.get_running_app()
        self.log_label.text += '\n=== 开始执行巡检 ===\n'

        # 重定向print输出到StringIO
        app.log_buffer = StringIO()
        old_stdout = sys.stdout
        sys.stdout = app.log_buffer

        def run_task():
            try:
                updated_tasks = []
                ok_cnt = 0
                for tsk in app.automator.task_list:
                    ret = app.automator.process_single_task(tsk)
                    if ret:
                        updated_tasks.append(ret)
                        ok_cnt += 1

                if updated_tasks and IOUtil.save(app.automator.data_dir, "TASK.txt", updated_tasks):
                    print(f"\n✓ 成功更新 TASK.txt")

                print(f"\n=== 巡检自动化完成 ===")
                print(f"总任务数: {len(app.automator.task_list)} | 成功处理: {ok_cnt}")
            except Exception as e:
                print(f"\n执行出错: {e}")
            finally:
                sys.stdout = old_stdout

        Thread(target=run_task).start()
        Clock.schedule_interval(app.update_log, 0.5)

class InspectionApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        data_dir = "/storage/emulated/0/widgetone/apps/NormalPIM/data"
        self.automator = InspectionAutomator(data_dir)

        if not self.automator.load_checker_list():
            return Label(text='无法加载 CHECKERLIST.txt\n请检查文件路径和权限', color=(1,0,0,1), font_size='20sp')

        if not self.automator.load_task_list():
            return Label(text='无法加载 TASK.txt\n请检查文件路径和权限', color=(1,0,0,1), font_size='20sp')

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

    def on_start(self):
        self.root.current = 'login'

    log_buffer = None

    def update_log(self, dt):
        if self.log_buffer:
            new_text = self.log_buffer.getvalue()
            if new_text:
                main_screen = self.root.get_screen('main')
                main_screen.log_label.text += new_text
                self.log_buffer.truncate(0)
                self.log_buffer.seek(0)
                main_screen.scroll.scroll_y = 0  # 滚动到底部
            return True
        return False


if __name__ == '__main__':
    InspectionApp().run()