"""
"""

from abc import ABCMeta, abstractmethod


class BaseCommand(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def add(self, parser, command_parser):
        pass

    @abstractmethod
    def process(self, args):
        pass
