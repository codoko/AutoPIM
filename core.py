# core.py
from __future__ import annotations
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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

class IOUtil:
    @staticmethod
    def load(parent: Path, filename: str, log_callback) -> Optional[List[Dict]]:
        path = parent / filename
        try:
            with path.open(encoding="utf-8") as f:
                data = json.loads(f.read().strip())
            log_callback(f"✓ 成功加载 {filename}，共 {len(data)} 条记录")
            return data
        except FileNotFoundError:
            log_callback(f"✗ 文件不存在: {filename}")
        except json.JSONDecodeError as e:
            log_callback(f"✗ {filename} JSON 解析失败: {e}")
        except OSError as e:
            log_callback(f"✗ 读取 {filename} 失败: {e}")
        return None

    @staticmethod
    def save(parent: Path, filename: str, data: List[Dict], log_callback) -> bool:
        path = parent / filename
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            json_str = json.dumps(data, ensure_ascii=False, indent=None, separators=(",", ":"))
            path.write_text(json_str, encoding="utf-8")
            log_callback(f"✓ 成功保存 {filename}")
            return True
        except (OSError, TypeError) as e:
            log_callback(f"✗ 保存 {filename} 失败: {e}")
            return False

class InspectionAutomator:
    def __init__(self, data_dir: str | Path, log_callback):
        self.data_dir = Path(data_dir)
        self.checker_list: List[Dict] = []
        self.task_list: List[Dict] = []
        self.user_info: Dict[str, str] = {}
        self.log_callback = log_callback

    def load_checker_list(self) -> bool:
        data = IOUtil.load(self.data_dir, "CHECKERLIST.txt", self.log_callback) or []
        self.checker_list = data
        return bool(self.checker_list)

    def load_task_list(self) -> bool:
        data = IOUtil.load(self.data_dir, "TASK.txt", self.log_callback) or []
        self.task_list = data
        return bool(self.task_list)

    def find_user_id(self) -> bool:
        for chk in self.checker_list:
            if chk.get("username") == self.user_info["username"] and chk.get("usercode") == self.user_info["usercode"]:
                self.user_info["userid"] = chk["userid"]
                self.log_callback(f"✓ 找到匹配的用户ID: {self.user_info['userid']}")
                return True
        self.log_callback(f"✗ 未找到匹配用户: {self.user_info['username']}")
        return False

    def load_task_items(self, task_code: str) -> Tuple[Optional[List[Dict]], Optional[List[str]], Optional[Dict[str, List[Dict]]]]:
        items = IOUtil.load(self.data_dir, f"TASKITEMLIST{task_code}.txt", self.log_callback)
        if not items:
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
        self.log_callback(f"\n处理任务: {name} ({code})")

        if not all([code, plan_start_str, plan_end_str]):
            self.log_callback("✗ 任务关键字段缺失，跳过")
            return None

        plan_start = TimeUtil.parse(plan_start_str)
        plan_end = TimeUtil.parse(plan_end_str)
        if not plan_start or not plan_end:
            self.log_callback("✗ 时间格式错误，跳过")
            return None

        items, sorted_areas, groups = self.load_task_items(code)
        if not items:
            return None
        if not sorted_areas:
            self.log_callback("✗ 无有效区域数据，跳过")
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
                    "checktime": TimeUtil.format(chk_time),
                    "checkresult": "ZC",
                    "fdesc": "正常",
                })

        if IOUtil.save(self.data_dir, f"TASKITEMLIST{code}.txt", items, self.log_callback):
            new_task = task.copy()
            new_task.update({"startdate": TimeUtil.format(start), "donedate": TimeUtil.format(end)})
            return new_task
        return None

    def run(self) -> None:
        self.log_callback("\n=== 开始执行巡检自动化 ===")
        if not self.load_checker_list() or not self.load_task_list():
            return

        self.log_callback(f"✓ 用户信息已接收: {self.user_info['username']} ({self.user_info['usercode']})")
        
        if not self.find_user_id():
            return

        updated_tasks: List[Dict] = []
        ok_cnt = 0
        for tsk in self.task_list:
            ret = self.process_single_task(tsk)
            if ret:
                updated_tasks.append(ret)
                ok_cnt += 1

        if updated_tasks and IOUtil.save(self.data_dir, "TASK.txt", updated_tasks, self.log_callback):
            self.log_callback(f"\n✓ 成功更新 TASK.txt")

        self.log_callback(f"\n=== 巡检自动化完成 ===")
        self.log_callback(f"总任务数: {len(self.task_list)} | 成功处理: {ok_cnt}")