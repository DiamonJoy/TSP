# -*- coding: utf-8 -*-

import random

# 生命类
from Life import Life

#----------- 遗传算法 -----------
class GA(object):

    # 初始化
    def __init__(self, xRate = 0.7, mutationRate = 0.005, lifeCount = 50, geneLength = 50, judge = lambda lf, av: 1, save = lambda: 1, mkLife = lambda: None, xFunc = None, mFunc = None):
        self.xRate = xRate                                  # 交叉率 
        self.mutationRate = mutationRate                    # 突变率
        self.mutationCount = 0                              # 突变次数
        self.generation = 0                                 # 进化代数
        self.lives = []                                     # 生命集合
        self.bounds = 0.0                                   # 得分总数    
        self.best = None                                    # 最优解
        self.lifeCount = lifeCount                          # 生命个数
        self.geneLength = geneLength                        # 基因长度
        self.__judge = judge                                # 评价函数
        self.save = save                                    # 保存函数
        self.mkLife = mkLife                                # 默认的产生生命的函数
        self.xFunc = (xFunc, self.__xFunc)[xFunc == None]   # 自定义交叉函数
        self.mFunc = (mFunc, self.__mFunc)[mFunc == None]   # 自定义变异函数

        # 创造生命集
        for i in range(lifeCount):
            self.lives.append(Life(self, self.mkLife()))

    # 默认交叉函数
    def __xFunc(self, p1, p2):
        
        r = random.randint(0, self.geneLength)
        gene = p1.gene[0:r] + p2.gene[r:]
        return gene
    
    # 默认突变函数
    def __mFunc(self, gene):
        
        r = random.randint(0, self.geneLength - 1)
        gene = gene[:r] + ("0", "1")[gene[r:r] == "1"] + gene[r + 1:]
        return gene

    # 产生后代
    def __bear(self, p1, p2):

        # 交叉
        r = random.random()
        if r < self.xRate:
            gene = self.xFunc(p1, p2)
        else:
            gene = p1.gene

        # 突变
        r = random.random()
        if r < self.mutationRate:
            gene = self.mFunc(gene)
            self.mutationCount += 1

        # 返回生命体
        return Life(self, gene)

    # 根据得分情况，随机取得一个个体，机率正比于个体的score属性
    def __getOne(self):
        # 轮盘
        r = random.uniform(0, self.bounds)
        for lf in self.lives:
            r -= lf.score;
            if r <= 0:
                return lf
    # 产生新的后代 
    def __newChild(self):
        
        return self.__bear(self.__getOne(), self.__getOne())

    # 根据传入的方法f，求得最优生命体和生命集总分
    def judge(self, f = lambda lf, av: 1):
        # 平均分
        lastAvg = self.bounds / float(self.lifeCount)
        self.bounds = 0.0
        self.best = Life(self)
        self.best.setScore(-1.0)
        for lf in self.lives:
            lf.score = f(lf, lastAvg)
            if lf.score > self.best.score:
                self.best = lf
            self.bounds += lf.score
            
    # 演化至下n代
    def next(self, n = 1):
        
        while n > 0:
            # 评估群体
            self.judge(self.__judge)
            # 新生命集
            newLives = []
            newLives.append(Life(self, self.best.gene))  # 将最好的父代加入竞争
            # 产生新的生命集个体
            while (len(newLives) < self.lifeCount):
                newLives.append(self.__newChild())
            # 更新新的生命集
            self.lives = newLives
            self.generation += 1
            self.save(self.best, self.generation)

            n -= 1
