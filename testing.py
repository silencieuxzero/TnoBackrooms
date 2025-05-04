import tkinter as tk


class PoliticalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("M.E.G.CN 政治模拟系统")

        # 领导人数据字典（根据战争支持度划分）
        self.leader_data = {
            'high': {'MPP_C_leader_1': 'Aread (鹰派)', 'MPP_C_leader_2': 'Maxwellyang (强硬派)'},
            'medium': {'MPP_C_leader_1': 'Smith (稳健派)', 'MPP_C_leader_2': 'Lee (协商派)'},
            'low': {'MPP_C_leader_1': 'Green (鸽派)', 'MPP_C_leader_2': 'White (和平派)'}
        }

        # 支持率变量
        self.support_rate_p = tk.IntVar(value=20)  # 进步党团
        self.support_rate_c = tk.IntVar(value=50)  # 保守党团
        self.support_rate_u = tk.IntVar(value=30)  # 统合党团
        self.support_rate_stable = tk.IntVar(value=80)  # 稳定度
        self.support_rate_war = tk.IntVar(value=30)  # 战争支持度
        self.support_rate_war.trace_add("write", self.update_leader)  # 动态监听变化

        # 当前领导人显示变量
        self.current_leader = tk.StringVar()
        self.update_leader()  # 初始化领导人显示

        # GUI布局
        self.create_widgets()

    def update_leader(self, *args):
        """根据战争支持度更新领导人"""
        war_rate = self.support_rate_war.get()
        if war_rate >= 70:
            self.current_leader.set(self.leader_data['high']['MPP_C_leader_1'])
        elif war_rate >= 30:
            self.current_leader.set(self.leader_data['medium']['MPP_C_leader_1'])
        else:
            self.current_leader.set(self.leader_data['low']['MPP_C_leader_1'])

    def create_widgets(self):
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
        tk.Label(self, textvariable=self.current_leader, font=("微软雅黑", 10), fg="blue").place(x=40, y=160)
        tk.Label(self, text="当前领导人:", font=("微软雅黑", 10)).place(x=10, y=160)

        # 战争支持度滑动条（测试用）
        tk.Scale(
            self, from_=0, to=100, orient=tk.HORIZONTAL,
            variable=self.support_rate_war,
            label="调整战争支持度",
            command=lambda e: self.update_leader()
        ).place(x=200, y=20)


if __name__ == "__main__":
    app = PoliticalApp()
    app.geometry("500x300")
    app.mainloop()