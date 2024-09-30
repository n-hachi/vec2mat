import numpy as np

def euler_to_rotation_matrix(roll, pitch, yaw):
    # 回転行列を計算
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])
    
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
    
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])
    
    # 回転行列を合成
    R = R_z @ R_y @ R_x  # ZYX順で回転
    
    return R

def create_transformation_matrix(x, y, z, roll, pitch, yaw):
    R = euler_to_rotation_matrix(roll, pitch, yaw)
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = [x, y, z]
    
    return T

def rotation_matrix_to_euler_angles(R):
    # Rの特異性を考慮して、オイラー角を計算
    sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
    
    if sy > 1e-6:  # 限界を設定
        x = np.arctan2(R[2, 1], R[2, 2])  # roll
        y = np.arctan2(-R[2, 0], sy)       # pitch
        z = np.arctan2(R[1, 0], R[0, 0])   # yaw
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])  # roll
        y = np.arctan2(-R[2, 0], sy)       # pitch
        z = 0  # yawは定義できない

    return x, y, z

def extract_position_and_euler(T):
    # 位置を抽出
    x = T[0, 3]
    y = T[1, 3]
    z = T[2, 3]
    
    # 回転行列を抽出
    R = T[:3, :3]
    
    # オイラー角を計算
    roll, pitch, yaw = rotation_matrix_to_euler_angles(R)
    
    return x, y, z, roll, pitch, yaw


def main():
    input_str = input("x y z roll(radian) pitch(radian) yaw(radian): ")
    x, y, z, roll, pitch, yaw = [float(v.strip()) for v in input_str.split()]
    transformation_matrix = create_transformation_matrix(x, y, z, roll, pitch, yaw)
    print(transformation_matrix)
    print(extract_position_and_euler(transformation_matrix))
    

if __name__ == "__main__":
    main()
