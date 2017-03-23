# -*- coding: utf-8 -*-

import random

#----------- 生命体 -----------
class Life(object):

    # 初始化
    def __init__(self, env, gene = None):

        # 遗传算法
        self.env = env

        # 生命体基因
        if gene == None:
            self.__rndGene()
        elif type(gene) == type([]):
            self.gene = []
            for k in gene:
                self.gene.append(k)
        else:
            self.gene = gene

    # 随机初始化基因
    def __rndGene(self):
        self.gene = ""
        for i in range(self.env.geneLength):
            self.gene += str(random.randint(0, 1))

    # 设置评估分数
    def setScore(self, v):
        self.score = v

    # 增加评价分数
    def addScore(self, v):
        self.score += v
