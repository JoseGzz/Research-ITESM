# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class DataReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self, source_filename):
        pass
