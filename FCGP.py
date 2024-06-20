import math

# 椭球参数（WGS-84）
a = 6378137.0  # 长半轴，单位：米
f = 1 / 298.257223563  # 偏心率

# 初始点的地理坐标（纬度和经度，单位：度）
lat1 = 30.0  # 起点纬度
lon1 = 114.0  # 起点经度

# 转换为弧度
lat1 = math.radians(lat1)
lon1 = math.radians(lon1)

# 已知大地线长和方位角（单位：米和度）
s = 150000  # 大地线长，单位：米
A1 = math.radians(45.0)  # 初始方位角，单位：弧度

# 将弧度转换为度
def rad_to_deg(rad):
    return math.degrees(rad)

# 计算两点间的中央经纬度
def central_angle(lat1, lon1, A1, s):
    # 使用简化公式，实际应用中应使用更复杂的大地测量公式
    B = math.tan(lat1) * math.tan(A1)
    theta = s / a  # 假设地球为正球体
    return theta

# 辅助函数：计算大地线终点坐标
def compute_end_point(lat1, lon1, A1, theta):
    # 使用简化公式，实际应用中应使用更复杂的大地测量公式
    delta_lon = theta / math.cos(lat1)
    lat2 = math.asin(math.sin(lat1) * math.cos(theta) + math.cos(lat1) * math.sin(theta) * math.cos(A1))
    lon2 = lon1 + math.atan2(math.sin(A1) * math.sin(theta) * math.cos(lat1), math.cos(theta) - math.sin(lat1) * math.sin(lat2))
    return lat2, lon2

# 计算中央角
theta = central_angle(lat1, lon1, A1, s)

# 计算终点坐标
lat2, lon2 = compute_end_point(lat1, lon1, A1, theta)

# 计算反方位角
A2 = math.atan2(math.sin(A1), -math.tan(lat1))  # 简化计算，实际应用中需更正

# 将结果转换为度
lat2_deg = rad_to_deg(lat2)
lon2_deg = rad_to_deg(lon2)
A2_deg = rad_to_deg(A2)

# 输出最终结果
print("正算结果：")
print(f"终点纬度: {lat2_deg} 度")
print(f"终点经度: {lon2_deg} 度")
print(f"终点反方位角: {A2_deg} 度")