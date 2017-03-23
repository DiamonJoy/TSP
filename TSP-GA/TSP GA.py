# -*- coding: utf-8 -*-

import sys
import random
import math
import time
import Tkinter
import threading

# 城市坐标
distance_x = [
    178,272,176,171,650,499,267,703,408,437,491,74,532,
    416,626,42,271,359,163,508,229,576,147,560,35,714,
    757,517,64,314,675,690,391,628,87,240,705,699,258,
    428,614,36,360,482,666,597,209,201,492,294]
distance_y = [
    170,395,198,151,242,556,57,401,305,421,267,105,525,
    381,244,330,395,169,141,380,153,442,528,329,232,48,
    498,265,343,120,165,50,433,63,491,275,348,222,288,
    490,213,524,244,114,104,552,70,425,227,331]

# 遗传算法类
from GA import GA

#----------- TSP问题 -----------
class MyTSP(object):

    # 初始化
    def __init__(self, root, width = 800, height = 600, n = 50):

        # 创建画布
        self.root = root                               
        self.width = width      
        self.height = height
        # 城市数目初始化为32
        self.n = n
        # Tkinter.Canvas
        self.canvas = Tkinter.Canvas(
                root,
                width = self.width,
                height = self.height,
                bg = "#EBEBEB",             # 背景白色 
                xscrollincrement = 1,
                yscrollincrement = 1
            )
        self.canvas.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
        self.title("TSP遗传算法(n:随机初始 e:开始进化 s:停止进化 q:退出程序)")
        self.__r = 5
        self.__lock = threading.RLock()     # 线程锁

        self.__bindEvents()
        self.new()

    # 按键响应程序
    def __bindEvents(self):

        self.root.bind("q", self.quite)    # 退出程序
        self.root.bind("n", self.new)      # 随机初始
        self.root.bind("e", self.evolve)   # 开始进化
        self.root.bind("s", self.stop)     # 停止进化

    # 更改标题
    def title(self, s):

        self.root.title(s)
            
    # 随机初始
    def new(self, evt = None):

        # 停止线程
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

        self.clear()     # 清除信息 
        self.nodes = []  # 节点坐标
        self.nodes2 = [] # 节点对象

        # 初始化城市节点
        for i in range(len(distance_x)):
            # 在画布上随机初始坐标
            x = distance_x[i]
            y = distance_y[i]
            self.nodes.append((x, y))
            # 生成节点椭圆，半径为self.__r
            node = self.canvas.create_oval(x - self.__r,
                    y - self.__r, x + self.__r, y + self.__r,
                    fill = "#ff0000",      # 填充红色
                    outline = "#000000",   # 轮廓白色
                    tags = "node",
                )
            self.nodes2.append(node)
            # 显示坐标
            self.canvas.create_text(x,y-10,              # 使用create_text方法在坐标（302，77）处绘制文字  
                    text = '('+str(x)+','+str(y)+')',    # 所绘制文字的内容  
                    fill = 'black'                       # 所绘制文字的颜色为灰色
                )
            
        # 顺序连接城市
        self.line(range(self.n))      
        
        # 遗传算法
        self.ga = GA(
                lifeCount = 50,
                xRate = 0.7,
                mutationRate = 0.1,
                judge = self.judge(),
                mkLife = self.mkLife(),
                xFunc = self.xFunc(),
                mFunc = self.mFunc(),
                save = self.save()
            )

    # 得到当前顺序下连线总长度
    def distance(self, order):
        
        distance = 0
        for i in range(-1, self.n - 1):
            i1, i2 = order[i], order[i + 1]
            p1, p2 = self.nodes[i1], self.nodes[i2]
            distance += math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        return distance

    # 创造新生命
    def mkLife(self):
        def f():
            lst = range(self.n)
            # 随机顺序
            random.shuffle(lst)
            return lst
        return f

    # 评价函数
    def judge(self):
            
        return lambda lf, av = 100: 1.0 / self.distance(lf.gene)

    # 交叉函数：选择lf2序列前子序列交叉到lf1前段，删除重复元素
    def xFunc(self):
            
        def f(lf1, lf2):
            p2 = random.randint(1, self.n - 1)
            # 截取if2
            g1 = lf2.gene[0:p2] + lf1.gene
            g11 = []
            for i in g1:
                if i not in g11:
                    g11.append(i)
            return g11
        return f
        
    # 变异函数:选择两个不同位置基因交换，第一个选择的基因重新加入到序列尾端
    def mFunc(self):
            
        def f(gene):
            p1 = random.randint(0, self.n - 1)
            p2 = random.randint(0, self.n - 1)
            while p2 == p1:
                p2 = random.randint(0, self.n - 1)
            gene[p1], gene[p2] = gene[p2], gene[p1]
            gene.append(gene[p2])
            del gene[p2]
            return gene
            
        return f

    # 保存
    def save(self):
        def f(lf, gen):
            pass
        return f

    # 进化计算
    def evolve(self, evt = None):

        # 开启线程
        self.__lock.acquire()
        self.__running = True
        self.__lock.release()

        while self.__running:
            # 下一步进化
            self.ga.next()
            # 连线
            self.line(self.ga.best.gene)
            # 设置标题
            self.title("TSP遗传算法(n:随机初始 e:开始进化 s:停止进化 q:退出程序) 迭代次数: %d" % self.ga.generation)
            # 更新画布
            self.canvas.update()
            print("迭代次数：%d, 变异次数%d, 最佳路径总距离：%d" % (self.ga.generation, self.ga.mutationCount, self.distance(self.ga.best.gene))) 

    # 将节点按order顺序连线
    def line(self, order):
        # 删除原线
        self.canvas.delete("line")
        def line2(i1, i2):
            p1, p2 = self.nodes[i1], self.nodes[i2]
            self.canvas.create_line(p1, p2, fill = "#000000", tags = "line")
            return i2
        
        # order[-1]为初始值
        reduce(line2, order, order[-1])

    # 清除画布
    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    # 退出程序
    def quite(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()
        self.root.destroy()
        print u"\n程序已退出..."
        sys.exit()

    # 停止进化
    def stop(self, evt):
        self.__lock.acquire()
        self.__running = False
        self.__lock.release()

    # 主循环
    def mainloop(self):
        self.root.mainloop()

#----------- 程序的入口处 -----------
        
if __name__ == "__main__":
    
    print u""" 
--------------------------------------------------------
    程序：遗传算法解决TPS问题程序 
    作者：许彬 
    日期：2015-12-10
    语言：Python 2.7 
-------------------------------------------------------- 
    """
    
    MyTSP(Tkinter.Tk()).mainloop()
