import math

# 椭球参数（WGS-84）
a = 6378137.0  # 长半轴，单位：米
f = 1 / 298.257223563  # 扁率
b = a * (1 - f)  # 短半轴，单位：米
e2 = (a**2 - b**2) / a**2  # 第一偏心率平方

# 初始点的地理坐标（纬度和经度，单位：度）
lat1 = 30.0  # 起点纬度
lon1 = 114.0  # 起点经度

# 转换为弧度
lat1 = math.radians(lat1)
lon1 = math.radians(lon1)

# 已知大地线长和方位角（单位：米和度）
s = 150000  # 大地线长，单位：米
A1 = math.radians(45.0)  # 初始方位角，单位：弧度

# 计算法线曲率半径N
def compute_N(B):
    return a / math.sqrt(1 - e2 * math.sin(B)**2)

# 计算子午圈曲率半径M
def compute_M(B):
    return a * (1 - e2) / (1 - e2 * math.sin(B)**2)**1.5

# 计算终点的纬度和经度
def direct_geodetic(lat1, lon1, s, A1):
    alpha = A1  # 初始方位角
    sigma = s / b  # 归化的大地线长

    # 高斯平均引数
    beta1 = math.atan((1 - f) * math.tan(lat1))
    U1 = math.atan((1 - f) * math.tan(lat1))
    sinU1 = math.sin(U1)
    cosU1 = math.cos(U1)
    
    # 初始计算
    sigma1 = math.atan2(math.tan(U1), math.cos(A1))
    sin_alpha = cosU1 * math.sin(A1)
    cos2_alpha = 1 - sin_alpha**2
    u2 = cos2_alpha * (a**2 - b**2) / b**2
    A = 1 + (u2 / 16384) * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = (u2 / 1024) * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))

    sigma_p = sigma
    sigma = s / (b * A)
    sin_sigma = 0
    cos_sigma = 0
    cos2_sigma_m = 0
    delta_sigma = 0

    for _ in range(1000):
        cos2_sigma_m = math.cos(2 * sigma1 + sigma)
        sin_sigma = math.sin(sigma)
        cos_sigma = math.cos(sigma)
        delta_sigma = B * sin_sigma * (cos2_sigma_m + (B / 4) * (cos_sigma * (-1 + 2 * cos2_sigma_m**2) - (B / 6) * cos2_sigma_m * (-3 + 4 * sin_sigma**2) * (-3 + 4 * cos2_sigma_m**2)))
        sigma_p = sigma
        sigma = s / (b * A) + delta_sigma
        if abs(sigma - sigma_p) < 1e-12:
            break

    tmp = sinU1 * sin_sigma - cosU1 * cos_sigma * math.cos(A1)
    lat2 = math.atan2(sinU1 * cos_sigma + cosU1 * sin_sigma * math.cos(A1), (1 - f) * math.sqrt(sin_alpha**2 + tmp**2))
    lamb = math.atan2(sin_sigma * math.sin(A1), cosU1 * cos_sigma - sinU1 * sin_sigma * math.cos(A1))
    C = (f / 16) * cos2_alpha * (4 + f * (4 - 3 * cos2_alpha))
    L = lamb - (1 - C) * f * sin_alpha * (sigma + C * sin_sigma * (cos2_sigma_m + C * cos_sigma * (-1 + 2 * cos2_sigma_m**2)))
    
    lon2 = lon1 + L

    # 转换为度
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    # 确保经度在-180度到180度之间
    if lon2 > 180:
        lon2 -= 360
    elif lon2 < -180:
        lon2 += 360

    # 终点方位角
    A2 = math.atan2(sin_alpha, -tmp)
    A2 = math.degrees(A2) + 180
    if A2 >= 360:
        A2 -= 360

    return lat2, lon2, A2

# 计算终点的纬度、经度和方位角
lat2, lon2, A2 = direct_geodetic(lat1, lon1, s, A1)

# 输出最终结果
print("计算结果：")
print(f"终点纬度 B2 = {lat2} 度")
print(f"终点经度 L2 = {lon2} 度")
print(f"终点反方位角 A2 = {A2} 度")
