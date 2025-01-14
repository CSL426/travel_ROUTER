"""
初始化 main 套件
提供主要的控制器和程式進入點
"""
# main/__init__.py
from .main_trip.controller import TripController

__all__ = ['TripController']
