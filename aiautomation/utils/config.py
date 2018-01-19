# -*- coding:utf-8 -*-

import yaml


class Config:
    """
    用于读取Config.yaml文件，缓存读取内容，这里没有做同步处理，多线程可能会有问题
    """

    def __init__(self, filename):
        self.filename = filename
        self.config = None

    def obj_dic(self, d):
        """
        将dict转化成对象
        :param d:
        :return:
        """
        top = type('new', (object,), d)
        seqs = tuple, list, set, frozenset
        for i, j in d.items():
            if isinstance(j, dict):
                setattr(top, i, self.obj_dic(j))
            elif isinstance(j, seqs):
                setattr(top, i,
                        type(j)(self.obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
            else:
                setattr(top, i, j)
        return top

    def getConfig(self):
        """
        读取配置文件，存储类变量中，没有同步处理，多线程需要修改
        :return:
        """
        if self.config is None:
            self.config = self.obj_dic(yaml.load(open(self.filename, 'r', encoding="utf8")))
        return self.config
