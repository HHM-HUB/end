import pyautogui
import time
import random
import threading
import json
import os
from datetime import datetime
from pynput import mouse, keyboard
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys

class ClickRecorder:
    """点击录制器"""
    def __init__(self):
        self.is_recording = False
        self.recorded_clicks = []
        self.start_time = None

    def start_recording(self):
        """开始录制"""
        self.is_recording = True
        self.recorded_clicks = []
        self.start_time = time.time()

    def stop_recording(self):
        """停止录制"""
        self.is_recording = False
        return self.recorded_clicks

    def record_click(self, x, y, button='left'):
        """记录点击"""
        if self.is_recording:
            timestamp = time.time() - self.start_time
            self.recorded_clicks.append({
                'x': x,
                'y': y,
                'button': str(button),
                'timestamp': round(timestamp, 3)
            })

    def get_recorded_data(self):
        """获取录制数据"""
        return {
            'clicks': self.recorded_clicks,
            'total_clicks': len(self.recorded_clicks),
            'duration': round(time.time() - self.start_time, 2) if self.start_time else 0
        }


class TaskManager:
    """任务管理器 - 后台管理系统"""
    def __init__(self, data_file='click_tasks.json'):
        self.data_file = data_file
        self.tasks = {}
        self.logs = []
        self.running_processes = {}
        self.load_tasks()

    def load_tasks(self):
        """加载任务数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = {}

    def save_tasks(self):
        """保存任务数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def create_task(self, name, recorded_data, repeat_count=1, interval=0.5):
        """创建任务"""
        task_id = f"task_{len(self.tasks) + 1}_{int(time.time())}"
        task = {
            'id': task_id,
            'name': name,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'recorded_data': recorded_data,
            'repeat_count': repeat_count,
            'interval': interval,
            'status': 'stopped',
            'last_run': None,
            'total_runs': 0
        }
        self.tasks[task_id] = task
        self.save_tasks()
        self.add_log(f"创建任务: {name} (ID: {task_id})")
        return task_id

    def update_task(self, task_id, **kwargs):
        """更新任务"""
        if task_id in self.tasks:
            self.tasks[task_id].update(kwargs)
            self.save_tasks()
            self.add_log(f"更新任务: {task_id}")
            return True
        return False

    def delete_task(self, task_id):
        """删除任务"""
        if task_id in self.tasks:
            task_name = self.tasks[task_id]['name']
            del self.tasks[task_id]
            self.save_tasks()
            self.add_log(f"删除任务: {task_name} (ID: {task_id})")
            return True
        return False

    def get_task(self, task_id):
        """获取任务"""
        return self.tasks.get(task_id)

    def get_all_tasks(self):
        """获取所有任务"""
        return self.tasks

    def add_log(self, message, level='INFO'):
        """添加日志"""
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'level': level,
            'message': message
        }
        self.logs.append(log_entry)
        # 保留最近1000条日志
        if len(self.logs) > 1000:
            self.logs = self.logs[-1000:]

    def get_logs(self, limit=100):
        """获取日志"""
        return self.logs[-limit:]

    def clear_logs(self):
        """清空日志"""
        self.logs = []

    def register_process(self, task_id, thread):
        """注册进程"""
        self.running_processes[task_id] = {
            'thread': thread,
            'started_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'running'
        }
        self.update_task(task_id, status='running')
        self.add_log(f"启动任务进程: {task_id}", 'SUCCESS')

    def unregister_process(self, task_id):
        """注销进程"""
        if task_id in self.running_processes:
            del self.running_processes[task_id]
            self.update_task(task_id, status='stopped')
            self.add_log(f"停止任务进程: {task_id}", 'WARNING')

    def get_running_processes(self):
        """获取运行中的进程"""
        return self.running_processes


class AutoClicker:
    def __init__(self, task_manager=None):
        self.is_clicking = False
        self.is_running = False
        self.click_count = 0
        self.interval = 0.5
        self.position = None
        self.thread = None
        self.task_manager = task_manager or TaskManager()
        self.current_task_id = None

    def click_worker(self, task_id, clicks, repeat_count, interval):
        """点击工作线程"""
        try:
            for run in range(repeat_count):
                if not self.is_running:
                    break

                self.task_manager.add_log(f"任务 {task_id} - 第 {run + 1}/{repeat_count} 次执行")

                for click in clicks:
                    if not self.is_running:
                        break

                    try:
                        x, y = click['x'], click['y']
                        button = click.get('button', 'Button.left')

                        # 解析按钮类型
                        if 'right' in button.lower():
                            pyautogui.rightClick(x, y)
                        elif 'middle' in button.lower():
                            pyautogui.middleClick(x, y)
                        else:
                            pyautogui.click(x, y)

                        self.click_count += 1
                        time.sleep(interval)
                    except Exception as e:
                        self.task_manager.add_log(f"点击错误: {str(e)}", 'ERROR')

                if run < repeat_count - 1 and self.is_running:
                    time.sleep(1)

            self.task_manager.update_task(
                task_id,
                status='completed',
                last_run=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                total_runs=self.task_manager.get_task(task_id)['total_runs'] + 1
            )
            self.task_manager.add_log(f"任务 {task_id} 完成", 'SUCCESS')

        except Exception as e:
            self.task_manager.add_log(f"任务 {task_id} 异常: {str(e)}", 'ERROR')
        finally:
            self.is_running = False
            self.is_clicking = False
            self.task_manager.unregister_process(task_id)

    def start_task(self, task_id):
        """启动任务"""
        task = self.task_manager.get_task(task_id)
        if not task:
            return False

        clicks = task['recorded_data']['clicks']
        repeat_count = task['repeat_count']
        interval = task['interval']

        if not clicks:
            self.task_manager.add_log(f"任务 {task_id} 没有录制的点击数据", 'ERROR')
            return False

        self.is_running = True
        self.is_clicking = True
        self.current_task_id = task_id

        thread = threading.Thread(
            target=self.click_worker,
            args=(task_id, clicks, repeat_count, interval),
            daemon=True
        )
        thread.start()

        self.task_manager.register_process(task_id, thread)
        return True

    def stop_task(self, task_id=None):
        """停止任务"""
        target_id = task_id or self.current_task_id
        if target_id:
            self.is_running = False
            self.is_clicking = False
            self.task_manager.unregister_process(target_id)

    def toggle_clicking(self):
        """切换点击状态"""
        if self.is_clicking:
            self.stop_clicking()
        else:
            self.start_clicking()
        return self.is_clicking

    def set_interval(self, interval):
        """设置点击间隔"""
        self.interval = interval

    def set_position(self, position):
        """设置点击位置"""
        self.position = position

    def get_mouse_position(self):
        """获取当前鼠标位置"""
        return pyautogui.position()

    def reset_count(self):
        """重置计数"""
        self.click_count = 0


class AutoClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("雾眠的小面板~")
        self.root.geometry("900x700")

        self.clicker = AutoClicker()
        self.recorder = ClickRecorder()
        self.task_manager = self.clicker.task_manager

        # 录制相关变量
        self.mouse_listener = None
        self.is_recording_mode = False

        self.setup_ui()

        # 绑定快捷键
        self.root.bind('<F1>', lambda e: self.toggle_recording())
        self.root.bind('<F2>', lambda e: self.get_position())
        self.root.bind('<F3>', lambda e: self.show_task_manager())
        self.root.bind('<Escape>', lambda e: self.exit_app())

        # 启动日志更新定时器
        self.update_logs()

    def setup_ui(self):
        """设置界面"""
        # 创建选项卡
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 主控制选项卡
        main_frame = tk.Frame(notebook)
        notebook.add(main_frame, text="🎯 主控制台")
        self.setup_main_tab(main_frame)

        # 任务管理选项卡
        task_frame = tk.Frame(notebook)
        notebook.add(task_frame, text="📋 任务管理")
        self.setup_task_tab(task_frame)

        # 日志查看选项卡
        log_frame = tk.Frame(notebook)
        notebook.add(log_frame, text="📝 运行日志")
        self.setup_log_tab(log_frame)

    def setup_main_tab(self, parent):
        """设置主控制台"""
        # 标题
        title_frame = tk.Frame(parent, bg="#667eea", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="🖱️ 雾眠的点击器",
            font=("Arial", 20, "bold"),
            bg="#667eea",
            fg="white"
        )
        title_label.pack(pady=15)

        content_frame = tk.Frame(parent, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 录制控制区
        record_frame = tk.LabelFrame(content_frame, text="录制控制", font=("Arial", 11, "bold"))
        record_frame.pack(fill=tk.X, pady=(0, 15))

        btn_frame = tk.Frame(record_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        self.record_btn = tk.Button(
            btn_frame,
            text="⏺️ 开始录制 (F1)",
            command=self.toggle_recording,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            cursor="hand2"
        )
        self.record_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        save_btn = tk.Button(
            btn_frame,
            text="💾 保存录制",
            command=self.save_recording,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            cursor="hand2"
        )
        save_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.record_status = tk.Label(
            record_frame,
            text="状态: 未录制",
            font=("Arial", 9),
            fg="#666"
        )
        self.record_status.pack(pady=(0, 5))

        # 点击间隔设置
        interval_frame = tk.LabelFrame(content_frame, text="点击间隔 (秒)", font=("Arial", 11))
        interval_frame.pack(fill=tk.X, pady=(0, 15))

        self.interval_var = tk.DoubleVar(value=0.5)
        interval_scale = tk.Scale(
            interval_frame,
            from_=0.1,
            to=5.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.interval_var,
            command=self.on_interval_change
        )
        interval_scale.pack(fill=tk.X, padx=10, pady=10)

        self.interval_label = tk.Label(interval_frame, text="0.5 秒", font=("Arial", 9))
        self.interval_label.pack(pady=(0, 5))

        # 点击位置设置
        position_frame = tk.LabelFrame(content_frame, text="点击位置", font=("Arial", 11))
        position_frame.pack(fill=tk.X, pady=(0, 15))

        self.position_var = tk.StringVar(value="当前位置")
        position_btn = tk.Button(
            position_frame,
            text="📍 获取鼠标位置 (F2)",
            command=self.get_position,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            cursor="hand2"
        )
        position_btn.pack(fill=tk.X, padx=10, pady=10)

        self.position_label = tk.Label(position_frame, textvariable=self.position_var, font=("Arial", 9))
        self.position_label.pack(pady=(0, 5))

        # 控制按钮
        control_frame = tk.Frame(content_frame)
        control_frame.pack(fill=tk.X, pady=(0, 15))

        self.toggle_btn = tk.Button(
            control_frame,
            text="▶️ 开始点击",
            command=self.toggle_click,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            cursor="hand2"
        )
        self.toggle_btn.pack(fill=tk.X, pady=5)

        reset_btn = tk.Button(
            control_frame,
            text="🔄 重置计数",
            command=self.reset_count,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            cursor="hand2"
        )
        reset_btn.pack(fill=tk.X, pady=5)

        # 统计信息
        stats_frame = tk.LabelFrame(content_frame, text="统计信息", font=("Arial", 11))
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        self.count_label = tk.Label(
            stats_frame,
            text="点击次数: 0",
            font=("Arial", 14, "bold"),
            fg="#667eea"
        )
        self.count_label.pack(pady=10)

        # 说明信息
        info_frame = tk.Frame(content_frame, bg="#f0f0f0", relief=tk.RAISED, borderwidth=1)
        info_frame.pack(fill=tk.X)

        info_text = """快捷键说明:
• F1 - 开始/停止录制
• F2 - 获取鼠标位置
• F3 - 打开任务管理
• ESC - 退出程序"""
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg="#f0f0f0",
            justify=tk.LEFT,
            anchor="w"
        )
        info_label.pack(padx=10, pady=10)

    def setup_task_tab(self, parent):
        """设置任务管理选项卡"""
        # 工具栏
        toolbar = tk.Frame(parent, bg="#f0f0f0")
        toolbar.pack(fill=tk.X, padx=10, pady=10)

        refresh_btn = tk.Button(
            toolbar,
            text="🔄 刷新",
            command=self.refresh_task_list,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9),
            cursor="hand2"
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(
            toolbar,
            text="🗑️ 删除选中",
            command=self.delete_selected_task,
            bg="#f44336",
            fg="white",
            font=("Arial", 9),
            cursor="hand2"
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        # 任务列表
        list_frame = tk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 创建Treeview
        columns = ('名称', '创建时间', '重复次数', '状态', '运行次数')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 双击编辑
        self.task_tree.bind('<Double-1>', self.edit_task)

        # 操作按钮
        action_frame = tk.Frame(parent)
        action_frame.pack(fill=tk.X, padx=10, pady=10)

        run_btn = tk.Button(
            action_frame,
            text="▶️ 运行选中任务",
            command=self.run_selected_task,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2"
        )
        run_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        stop_btn = tk.Button(
            action_frame,
            text="⏹️ 停止任务",
            command=self.stop_selected_task,
            bg="#f44336",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2"
        )
        stop_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        # 进程监控
        process_frame = tk.LabelFrame(parent, text="运行中的进程", font=("Arial", 10))
        process_frame.pack(fill=tk.X, padx=10, pady=10)

        self.process_text = scrolledtext.ScrolledText(
            process_frame,
            height=6,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        self.process_text.pack(fill=tk.X, padx=5, pady=5)

        # 初始化任务列表
        self.refresh_task_list()
        self.update_process_list()

    def setup_log_tab(self, parent):
        """设置日志选项卡"""
        # 工具栏
        toolbar = tk.Frame(parent)
        toolbar.pack(fill=tk.X, padx=10, pady=10)

        clear_btn = tk.Button(
            toolbar,
            text="🗑️ 清空日志",
            command=self.clear_logs,
            bg="#f44336",
            fg="white",
            font=("Arial", 9),
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        export_btn = tk.Button(
            toolbar,
            text="📤 导出日志",
            command=self.export_logs,
            bg="#2196F3",
            fg="white",
            font=("Arial", 9),
            cursor="hand2"
        )
        export_btn.pack(side=tk.LEFT, padx=5)

        # 日志显示区
        log_frame = tk.Frame(parent)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 配置标签颜色
        self.log_text.tag_config('INFO', foreground='#4CAF50')
        self.log_text.tag_config('WARNING', foreground='#FF9800')
        self.log_text.tag_config('ERROR', foreground='#f44336')
        self.log_text.tag_config('SUCCESS', foreground='#00bcd4')

    def on_mouse_click(self, x, y, button, pressed):
        """鼠标点击监听器"""
        if pressed and self.is_recording_mode:
            self.recorder.record_click(x, y, button)
            self.record_status.config(text=f"状态: 录制中... (已录制: {len(self.recorder.recorded_clicks)} 次点击)")

    def toggle_recording(self):
        """切换录制状态"""
        if not self.is_recording_mode:
            # 开始录制
            self.recorder.start_recording()
            self.is_recording_mode = True

            # 启动鼠标监听
            self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
            self.mouse_listener.start()

            self.record_btn.config(text="⏹️ 停止录制 (F1)", bg="#f44336")
            self.record_status.config(text="状态: 🔴 录制中...", fg="red")

            messagebox.showinfo("录制开始", "现在开始录制鼠标点击!\n点击任意位置进行录制。\n按F1或点击按钮停止录制。")
        else:
            # 停止录制
            self.is_recording_mode = False
            if self.mouse_listener:
                self.mouse_listener.stop()

            data = self.recorder.get_recorded_data()
            self.record_btn.config(text="⏺️ 开始录制 (F1)", bg="#4CAF50")
            self.record_status.config(
                text=f"状态: 已录制 {data['total_clicks']} 次点击, 时长: {data['duration']}秒",
                fg="green"
            )

    def save_recording(self):
        """保存录制"""
        if not self.recorder.recorded_clicks:
            messagebox.showwarning("警告", "没有录制的数据!")
            return

        # 弹出对话框输入任务信息
        dialog = tk.Toplevel(self.root)
        dialog.title("保存任务")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="任务名称:", font=("Arial", 10)).pack(pady=10)
        name_entry = tk.Entry(dialog, font=("Arial", 11), width=30)
        name_entry.pack(pady=5)
        name_entry.focus()

        tk.Label(dialog, text="重复次数:", font=("Arial", 10)).pack(pady=10)
        repeat_var = tk.IntVar(value=1)
        repeat_spin = tk.Spinbox(dialog, from_=1, to=9999, textvariable=repeat_var, font=("Arial", 11))
        repeat_spin.pack(pady=5)

        tk.Label(dialog, text="点击间隔(秒):", font=("Arial", 10)).pack(pady=10)
        interval_var = tk.DoubleVar(value=0.5)
        interval_spin = tk.Spinbox(dialog, from_=0.1, to=10.0, increment=0.1,
                                   textvariable=interval_var, font=("Arial", 11))
        interval_spin.pack(pady=5)

        def save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("警告", "请输入任务名称!")
                return

            recorded_data = self.recorder.get_recorded_data()
            task_id = self.task_manager.create_task(
                name=name,
                recorded_data=recorded_data,
                repeat_count=repeat_var.get(),
                interval=interval_var.get()
            )

            messagebox.showinfo("成功", f"任务已保存!\n任务ID: {task_id}")
            dialog.destroy()
            self.refresh_task_list()

        tk.Button(dialog, text="保存", command=save, bg="#4CAF50",
                 fg="white", font=("Arial", 11, "bold")).pack(pady=20)

    def get_position(self):
        """获取鼠标位置"""
        def delayed_get():
            time.sleep(2)
            pos = self.clicker.get_mouse_position()
            self.clicker.set_position(pos)
            self.position_var.set(f"X: {pos.x}, Y: {pos.y}")

        thread = threading.Thread(target=delayed_get, daemon=True)
        thread.start()

        self.position_var.set("请在2秒内移动鼠标到目标位置...")

    def toggle_click(self):
        """切换点击状态"""
        is_clicking = self.clicker.toggle_clicking()

        if is_clicking:
            self.toggle_btn.config(text="⏹️ 停止点击", bg="#f44336")
        else:
            self.toggle_btn.config(text="▶️ 开始点击", bg="#2196F3")

    def reset_count(self):
        """重置计数"""
        self.clicker.reset_count()
        self.count_label.config(text="点击次数: 0")

    def on_interval_change(self, value):
        """间隔改变回调"""
        interval = float(value)
        self.clicker.set_interval(interval)
        self.interval_label.config(text=f"{interval:.1f} 秒")

    def refresh_task_list(self):
        """刷新任务列表"""
        # 清空列表
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        # 添加任务
        tasks = self.task_manager.get_all_tasks()
        for task_id, task in tasks.items():
            self.task_tree.insert('', tk.END, iid=task_id, values=(
                task['name'],
                task['created_at'],
                task['repeat_count'],
                task['status'],
                task['total_runs']
            ))

    def edit_task(self, event):
        """编辑任务"""
        selected = self.task_tree.selection()
        if not selected:
            return

        task_id = selected[0]
        task = self.task_manager.get_task(task_id)
        if not task:
            return

        # 编辑对话框
        dialog = tk.Toplevel(self.root)
        dialog.title(f"编辑任务: {task['name']}")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="任务名称:", font=("Arial", 10)).pack(pady=10)
        name_entry = tk.Entry(dialog, font=("Arial", 11), width=30)
        name_entry.insert(0, task['name'])
        name_entry.pack(pady=5)

        tk.Label(dialog, text="重复次数:", font=("Arial", 10)).pack(pady=10)
        repeat_var = tk.IntVar(value=task['repeat_count'])
        repeat_spin = tk.Spinbox(dialog, from_=1, to=9999, textvariable=repeat_var, font=("Arial", 11))
        repeat_spin.pack(pady=5)

        tk.Label(dialog, text="点击间隔(秒):", font=("Arial", 10)).pack(pady=10)
        interval_var = tk.DoubleVar(value=task['interval'])
        interval_spin = tk.Spinbox(dialog, from_=0.1, to=10.0, increment=0.1,
                                   textvariable=interval_var, font=("Arial", 11))
        interval_spin.pack(pady=5)

        def update():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("警告", "请输入任务名称!")
                return

            self.task_manager.update_task(
                task_id,
                name=name,
                repeat_count=repeat_var.get(),
                interval=interval_var.get()
            )

            messagebox.showinfo("成功", "任务已更新!")
            dialog.destroy()
            self.refresh_task_list()

        tk.Button(dialog, text="更新", command=update, bg="#2196F3",
                 fg="white", font=("Arial", 11, "bold")).pack(pady=20)

    def delete_selected_task(self):
        """删除选中任务"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要删除的任务!")
            return

        task_id = selected[0]
        task = self.task_manager.get_task(task_id)

        if messagebox.askyesno("确认删除", f"确定要删除任务 '{task['name']}' 吗?"):
            self.task_manager.delete_task(task_id)
            self.refresh_task_list()
            messagebox.showinfo("成功", "任务已删除!")

    def run_selected_task(self):
        """运行选中任务"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要运行的任务!")
            return

        task_id = selected[0]
        task = self.task_manager.get_task(task_id)

        if task['status'] == 'running':
            messagebox.showwarning("警告", "该任务正在运行中!")
            return

        if self.clicker.start_task(task_id):
            messagebox.showinfo("成功", f"任务 '{task['name']}' 已启动!")
            self.refresh_task_list()
            self.update_process_list()
        else:
            messagebox.showerror("错误", "任务启动失败!")

    def stop_selected_task(self):
        """停止选中任务"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请选择要停止的任务!")
            return

        task_id = selected[0]
        self.clicker.stop_task(task_id)
        messagebox.showinfo("成功", "任务已停止!")
        self.refresh_task_list()
        self.update_process_list()

    def update_process_list(self):
        """更新进程列表"""
        processes = self.task_manager.get_running_processes()

        self.process_text.delete(1.0, tk.END)

        if not processes:
            self.process_text.insert(tk.END, "暂无运行中的进程\n")
        else:
            for task_id, proc_info in processes.items():
                task = self.task_manager.get_task(task_id)
                task_name = task['name'] if task else task_id

                info = f"""任务: {task_name}
ID: {task_id}
启动时间: {proc_info['started_at']}
状态: {proc_info['status']}
{'='*50}\n"""
                self.process_text.insert(tk.END, info)

        # 每5秒更新一次
        self.root.after(5000, self.update_process_list)

    def update_logs(self):
        """更新日志显示"""
        logs = self.task_manager.get_logs(100)

        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)

        for log in logs:
            timestamp = log['timestamp']
            level = log['level']
            message = log['message']

            log_line = f"[{timestamp}] [{level}] {message}\n"
            self.log_text.insert(tk.END, log_line, level)

        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

        # 每2秒更新一次
        self.root.after(2000, self.update_logs)

    def clear_logs(self):
        """清空日志"""
        if messagebox.askyesno("确认", "确定要清空所有日志吗?"):
            self.task_manager.clear_logs()
            messagebox.showinfo("成功", "日志已清空!")

    def export_logs(self):
        """导出日志"""
        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialfilename=f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        if file_path:
            logs = self.task_manager.get_logs()
            with open(file_path, 'w', encoding='utf-8') as f:
                for log in logs:
                    line = f"[{log['timestamp']}] [{log['level']}] {log['message']}\n"
                    f.write(line)

            messagebox.showinfo("成功", f"日志已导出到:\n{file_path}")

    def show_task_manager(self):
        """显示任务管理器(切换到任务选项卡)"""
        # 找到notebook并切换到任务选项卡
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Notebook):
                widget.select(1)  # 切换到第二个选项卡(任务管理)
                break

    def exit_app(self):
        """退出应用"""
        if messagebox.askokcancel("退出", "确定要退出程序吗?\n所有运行中的任务将被停止。"):
            self.clicker.stop_task()
            self.root.quit()


def main():
    # 检查依赖
    try:
        import pyautogui
        from pynput import mouse, keyboard
    except ImportError:
        print("请先安装必要的库:")
        print("pip install pyautogui pynput")
        sys.exit(1)

    # 禁用pyautogui的失败安全保护(可选)
    pyautogui.FAILSAFE = True

    root = tk.Tk()
    app = AutoClickerGUI(root)

    # 居中窗口
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
