# main.py
import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class TimeUtil:
    FMT = "%Y-%m-%d %H:%M:%S"
    @staticmethod
    def parse(dt_str: str) -> Optional[datetime]:
        try: return datetime.strptime(dt_str, TimeUtil.FMT)
        except ValueError: return None
    @staticmethod
    def format(dt: datetime) -> str: return dt.strftime(TimeUtil.FMT)
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
        except: return None

    @staticmethod
    def save(parent: Path, filename: str, data: List[Dict]) -> bool:
        path = parent / filename
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            json_str = json.dumps(data, ensure_ascii=False, indent=None, separators=(",", ":"))
            path.write_text(json_str, encoding="utf-8")
            return True
        except: return False

class InspectionAutomator:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.checker_list: List[Dict] = []
        self.task_list: List[Dict] = []
        self.user_info: Dict[str, str] = {}

    def load_checker_list(self) -> bool:
        self.checker_list = IOUtil.load(self.data_dir, "CHECKERLIST.txt") or []
        return bool(self.checker_list)

    def load_task_list(self) -> bool:
        self.task_list = IOUtil.load(self.data_dir, "TASK.txt") or []
        return bool(self.task_list)

    def find_user_id(self, username: str, usercode: str) -> bool:
        for chk in self.checker_list:
            if chk.get("username") == username and chk.get("usercode") == usercode:
                self.user_info = {"username": username, "usercode": usercode, "userid": chk["userid"]}
                return True
        return False

    def process_single_task(self, task: Dict) -> Optional[Dict]:
        code = task.get("taskcode")
        plan_start_str = task.get("planstartdate")
        plan_end_str = task.get("planenddate")

        if not all([code, plan_start_str, plan_end_str]):
            return None

        plan_start = TimeUtil.parse(plan_start_str)
        plan_end = TimeUtil.parse(plan_end_str)
        if not plan_start or not plan_end: return None

        items = IOUtil.load(self.data_dir, f"TASKITEMLIST{code}.txt")
        if not items: return None

        duration = plan_end - plan_start
        if duration >= timedelta(hours=4):
            start = plan_start + timedelta(hours=random.randint(1, 3), minutes=random.randint(1, 10)) + TimeUtil.rand_sec()
        else:
            start = plan_start + timedelta(minutes=random.randint(1, 5)) + TimeUtil.rand_sec()

        check_times = [start.replace(second=random.randint(0, 59))]
        cur = check_times[0]
        for _ in range(len(items) - 1):
            cur += timedelta(minutes=random.randint(2, 4)) + TimeUtil.rand_sec()
            check_times.append(cur)

        latest = check_times[-1]
        end = latest + timedelta(minutes=random.randint(1, 2)) + TimeUtil.rand_sec()
        if end > plan_end: end = plan_end - TimeUtil.rand_sec(30)

        for it, chk_time in zip(items, check_times):
            it.update({
                "checkusrid": self.user_info["userid"],
                "checkusrname": self.user_info["username"],
                "checktime": TimeUtil.format(chk_time),
                "checkresult": "ZC",
                "fdesc": "正常",
            })

        if IOUtil.save(self.data_dir, f"TASKITEMLIST{code}.txt", items):
            return task | {"startdate": TimeUtil.format(start), "donedate": TimeUtil.format(end)}
        return None

    def run(self) -> str:
        """执行主逻辑，返回结果字符串"""
        if not self.load_checker_list() or not self.load_task_list():
            return "错误：缺少 CHECKERLIST.txt 或 TASK.txt 文件"

        updated_tasks = []
        for tsk in self.task_list:
            ret = self.process_single_task(tsk)
            if ret: updated_tasks.append(ret)

        if updated_tasks and IOUtil.save(self.data_dir, "TASK.txt", updated_tasks):
            return f"成功！更新了 {len(updated_tasks)} 个任务。"
        else:
            return "执行失败或没有任务可处理。"

# 供 GUI 调用的函数
def start_inspection(username: str, usercode: str) -> str:
    # 注意：Android 上的路径通常为应用私有目录或特定挂载点
    # 这里使用示例路径，你可能需要根据实际手机存储结构调整
    data_dir = "/storage/emulated/0/widgetone/apps/NormalPIM/data"
    auto = InspectionAutomator(data_dir)
    if auto.find_user_id(username, usercode):
        return auto.run()
    else:
        return "用户名或代码不匹配！"
