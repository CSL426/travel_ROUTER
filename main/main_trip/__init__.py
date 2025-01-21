"""
行程規劃子系統

此子系統提供：
1. 行程規劃控制器
2. 便捷的規劃函式

可以透過:
- TripController: 完整功能的控制器類別
- run_trip_planner: 包裝後的便捷函式
來使用系統
"""

from .controllers.controller import TripController, init_config
from .trip_service import run_trip_planner

__all__ = [
    'TripController',  # 導出控制器類別
    'init_config',  # 導出初始化設定函式
    'run_trip_planner'  # 導出便捷函式
]
