#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巡检自动化 - Android 版 (Kivy UI)
基于 kimi.py 重构，替换终端交互为 Kivy GUI。
"""

from __future__ import annotations

import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.utils import platform

# ---------- 常量 ----------
DATA_DIR_ANDROID = "/storage/emulated/0/widgetone/apps/NormalPIM/data"
DATA_DIR_DESKTOP = os.path.join(os.path.dirname(__file__), "data")

# ---------- KV 样式 ----------
KV = '''
#:import utils kivy.utils

<RootWidget>:
    orientation: 'vertical'
    padding: dp(16)
    spacing: dp(12)
    canvas.before:
        Color:
            rgba: 0.95, 0.96, 0.98, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # ---- 顶部标题栏 ----
    BoxLayout:
        size_hint_y: None
        height: dp(56)
        canvas.before:
            Color:
                rgba: 0.16, 0.32, 0.47, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(8)]
        Label:
            text: '巡检自动化'
            font_size: sp(22)
            bold: True
            color: 1, 1, 1, 1

    # ---- 状态区 ----
    BoxLayout:
        size_hint_y: None
        height: dp(36)
        Label:
            id: status_label
            text: root.status_text
            font_size: sp(14)
            color: 0.3, 0.3, 0.3, 1
            halign: 'left'
            text_size: self.size

    # ---- 用户信息输入 ----
    BoxLayout:
        size_hint_y: None
        height: dp(50)
        spacing: dp(8)
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(6)]
            Color:
                rgba: 0.8, 0.85, 0.9, 1
            Line:
                rounded_rectangle: [self.x, self.y, self.width, self.height, dp(6)]
                width: 1.2
        TextInput:
            id: username_input
            hint_text: '用户名 (username)'
            multiline: False
            font_size: sp(16)
            padding: [dp(12), dp(12)]
            background_color: 0,0,0,0
            foreground_color: 0.2, 0.2, 0.2, 1
            cursor_color: 0.16, 0.32, 0.47, 1

    BoxLayout:
        size_hint_y: None
        height: dp(50)
        spacing: dp(8)
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(6)]
            Color:
                rgba: 0.8, 0.85, 0.9, 1
            Line:
                rounded_rectangle: [self.x, self.y, self.width, self.height, dp(6)]
                width: 1.2
        TextInput:
            id: usercode_input
            hint_text: '用户代码 (usercode)'
            multiline: False
            font_size: sp(16)
            padding: [dp(12), dp(12)]
            background_color: 0,0,0,0
            foreground_color: 0.2, 0.2, 0.2, 1
            cursor_color: 0.16, 0.32, 0.47, 1

    # ---- 数据目录 ----
    BoxLayout:
        size_hint_y: None
        height: dp(50)
        spacing: dp(8)
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(6)]
            Color:
                rgba: 0.8, 0.85, 0.9, 1
            Line:
                rounded_rectangle: [self.x, self.y, self.width, self.height, dp(6)]
                width: 1.2
        TextInput:
            id: datadir_input
            hint_text: '数据目录路径'
            text: root.data_dir_path
            multiline: False
            font_size: sp(14)
            padding: [dp(12), dp(12)]
            background_color: 0,0,0,0
            foreground_color: 0.2, 0.2, 0.2, 1
            cursor_color: 0.16, 0.32, 0.47, 1

    # ---- 执行按钮 ----
    Button:
        size_hint_y: None
        height: dp(52)
        text: '▶  开始执行巡检'
        font_size: sp(18)
        bold: True
        background_color: 0,0,0,0
        background_normal: ''
        color: 1, 1, 1, 1
        disabled: root.running
        canvas.before:
            Color:
                rgba: (0.16, 0.32, 0.47, 1) if not self.disabled else (0.5, 0.5, 0.5, 1)
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(8)]
        on_release: root.start_automation()

    # ---- 日志输出 ----
    ScrollView:
        id: scroll_view
        bar_width: dp(4)
        bar_color: 0.16, 0.32, 0.47, 0.5
        canvas.before:
            Color:
                rgba: 0.12, 0.14, 0.18, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(6)]
        Label:
            id: log_label
            text: root.log_text
            font_size: sp(13)
            font_name: 'Roboto'
            color: 0.7, 0.85, 0.6, 1
            text_size: self.width - dp(16), None
            size_hint_y: None
            height: max(self.texture_size[1] + dp(16), scroll_view.height)
            halign: 'left'
            valign: 'top'
            padding: [dp(8), dp(8)]
'''


# ---------- 工具类 ----------
class TimeUtil:
    FMT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def parse(dt_str: str) -> Optional[datetime]:
        try:
            return datetime.strptime(dt_str, TimeUtil.FMT)
        except ValueError:
            return None

    @staticmethod
    def fmt(dt: datetime) -> str:
        return dt.strftime(TimeUtil.FMT)

    @staticmethod
    def rand_sec(max_sec: int = 59) -> timedelta:
        return timedelta(seconds=random.randint(0, max_sec))


class IOUtil:
    @staticmethod
    def load(parent: Path, filename: str) -> Optional[List[Dict]]:
        path = parent / filename
        try:
            with path.open(encoding="utf-8") as f:
                data = json.loads(f.read().strip())
            return data
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return None

    @staticmethod
    def save(parent: Path, filename: str, data: List[Dict]) -> bool:
        path = parent / filename
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            json_str = json.dumps(data, ensure_ascii=False, indent=None, separators=(",", ":"))
            path.write_text(json_str, encoding="utf-8")
            return True
        except (OSError, TypeError):
            return False


# ---------- 业务逻辑 ----------
class InspectionAutomator:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.checker_list: List[Dict] = []
        self.task_list: List[Dict] = []
        self.user_info: Dict[str, str] = {}
        self.log_callback = None  # type: Optional[callable]

    def log(self, msg: str):
        if self.log_callback:
            self.log_callback(msg)

    def load_checker_list(self) -> bool:
        self.checker_list = IOUtil.load(self.data_dir, "CHECKERLIST.txt") or []
        self.log(f"✓ 加载 CHECKERLIST.txt: {len(self.checker_list)} 条")
        return bool(self.checker_list)

    def load_task_list(self) -> bool:
        self.task_list = IOUtil.load(self.data_dir, "TASK.txt") or []
        self.log(f"✓ 加载 TASK.txt: {len(self.task_list)} 条")
        return bool(self.task_list)

    def find_user_id(self) -> bool:
        for chk in self.checker_list:
            if chk.get("username") == self.user_info["username"] and chk.get("usercode") == self.user_info["usercode"]:
                self.user_info["userid"] = chk["userid"]
                self.log(f"✓ 匹配用户ID: {self.user_info['userid']}")
                return True
        self.log(f"✗ 未找到匹配用户: {self.user_info['username']}")
        return False

    def load_task_items(self, task_code: str):
        items = IOUtil.load(self.data_dir, f"TASKITEMLIST{task_code}.txt")
        if not items:
            self.log(f"  ✗ 无法加载 TASKITEMLIST{task_code}.txt")
            return None, None, None
        groups: Dict[str, List[Dict]] = {}
        for it in items:
            groups.setdefault(it.get("areacode"), []).append(it)
        sorted_areas = sorted(groups.keys(), key=lambda x: int(x) if x.isdigit() else 999)
        return items, sorted_areas, groups

    def generate_time_sequence(self, start: datetime, area_count: int) -> List[datetime]:
        times = [start.replace(second=random.randint(0, 59))]
        cur = times[0]
        for _ in range(area_count - 1):
            cur += timedelta(minutes=random.randint(2, 4)) + TimeUtil.rand_sec()
            times.append(cur)
        return times

    def process_single_task(self, task: Dict) -> Optional[Dict]:
        code = task.get("taskcode")
        name = task.get("taskname", "未知任务")
        plan_start_str = task.get("planstartdate")
        plan_end_str = task.get("planenddate")
        self.log(f"\n▸ 任务: {name} ({code})")

        if not all([code, plan_start_str, plan_end_str]):
            self.log("  ✗ 关键字段缺失，跳过")
            return None

        plan_start = TimeUtil.parse(plan_start_str)
        plan_end = TimeUtil.parse(plan_end_str)
        if not plan_start or not plan_end:
            self.log("  ✗ 时间格式错误，跳过")
            return None

        items, sorted_areas, groups = self.load_task_items(code)
        if not items or not sorted_areas:
            self.log("  ✗ 无有效数据，跳过")
            return None

        duration = plan_end - plan_start
        if duration >= timedelta(hours=4):
            start = plan_start + timedelta(hours=random.randint(1, 3), minutes=random.randint(1, 10)) + TimeUtil.rand_sec()
        else:
            start = plan_start + timedelta(minutes=random.randint(1, 5)) + TimeUtil.rand_sec()

        check_times = self.generate_time_sequence(start, len(sorted_areas))
        latest = check_times[-1]
        end = latest + timedelta(minutes=random.randint(1, 2)) + TimeUtil.rand_sec()
        if end > plan_end:
            end = plan_end - TimeUtil.rand_sec(30)

        for area, chk_time in zip(sorted_areas, check_times):
            for it in groups[area]:
                it.update({
                    "checkusrid": self.user_info["userid"],
                    "checkusrname": self.user_info["username"],
                    "checktime": TimeUtil.fmt(chk_time),
                    "checkresult": "ZC",
                    "fdesc": "正常",
                })

        if IOUtil.save(self.data_dir, f"TASKITEMLIST{code}.txt", items):
            new_task = task.copy()
            new_task.update({"startdate": TimeUtil.fmt(start), "donedate": TimeUtil.fmt(end)})
            self.log(f"  ✓ 完成 ({len(sorted_areas)} 个区域)")
            return new_task
        self.log(f"  ✗ 保存失败")
        return None

    def run(self, username: str, usercode: str) -> str:
        """主流程，返回结果摘要"""
        self.log("=== 开始执行巡检自动化 ===")

        if not self.load_checker_list():
            return "错误: CHECKERLIST.txt 加载失败"
        if not self.load_task_list():
            return "错误: TASK.txt 加载失败"

        self.user_info["username"] = username
        self.user_info["usercode"] = usercode

        if not self.find_user_id():
            return "错误: 用户信息不匹配"

        updated_tasks: List[Dict] = []
        ok_cnt = 0
        for tsk in self.task_list:
            ret = self.process_single_task(tsk)
            if ret:
                updated_tasks.append(ret)
                ok_cnt += 1

        if updated_tasks and IOUtil.save(self.data_dir, "TASK.txt", updated_tasks):
            self.log("✓ TASK.txt 已更新")

        summary = f"完成! 总任务: {len(self.task_list)} | 成功: {ok_cnt}"
        self.log(f"=== {summary} ===")
        return summary


# ---------- Kivy UI ----------
class RootWidget(BoxLayout):
    status_text = StringProperty("就绪，请输入信息后点击执行")
    log_text = StringProperty("")
    running = BooleanProperty(False)
    data_dir_path = StringProperty(DATA_DIR_ANDROID if platform == 'android' else DATA_DIR_DESKTOP)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._automator = None

    def _append_log(self, msg: str):
        self.log_text += msg + "\n"
        # 自动滚动到底部
        Clock.schedule_once(lambda dt: setattr(self.ids.scroll_view, 'scroll_y', 0), 0.05)

    def start_automation(self):
        username = self.ids.username_input.text.strip()
        usercode = self.ids.usercode_input.text.strip()
        data_dir = self.ids.datadir_input.text.strip()

        if not username or not usercode:
            self._show_popup("提示", "请输入用户名和用户代码")
            return
        if not data_dir:
            self._show_popup("提示", "请输入数据目录路径")
            return
        if not Path(data_dir).exists():
            self._show_popup("错误", f"数据目录不存在:\n{data_dir}")
            return

        self.running = True
        self.status_text = "正在执行..."
        self.log_text = ""

        self._automator = InspectionAutomator(data_dir)
        self._automator.log_callback = self._append_log

        # 在下一个事件循环执行，避免阻塞 UI
        Clock.schedule_once(lambda dt: self._do_run(username, usercode), 0.1)

    def _do_run(self, username: str, usercode: str):
        try:
            result = self._automator.run(username, usercode)
            self.status_text = result
        except Exception as e:
            self._append_log(f"✗ 异常: {e}")
            self.status_text = f"执行出错: {e}"
        finally:
            self.running = False

    def _show_popup(self, title: str, msg: str):
        popup = Popup(
            title=title,
            content=Label(text=msg, font_size=sp(16), halign='center', text_size=(dp(250), None)),
            size_hint=(0.8, 0.3),
            auto_dismiss=True,
        )
        popup.open()


class InspectionApp(App):
    def build(self):
        self.title = "巡检自动化"
        Builder.load_string(KV)
        return RootWidget()


if __name__ == "__main__":
    InspectionApp().run()
