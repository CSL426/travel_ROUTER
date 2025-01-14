"""
初始化 main 套件
提供主要的控制器和程式進入點
"""
# main/__init__.py
from .main_trip.controllers.controller import TripController
from .main_trip.trip_service import run_trip_planner

__all__ = [
    'TripController',
    'run_trip_planner',
]
