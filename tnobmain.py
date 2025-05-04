import os
import tkinter as tk
from struct import pack
from tkinter import scrolledtext
from tkinter import Tk, simpledialog, messagebox
import idx
import webbrowser as web


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("新秩序：后室末日")
        self.root.geometry("600x400")
        self.root.resizable(0, 0)

        # 创建页面容器
        self.frames = {}
        for Page in (MainPage, SettingsPage, HelpPage, StartPage, PoliticalPanel, EconomicPanel, ResolutionPanel, DiplomaticPanel):
            frame = Page(parent=self.root, controller=self)
            self.frames[Page.__name__] = frame
            frame.place(x=0, y=0, relwidth=1, relheight=1)  # 填充整个窗口

        self.show_frame("MainPage")  # 初始显示主页
        self.center_window()

    def center_window(self):
        """ 窗口居中 """
        self.root.update()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"+{x}+{y}")

    def show_frame(self, page_name):
        """ 显示指定页面 """
        frame = self.frames[page_name]
        frame.tkraise()  # 提升到最前

#三个党团的支持率字典
MPP_Us = {}
MPP_Cs = {}
MPP_Ps = {}

class BasePage(tk.Frame):
    """ 页面基类 """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        pass


class MainPage(BasePage):
    def create_widgets(self):
        # 标题
        tk.Label(self, text="M.E.G.CN事务系统", font=("微软雅黑", 24)).pack(pady=40)

        # 功能按钮
        buttons = [
            ("开始游戏", "StartPage"),
            ("进入设置", "SettingsPage"),
            ("帮助文档", self.helpword),
            ("退出程序", self.controller.root.destroy)
        ]

        for text, command in buttons:
            btn = tk.Button(
                self,
                text=text,
                width=15,
                command=lambda cmd=command: self.handle_command(cmd)
            )
            btn.pack(pady=10)

    def handle_command(self, command):
        if isinstance(command, str):
            self.controller.show_frame(command)
        else:
            command()

    def helpword(self):
        """ 增加支持率的方法 """
        web.open("https://luoxirain.netlify.app/")


class SettingsPage(BasePage):
    def create_widgets(self):
        # 返回按钮
        tk.Button(
            self,
            text="返回主页",
            command=lambda: self.controller.show_frame("MainPage")
        ).pack(anchor="nw", padx=20, pady=10)

        # 设置内容
        tk.Label(self, text="系统设置", font=("微软雅黑", 20)).pack(pady=30)

        # 设置项
        settings = ["主题设置", "通知管理", "账户安全"]
        for item in settings:
            tk.Button(self, text=item).pack(pady=5)


class HelpPage(BasePage):
    def create_widgets(self):
        tk.Button(
            self,
            text="返回主页",
            command=lambda: self.controller.show_frame("MainPage")
        ).pack(anchor="nw", padx=20, pady=10)

# 设置内容
        tk.Label(self, text="系统设置", font=("微软雅黑", 20)).pack(pady=30)

        # 设置项
        settings = ["主题设置", "通知管理", "账户安全"]
        for item in settings:
            tk.Button(self, text=item).pack(pady=5)

class StartPage(BasePage):
    def create_widgets(self):
        # 返回按钮
        tk.Button(
            self,
            text="返回主页",
            command=lambda: self.controller.show_frame("MainPage")
        ).pack(anchor="nw", padx=20, pady=10)

        # 设置内容
        tk.Label(self, text="欢迎回来", font=("微软雅黑", 15)).pack(pady=30)

        # 设置项
        options = [
            ("打开政治面板", "PoliticalPanel", "政治面板"),
            ("打开经济面板", "EconomicPanel", "经济面板"),
            ("打开决议面板", "ResolutionPanel", "决议面板"),
            ("打开外交面板", "DiplomaticPanel", "外交面板")
        ]
        for item in options:
            tk.Button(self, text=item[2],
                      width=15,  # 宽度（字符单位）
                      height=1,  # 高度（文本行数）
                      command=lambda cmd=item[1]: self.start_command(cmd)
                      ).pack(side="left", fill="x", padx=17)

    def start_command(self, command):
        if isinstance(command, str):
            self.controller.show_frame(command)
        else:
            command()

# 政治面板
class PoliticalPanel(BasePage):
    def create_widgets(self):
        # 返回按钮
        tk.Button(
            self,
            text="返回控制面板",
            command=lambda: self.controller.show_frame("StartPage")
        ).grid(row=0, column=0, sticky="nw", padx=20, pady=10)

        # 标题
        tk.Label(self, text="M.E.G.CN政治分析系统", font=("微软雅黑", 15)).place(x=190, y=20)

        self.leader_data = {
            'high': {'MPP_U_leader_1': 'Adaihappyjan（MPP-U）', 'MPP_U_leader_2': 'Maxwellyang (强硬派)'},
            'medium': {'MPP_C_leader_1': 'MaxwellYang（MPP-C）', 'MPP_C_leader_2': 'Lee (协商派)'},
            'low': {'MPP_P_leader_1': '南岸青栀（MPP-P）', 'MPP_P_leader_2': 'White (和平派)'}
        }

        # 支持率变量
        self.support_rate_p = tk.IntVar(value=20)  # 初始支持率为20%
        self.support_rate_c = tk.IntVar(value=50)  # 初始支持率为50%
        self.support_rate_u = tk.IntVar(value=30)  # 初始支持率为30%
        self.support_rate_stable = tk.IntVar(value=80)  # 初始稳定度为80%
        self.support_rate_war = tk.IntVar(value=30)  # 初始战争支持度为30%
        # 绑定动态监听
        self.support_rate_p.trace_add("write", self.update_leader)
        self.support_rate_c.trace_add("write", self.update_leader)
        self.support_rate_u.trace_add("write", self.update_leader)
        self.support_rate_stable.trace_add("write", self.over)


        # 当前领导人显示变量
        self.current_leader = tk.StringVar()
        self.update_leader()  # 初始化领导人显示

        # GUI布局
        self.setup_gui()

    def over (self, *args):
        support_rate_stable = self.support_rate_stable.get()
        # 根据稳定度决定是否爆事件
        stable_rate = self.support_rate_stable.get()
        if stable_rate >= 70:
            print('high')
        elif stable_rate >= 30:
            self.stablerate()
        else:
            print('low')

    def stablerate(self):
        """同时执行两个操作的组合函数"""
        self.open_child_window_mediumstable()  # 弹出子窗口

    # 稳定度事件medium
    def open_child_window_mediumstable(self):
        """ 弹出子窗口 """
        child_window_mediumstable = tk.Toplevel(self)  # 创建子窗口
        child_window_mediumstable.title("事件")  # 设置子窗口标题
        child_window_mediumstable.geometry("650x700")  # 设置子窗口大小

        # 在子窗口中添加一些内容
        tk.Label(child_window_mediumstable, text="崩溃之始……", font=("微软雅黑", 14)).pack(pady=20)

        # 添加更多文本
        file_path = "./assets/other_word/medium_stable.txt"

        with open(file_path, "r", encoding="utf-8") as file:
            content_p = file.read()
            tk.Label(child_window_mediumstable, text=content_p, anchor="w", justify="left", wraplength=600, font=("微软雅黑", 10)).pack(pady=10)
            tk.Button(child_window_mediumstable, text="“灯火微弱……”", command=child_window_mediumstable.destroy).pack(pady=10)

    def update_leader(self, *args):
        """根据战争支持度比较更新领导人"""
#        war_rate = self.support_rate_war.get()
#        print(f"Current war support rate: {war_rate}")  # 调试信息
        # 获取各派系的支持度
        support_rate_p = self.support_rate_p.get()
        support_rate_c = self.support_rate_c.get()
        support_rate_u = self.support_rate_u.get()

        # 比较支持度并更新领导人
        if support_rate_p > support_rate_c and support_rate_p > support_rate_u:
            # 如果 P 派系支持度最高
            self.current_leader.set(self.leader_data['low']['MPP_P_leader_1'])
        elif support_rate_c > support_rate_p and support_rate_c > support_rate_u:
            # 如果 C 派系支持度最高
            self.current_leader.set(self.leader_data['medium']['MPP_C_leader_1'])
        elif support_rate_u > support_rate_p and support_rate_u > support_rate_c:
            # 如果 U 派系支持度最高
            self.current_leader.set(self.leader_data['high']['MPP_U_leader_1'])
        else:
            # 如果支持度相同或未定义
            self.current_leader.set(self.leader_data['medium']['MPP_C_leader_1'])

    def increase_support_rate_war(self, increment):
        """增加战争支持度并更新领导人"""
        current_rate = self.support_rate_war.get()
        self.support_rate_war.set(current_rate + increment)
        self.update_leader()  # 更新领导人

    def setup_gui(self):
        """设置 GUI 布局"""
        # 支持率标签组
        rates = [
            (self.support_rate_p, 120, "MPP-P(M.E.G.CN进步公约-进步党团)"),
            (self.support_rate_c, 100, "MPP-C(M.E.G.CN进步公约-保守党团)"),
            (self.support_rate_u, 80, "MPP-U(M.E.G.CN进步公约-统合党团)"),
            (self.support_rate_stable, 60, "M.E.G.CN稳定度"),
            (self.support_rate_war, 140, "战争支持度")
        ]

        for var, y, text in rates:
                tk.Label(self, textvariable=var, font=("微软雅黑", 10)).place(x=10, y=y)
                tk.Label(self, text=f"% 当前{text}", font=("微软雅黑", 10)).place(x=40, y=y)

            # 领导人显示
        tk.Label(self, textvariable=self.current_leader, font=("微软雅黑", 10), fg="blue").place(x=90, y=160)
        tk.Label(self, text="当前领导人:", font=("微软雅黑", 10)).place(x=10, y=160)

        # 稳定度滑动条（测试用）
        tk.Scale(
            self, from_=0, to=100, orient=tk.HORIZONTAL,
            variable=self.support_rate_stable,
            label="调整稳定度",
            command=lambda e: self.update_leader()
        ).place(x=200, y=20)

        # 显示支持率的标签
        self.rate_label = tk.Label(self, textvariable=self.support_rate_p, font=("微软雅黑", 10))
        self.rate_label.place(x=10, y=120)  # 数字位置
        self.text_label = tk.Label(self, text="% 当前MPP-P(M.E.G.CN进步公约-进步党团)支持率", font=("微软雅黑", 10))
        self.text_label.place(x=40, y=120)  # 文字位置

        self.rate_label_c = tk.Label(self, textvariable=self.support_rate_c, font=("微软雅黑", 10))
        self.rate_label_c.place(x=10, y=100)  # 数字位置
        self.text_label_c = tk.Label(self, text="% 当前MPP-C(M.E.G.CN进步公约-保守党团)支持率", font=("微软雅黑", 10))
        self.text_label_c.place(x=40, y=100)  # 文字位置

        self.rate_label_u = tk.Label(self, textvariable=self.support_rate_u, font=("微软雅黑", 10))
        self.rate_label_u.place(x=10, y=80)  # 数字位置
        self.text_label_u = tk.Label(self, text="% 当前MPP-U(M.E.G.CN进步公约-统合党团)支持率", font=("微软雅黑", 10))
        self.text_label_u.place(x=40, y=80)  # 文字位置

        self.rate_label = tk.Label(self, textvariable=self.support_rate_stable, font=("微软雅黑", 10))
        self.rate_label.place(x=10, y=60)  # 数字位置
        self.text_label = tk.Label(self, text="% 当前M.E.G.CN稳定度", font=("微软雅黑", 10))
        self.text_label.place(x=40, y=60)  # 文字位置

        self.rate_label = tk.Label(self, textvariable=self.support_rate_war, font=("微软雅黑", 10))
        self.rate_label.place(x=10, y=140)  # 数字位置
        self.text_label = tk.Label(self, text="% 当前战争支持度", font=("微软雅黑", 10))
        self.text_label.place(x=40, y=140)  # 文字位置

        # 设置项
        politicaloptions = [
            ("增加支持率", self.increase_support_rate_p, "增加MPP-P支持率"),  # 新增按钮
            ("增加支持率", self.increase_support_rate_c, "增加MPP-C支持率"),
            ("增加支持率", self.increase_support_rate_u, "增加MPP-U支持率"),
            ("减少支持率", self.increase_support_rate_np, "减少MPP-P支持率"),  # 新增按钮
            ("减少支持率", self.increase_support_rate_nc, "减少MPP-C支持率"),
            ("减少支持率", self.increase_support_rate_nu, "减少MPP-U支持率"),
        ]

        # 配置最后一行以扩展到窗口底部
        self.grid_rowconfigure(1, weight=1)  # 第二行扩展
        self.grid_rowconfigure(2, weight=0)  # 按钮所在行不扩展

        # 计算每行应该有多少个按钮
        buttons_per_row = 4  # 每行放置3个按钮

        for i, item in enumerate(politicaloptions):
            if callable(item[1]):  # 如果是函数，则直接使用
                command = item[1]
            else:
                command = lambda cmd=item[1]: self.start_command(cmd)

            # 计算行和列的位置
            row = 2 + i // buttons_per_row  # 按钮分布在多行
            column = i % buttons_per_row

            tk.Button(self, text=item[2],
                      width=15,  # 宽度（字符单位）
                      height=1,  # 高度（文本行数）
                      font=("微软雅黑", 10),  # 指定字体
                      command=command
                      ).grid(row=row, column=column, padx=2, pady=2, sticky="s")

        # 配置列的权重，使按钮均匀分布
        for col in range(buttons_per_row):
            self.grid_columnconfigure(col, weight=1)

    # 以下为加支持率
    def increase_support_rate_p(self):
        """ 增加支持率的方法 """
        current_rate_p = self.support_rate_p.get()
        new_rate = min(current_rate_p + 1, 100)  # 每次增加1%，最大为100%
        self.support_rate_p.set(new_rate)

    def increase_support_rate_c(self):
        """ 增加支持率的方法 """
        current_rate_c = self.support_rate_c.get()
        new_rate = min(current_rate_c + 1, 100)
        self.support_rate_c.set(new_rate)

    def increase_support_rate_u(self):
        """ 增加支持率的方法 """
        current_rate_u = self.support_rate_u.get()
        new_rate = min(current_rate_u + 1, 100)
        self.support_rate_u.set(new_rate)

    # 以下为减支持率
    def increase_support_rate_np(self):
        """ 减少支持率的方法 """
        current_rate_np = self.support_rate_p.get()
        new_rate = min(current_rate_np - 1, 100)
        self.support_rate_p.set(new_rate)

    def increase_support_rate_nc(self):
        """ 减少支持率的方法 """
        current_rate_nc = self.support_rate_c.get()
        new_rate = min(current_rate_nc - 1, 100)
        self.support_rate_c.set(new_rate)

    def increase_support_rate_nu(self):
        """ 减少支持率的方法 """
        current_rate_nu = self.support_rate_u.get()
        new_rate = min(current_rate_nu - 1, 100)
        self.support_rate_u.set(new_rate)

    def increase_support_rate_war(self):
        """ 增加战争支持度的方法 """
        current_rate_nu = self.support_rate_war.get()
        new_rate = min(current_rate_nu + 1, 0)
        self.support_rate_war.set(new_rate)

    def increase_support_rate_nwar(self):
        """ 减少战争支持度的方法 """
        current_rate_nu = self.support_rate_war.get()
        new_rate = min(current_rate_nu - 1, 100)
        self.support_rate_war.set(new_rate)

    def increase_support_rate_stable(self):
        """ 增加稳定度的方法 """
        current_rate_nu = self.support_rate_stable.get()
        new_rate = min(current_rate_nu + 1, 100)
        self.support_rate_stable.set(new_rate)

    def increase_support_rate_nstable(self):
        """ 减少稳定度的方法 """
        current_rate_nu = self.support_rate_stable.get()
        new_rate = min(current_rate_nu - 1, 100)
        self.support_rate_stable.set(new_rate)

    def start_command(self, command):
        if isinstance(command, str):
            self.controller.show_frame(command)
        else:
            command()

# 经济面板
class EconomicPanel(BasePage):
    def create_widgets(self):
        # 返回按钮
        tk.Button(
            self,
            text="返回主页",
            command=lambda: self.controller.show_frame("MainPage")
        ).pack(anchor="nw", padx=20, pady=10)

        # 设置内容
        tk.Label(self, text="新秩序：后室末日", font=("微软雅黑", 15)).pack(pady=30)

        # 设置项
        options = {
            ("打开政治面板", "PoliticalPanel"),
            ("打开经济面板", "EconomicPanel"),
            ("打开决议面板", "ResolutionPanel"),
            ("打开外交面板", "DiplomaticPanel")
        }
        for item in options:
            tk.Button(self, text=item,
                      width=15,  # 宽度（字符单位）
                      height=1  # 高度（文本行数）
                      ).pack(side="left", fill="x", padx=17)

# 决议面板
class ResolutionPanel(BasePage):
    def create_widgets(self):
        # 返回按钮
        tk.Button(
            self,
            text="返回控制面板",
            command=lambda: self.controller.show_frame("StartPage")
        ).pack(anchor="nw", padx=20, pady=10)

        # 标题
        tk.Label(self, text="M.E.G.CN归档文件处理系统", font=("微软雅黑", 15)).place(x=190, y=20)

        # 设置项
        self.execute_button_p = tk.Button(
            self,
            text="冬月变奏-1",
            command=self.combined_operation,
            width=30,  # 宽度（字符单位）
            height=1,  # 高度（文本行数）
            font=("微软雅黑", 10),  # 指定字体
            #command=lambda: self.increase_support_rate_p#("StartPage")
        )
        self.execute_button_p.pack(padx=20, pady=10)

        self.execute_button_u = tk.Button(
            self,
            text="MPP-U背景故事",
            command=self.combined_operation_u,
            width=30,  # 宽度（字符单位）
            height=1,  # 高度（文本行数）
            font=("微软雅黑", 10),  # 指定字体
            #command=lambda: self.increase_support_rate_p#("StartPage")
        )
        self.execute_button_u.pack(padx=20, pady=10)

        self.execute_button_c = tk.Button(
            self,
            text="MPP-C背景故事",
            command=self.combined_operation_c,
            width=30,  # 宽度（字符单位）
            height=1,  # 高度（文本行数）
            font=("微软雅黑", 10),  # 指定字体
            #command=lambda: self.increase_support_rate_p#("StartPage")
        )
        self.execute_button_c.pack(padx=20, pady=10)

    def combined_operation(self):
        """同时执行两个操作的组合函数"""
        self.execute_button_p.pack_forget()
        self.open_child_window_p()  # 弹出子窗口
        self.increase_support_rate_p()  # 改变支持率

    def combined_operation_u(self):
        """同时执行两个操作的组合函数"""
        self.execute_button_u.pack_forget()
        self.open_child_window_u()  # 弹出子窗口
        self.increase_support_rate_u()  # 改变支持率

    def combined_operation_c(self):
        """同时执行两个操作的组合函数"""
        self.execute_button_c.pack_forget()
        self.open_child_window_c()  # 弹出子窗口
        self.increase_support_rate_c()  # 改变支持率

#        for item in resolutionoptions:
#            # 使用lambda捕获当前item[1]的值
#            if callable(item[1]):
#                command = lambda x=item[1]: x()  # 显式调用可调用对象
#            else:
#                command = lambda cmd=item[1]: self.start_command(cmd)

    def increase_support_rate_p(self):
        political_panel = self.controller.frames["PoliticalPanel"]
        count1 = 0
        count2 = 0
        count3 = 0
        while count1 < 20:  # 循环2次
            political_panel.increase_support_rate_nu()
            count1 += 1
        while count2 < 20:  # 循环2次
            political_panel.increase_support_rate_p()
            count2 += 1
        while count3 < 60:  # 循环2次
            political_panel.increase_support_rate_nstable()
            count3 += 1
#        political_panel.increase_support_rate_nu()
#        political_panel.increase_support_rate_nu()

    def increase_support_rate_u(self):
        political_panel = self.controller.frames["PoliticalPanel"]
        political_panel.increase_support_rate_u()

    def increase_support_rate_c(self):
        political_panel = self.controller.frames["PoliticalPanel"]
        political_panel.increase_support_rate_c()

#            tk.Button(self, text=item[2],
#                      width=15,  # 宽度（字符单位）
#                      height=1,  # 高度（文本行数）
#                      font=("微软雅黑", 10),  # 指定字体
#                      command=command
#            ).pack(side="top", fill="x", padx=5, pady=10)

#    def increase_support_rate_p(self):
#        """ 增加支持率的方法 """
#        current_rate_p = self.support_rate_p.get()
#        new_rate = min(current_rate_p + 10, 100)  # 每次增加10%，最大为100%
#        self.support_rate_p.set(new_rate)

    def open_child_window_p(self):
        """ 弹出子窗口 """
        child_window_p = tk.Toplevel(self)  # 创建子窗口
        child_window_p.title("事件")  # 设置子窗口标题
        child_window_p.geometry("650x700")  # 设置子窗口大小

        # 在子窗口中添加一些内容
        tk.Label(child_window_p, text="华屋秋墟：冬月变奏", font=("微软雅黑", 14)).pack(pady=20)

        # 添加更多文本
        file_path = "./assets/mpp_p_word/mpp_p_1.txt"

        with open(file_path, "r", encoding="utf-8") as file:
            content_p = file.read()
            tk.Label(child_window_p, text=content_p, anchor="w", justify="left", wraplength=600, font=("微软雅黑", 10)).pack(pady=10)
            tk.Button(child_window_p, text="“你在亲手毁掉M.E.G.CN”", command=child_window_p.destroy).pack(pady=10)

    def open_child_window_u(self):
        """ 弹出子窗口 """
        child_window_u = tk.Toplevel(self)  # 创建子窗口
        child_window_u.title("事件")  # 设置子窗口标题
        child_window_u.geometry("650x700")  # 设置子窗口大小

        # 在子窗口中添加一些内容
        tk.Label(child_window_u, text="七号决议：落日行动", font=("微软雅黑", 14)).pack(pady=20)
        # 添加更多文本
        file_path = "./assets/mpp_u_word/mpp_u_1.txt"

        with open(file_path, "r", encoding="utf-8") as file:
            content_u = file.read()
            tk.Label(child_window_u, text=content_u, anchor="w", justify="left", wraplength=600, font=("微软雅黑", 10)).pack(pady=10)
            tk.Button(child_window_u, text="关闭", command=child_window_u.destroy).pack(pady=10)

    def open_child_window_c(self):
        """ 弹出子窗口 """
        child_window_c = tk.Toplevel(self)  # 创建子窗口
        child_window_c.title("事件")  # 设置子窗口标题
        child_window_c.geometry("650x700")  # 设置子窗口大小

        # 在子窗口中添加一些内容
        tk.Label(child_window_c, text="四号决议：希波克拉底计划", font=("微软雅黑", 14)).pack(pady=20)

        file_path = "./assets/mpp_c_word/mpp_c_1.txt"

        with open(file_path, "r", encoding="utf-8") as file:
            content_c = file.read()
            tk.Label(child_window_c, text=content_c, anchor="w", justify="left", wraplength=600, font=("微软雅黑", 10)).pack(pady=10)
            tk.Button(child_window_c, text="关闭", command=child_window_c.destroy).pack(pady=10)

    def start_command(self, command):
        if isinstance(command, str):
            self.controller.show_frame(command)
        else:
            command()

#外交面板
class DiplomaticPanel(BasePage):
    def create_widgets(self):
        # 返回按钮
        tk.Button(
            self,
            text="返回主页",
            command=lambda: self.controller.show_frame("MainPage")
        ).pack(anchor="nw", padx=20, pady=10)

        # 设置内容
        tk.Label(self, text="新秩序：后室末日", font=("微软雅黑", 15)).pack(pady=30)

        # 设置项
        options = {
            ("打开政治面板", "PoliticalPanel"),
            ("打开经济面板", "EconomicPanel"),
            ("打开决议面板", "ResolutionPanel"),
            ("打开外交面板", "DiplomaticPanel")
        }
        for item in options:
            tk.Button(self, text=item,
                      width=15,  # 宽度（字符单位）
                      height=1  # 高度（文本行数）
                      ).pack(side="left", fill="x", padx=17)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()