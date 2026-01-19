# app.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder
import threading

# 导入我们的业务逻辑
from main import start_inspection

# 设置窗口背景色（模拟安卓风格）
Window.clearcolor = (0.95, 0.95, 0.95, 1)

class LoginScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class InspectionApp(App):
    def build(self):
        # 加载 KV 文件
        Builder.load_file('main.kv')
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(MainScreen(name='main'))
        return self.sm

    def check_login(self):
        username = self.root.ids.username_input.text
        usercode = self.root.ids.usercode_input.text
        password = self.root.ids.password_input.text

        if password != "12138":
            self.root.ids.password_input.text = ""
            self.show_popup("错误", "默认密码错误！")
            return

        # 这里简单模拟验证，实际逻辑在 main.py 中
        # 我们先检查格式，具体匹配在执行时由 main.py 处理
        if username and usercode:
            # 登录成功，跳转到主界面
            self.root.current = 'main'
            self.root.ids.welcome_label.text = f"欢迎, {username}!"
        else:
            self.show_popup("错误", "请输入用户名和代码")

    def run_script(self):
        # 获取当前用户信息（这里简化处理，实际应从登录状态获取）
        # 由于界面和逻辑分离，这里我们假设登录页的数据还存在，或者需要重构存储
        # 为了演示，我们从全局状态或重新获取
        # 注意：在实际 Kivy 中，最好用属性保存
        username = self.root.ids.username_input.text if hasattr(self.root.ids, 'username_input') else ""
        usercode = self.root.ids.usercode_input.text if hasattr(self.root.ids, 'usercode_input') else ""

        if not username or not usercode:
            # 尝试从主界面或其他地方获取，这里为了演示直接报错
            self.show_popup("错误", "用户信息丢失，请重新登录")
            return

        # 在新线程中运行脚本，防止界面卡死
        threading.Thread(target=self.execute_task, args=(username, usercode), daemon=True).start()

    def execute_task(self, username, usercode):
        # 调用核心逻辑
        result = start_inspection(username, usercode)
        
        # 更新 UI（必须在主线程）
        def update_ui(dt):
            result_label = self.root.ids.result_label
            result_label.text = result
            # 如果成功，可以改变颜色
            if "成功" in result:
                result_label.color = 0, 1, 0, 1 # 绿色
            else:
                result_label.color = 1, 0, 0, 1 # 红色

        from kivy.clock import Clock
        Clock.schedule_once(update_ui)

    def show_popup(self, title, message):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout

        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        btn = Button(text='确定', size_hint_y=None, height='50dp')
        content.add_widget(btn)

        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup.open()

# 这里为了打包，需要定义一个入口
if __name__ == '__main__':
    InspectionApp().run()
