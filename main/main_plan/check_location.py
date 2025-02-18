def is_in_new_taipei(lat: float, lon: float) -> bool:
    """
    判斷給定的經緯度是否在新北市範圍內（不包含基隆）
    
    Args:
        lat: 緯度
        lon: 經度
        
    Returns:
        bool: True表示在新北市內，False表示不在
    """
    
    # 新北市各區的大致邊界點（順時針排列）
    # 這些點是新北市的外圍輪廓，形成一個多邊形
    new_taipei_bounds = [
        (25.2977, 121.4151),  # 淡水區
        (25.2984, 121.5410),  # 金山區
        (25.2381, 121.6457),  # 萬里區
        (25.1549, 121.7457),  # 瑞芳區
        (25.0237, 121.8235),  # 貢寮區
        (24.9126, 121.8235),  # 雙溪區
        (24.8666, 121.7673),  # 坪林區
        (24.8157, 121.5964),  # 烏來區
        (24.8940, 121.4726),  # 新店區
        (24.9952, 121.3696),  # 樹林區
        (25.0222, 121.2833),  # 林口區
        (25.1539, 121.3215),  # 八里區
        (25.1831, 121.3696),  # 五股區
    ]
    
    def is_point_in_polygon(point: tuple, polygon: list) -> bool:
        """
        射線法（Ray Casting Algorithm）判斷點是否在多邊形內
        
        Args:
            point: (lat, lon) 待判斷的點
            polygon: 多邊形的頂點列表
            
        Returns:
            bool: True表示在多邊形內，False表示在多邊形外
        """
        x, y = point
        inside = False
        
        j = len(polygon) - 1
        for i in range(len(polygon)):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            
            if ((yi > y) != (yj > y)) and \
               (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
            
        return inside
    
    # 基隆市的大致範圍（作為排除區域）
    keelung_bounds = [
        (25.1549, 121.7457),  # 西北角
        (25.1549, 121.7873),  # 東北角
        (25.1165, 121.7873),  # 東南角
        (25.1165, 121.7457),  # 西南角
    ]
    
    # 判斷是否在新北市內且不在基隆市內
    is_in_new_taipei_area = is_point_in_polygon((lat, lon), new_taipei_bounds)
    is_in_keelung_area = is_point_in_polygon((lat, lon), keelung_bounds)
    
    return is_in_new_taipei_area and not is_in_keelung_area

# 測試用例
if __name__ == "__main__":
    # 測試一些已知的地點
    test_locations = [
        (25.0856, 121.4739, "板橋市政府"),    # 應該在新北市內
        (25.1276, 121.7391, "基隆廟口"),      # 應該不在（基隆）
        (25.0339, 121.5644, "台北101"),       # 應該不在（台北市）
        (25.1840, 121.4458, "淡水老街"),      # 應該在新北市內
        (25.0121, 121.4651, "新店碧潭"),      # 應該在新北市內
        (24.95764031289562, 121.22525683541723, "緯育")
    ]
    
    for lat, lon, name in test_locations:
        result = is_in_new_taipei(lat, lon)
        print(f"{name} ({lat}, {lon}) 是否在新北市內: {result}")