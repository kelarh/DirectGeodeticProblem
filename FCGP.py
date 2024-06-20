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

# 平均半径
R = (a + b) / 2

# 计算法线曲率半径N和子午圈曲率半径M
def compute_N(B):
    return a / math.sqrt(1 - e2 * math.sin(B)**2)

def compute_M(B):
    return a * (1 - e2) / (1 - e2 * math.sin(B)**2)**1.5

# 计算大地方位角变化量
def delta_A(B, A):
    N = compute_N(B)
    return (math.tan(B) * math.sin(A)) / N

# 计算终点的纬度和经度
def compute_lat_lon(lat1, lon1, s, A1):
    Bm = lat1
    Lm = lon1
    
    epsilon = 1e-10  # 收敛条件

    for _ in range(100):
        N = compute_N(Bm)
        M = compute_M(Bm)
        
        delta_B = (s * math.cos(A1)) / M
        delta_L = (s * math.sin(A1)) / (N * math.cos(Bm))
        delta_A1 = delta_A(Bm, A1)
        
        Bm_new = Bm + delta_B / 2
        Lm_new = Lm + delta_L / 2
        A1_new = A1 + delta_A1 / 2
        
        if (abs(Bm_new - Bm) < epsilon and abs(Lm_new - Lm) < epsilon and abs(A1_new - A1) < epsilon):
            break
        
        Bm = Bm_new
        Lm = Lm_new
        A1 = A1_new

    return Bm, Lm, A1

lat2, lon2, A2 = compute_lat_lon(lat1, lon1, s, A1)

# 计算终点的反方位角
A2 = math.degrees(A2) + 180
if A2 >= 360:
    A2 -= 360

# 转换回度
lat2 = math.degrees(lat2)
lon2 = math.degrees(lon2)

# 输出最终结果
print("计算结果：")
print(f"终点纬度 B2 = {lat2} 度")
print(f"终点经度 L2 = {lon2} 度")
print(f"终点反方位角 A2 = {A2} 度")
