import math

# 地球椭球参数
a = 6378137  # 大地水准面半径，单位：米
f = 1 / 298.257223563  # 扁率

# 两点的地理坐标（十进制度数）
lat1, lon1 = 30.0, 114.0  # 点1的纬度和经度
lat2, lon2 = 31.0, 115.0  # 点2的纬度和经度

# 将地理坐标转换为弧度
lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

# 计算两点间中央经纬度
delta_lon = lon2_rad - lon1_rad

# 计算两点间距离的辅助函数
def H(lat1, lat2):
    return math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(delta_lon)

# 计算大地线长度
def calculate_distance(lat1, lon1, lat2, lon2, a, f):
    # 使用Vincenty公式计算两点间的距离，这是一个迭代过程
    # 这里使用简化的版本，实际应用中可能需要更复杂的迭代算法
    U1 = math.atan((1 - f) * math.tan(lat1_rad))
    U2 = math.atan((1 - f) * math.tan(lat2_rad))
    L = delta_lon
    lambda12 = L
    lambda_old = 0
    while abs(lambda12 - lambda_old) > 1e-10:
        sin_sigma = math.sqrt((math.cos(U2) * math.sin(lambda12)) ** 2 +
                             (math.cos(U1) * math.sin(U2) - math.sin(U1) * math.cos(U2) * math.cos(lambda12)) ** 2)
        cos_sigma = math.sin(U1) * math.sin(U2) + math.cos(U1) * math.cos(U2) * math.cos(lambda12)
        sigma = math.atan2(sin_sigma, cos_sigma)
        sin_alpha = math.cos(U1) * math.cos(U2) * math.sin(lambda12) / sin_sigma
        cos2alpha = 1 - sin_alpha ** 2
        cos_lambda_alpha = math.cos(lambda12) - 2 * math.sin(U1) * math.sin(U2) / cos2alpha
        C = f / 16 * cos2alpha * (4 + f * (4 - 3 * cos2alpha))
        lambda_old = lambda12
        lambda12 = L + (1 - C) * f * sin_alpha * (sigma + C * math.sin(sigma) * (math.cos(lambda12) + C * math.cos(sigma) * (-1 + 2 * math.cos(lambda12) ** 2)))

    distance = a * ((1 - f) * math.cos(U1) * math.cos(U2) * lambda12 + (f / 4 - f ** 2 / 6) * math.log((1 + sin_sigma) / (1 - sin_sigma)))
    return distance

# 计算正反方位角
def calculate_azimuth(lat1, lon1, lat2, lon2):
    # 计算正方位角
    alpha1 = math.atan2((math.sin(delta_lon) * math.cos(lat2_rad)),
                        (math.cos(lat1_rad) * math.tan(lat2_rad) - math.sin(lat1_rad) * math.cos(delta_lon)))
    # 计算反方位角
    alpha2 = math.atan2((-math.sin(delta_lon) * math.cos(lat1_rad)),
                        (-math.sin(lat2_rad) * math.tan(lat1_rad) + math.cos(lat2_rad) * math.cos(delta_lon)))
    return math.degrees(alpha1), math.degrees(alpha2)

# 计算大地线长度和正反方位角
distance = calculate_distance(lat1_rad, lon1_rad, lat2_rad, lon2_rad, a, f)
azimuth1, azimuth2 = calculate_azimuth(lat1_rad, lon1_rad, lat2_rad, lon2_rad)

# 输出结果
print("反算结果：")
print(f"大地线长度: {distance} 米")
print(f"正方位角: {azimuth1} 度")
print(f"反方位角: {azimuth2} 度")