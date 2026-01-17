# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import threading

# 导入核心逻辑
from core import InspectionAutomator

# 默认密码（这个可以保留为12138，因为它只是第三重验证）
DEFAULT_PASSWORD = "12138"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        layout.add_widget(Label(text="巡检系统登录", font_size=24, size_hint_y=None, height=60))
        
        # 三重输入框
        self.username_input = TextInput(hint_text="请输入人员名", multiline=False)
        self.usercode_input = TextInput(hint_text="请输入人员代码", multiline=False)
        self.password_input = TextInput(hint_text="请输入默认密码", password=True, multiline=False)
        
        login_btn = Button(text="登录", size_hint_y=None, height=60)
        login_btn.bind(on_press=self.check_login)
        
        layout.add_widget(self.username_input)
        layout.add_widget(self.usercode_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_btn)
        self.add_widget(layout)

    def check_login(self, instance):
        username = self.username_input.text.strip()
        usercode = self.usercode_input.text.strip()
        password = self.password_input.text
        
        # 第一重：检查默认密码
        if password != DEFAULT_PASSWORD:
            print("登录失败：默认密码错误")
            return
            
        # 第二、三重：检查用户名和代码是否匹配（通过调用核心逻辑）
        auto = InspectionAutomator("/storage/emulated/0/widgetone/apps/NormalPIM/data", lambda x: None)
        auto.user_info = {"username": username, "usercode": usercode}
        
        if not auto.load_checker_list():
            print("登录失败：无法加载用户列表")
            return
            
        if auto.find_user_id():
            # 登录成功，保存用户信息到App中
            app = InspectionApp.get_running_app()
            app.username = username
            app.usercode = usercode
            app.root.current = 'main'
        else:
            print("登录失败：人员名或人员代码不匹配")

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        layout.add_widget(Label(text="巡检执行面板", font_size=20))
        
        # 显示已登录的用户信息
        app = InspectionApp.get_running_app()
        self.user_label = Label(text=f"当前用户: {app.username} ({app.usercode})", size_hint_y=None, height=40)
        
        self.run_btn = Button(text="执行巡检脚本", size_hint_y=None, height=60)
        self.run_btn.bind(on_press=self.start_execution)
        
        # 日志显示框
        self.log_label = Label(text="点击按钮开始执行...\n", size_hint_y=None, text_size=(400, None))
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.7))
        scroll.add_widget(self.log_label)
        
        layout.add_widget(self.user_label)
        layout.add_widget(self.run_btn)
        layout.add_widget(scroll)
        
        self.add_widget(layout)

    def start_execution(self, instance):
        self.run_btn.disabled = True
        self.log("开始执行巡检任务...\n")
        
        # 在后台线程运行，防止界面卡死
        thread = threading.Thread(target=self.run_script)
        thread.start()

    def run_script(self):
        try:
            app = InspectionApp.get_running_app()
            # 初始化逻辑类
            auto = InspectionAutomator("/storage/emulated/0/widgetone/apps/NormalPIM/data", self.log)
            # 设置用户信息（从登录时获取）
            auto.user_info = {"username": app.username, "usercode": app.usercode}
            # 执行主逻辑
            auto.run()
        except Exception as e:
            self.log(f"脚本运行出错: {e}")
        finally:
            self.run_btn.disabled = False

    def log(self, message):
        print(message) # 控制台输出
        if hasattr(self, 'log_label'):
            self.log_label.text += message + "\n"

class InspectionApp(App):
    def build(self):
        # 初始化用户信息为空
        self.username = ""
        self.usercode = ""
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    InspectionApp().run()