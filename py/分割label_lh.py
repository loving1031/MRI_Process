import nibabel.freesurfer.io as fs
import numpy as np
from sklearn.cluster import KMeans
import os

# 初始设定
total_surface_area = 93452  # 总表面积 mm²
total_vertices = 142909  # 总顶点数
surface_area_per_vertex = total_surface_area / total_vertices  # 每个顶点的表面积
target_area_per_region = 4  # 目标每个子区域表面积
target_vertices_per_region = target_area_per_region / surface_area_per_vertex

# 路径设定
label_files_path = '/home/loving/NEW_Progress/lh_label_seg_86_195_381_762_1519_2963_6337'  # 替换为你的标签文件所在文件夹
output_dir = '/home/loving/NEW_Progress/lh_label_seg_86_195_381_762_1519_2963_6337_15000'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取表面数据
subject_id = "subject2"
surf_file = f"/home/loving/freesurfer/subjects/{subject_id}/surf/lh.white"

# 读取pial表面顶点坐标
vertices, _ = fs.read_geometry(surf_file)

# 检查 vertices 的形状
if vertices.ndim != 2 or vertices.shape[1] != 3:
    raise ValueError(f"读取的表面顶点数据形状不正确: {vertices.shape}。期望是 (n_points, 3)。")

# 遍历label文件并进行分割
for label_file in os.listdir(label_files_path):
    if label_file.endswith('.label'):
        label_path = os.path.join(label_files_path, label_file)

        try:
            # 读取每个label文件
            label_vertices = fs.read_label(label_path)

            # 检查 label_vertices 是否为空
            if len(label_vertices) == 0:
                print(f"标签文件 {label_file} 中没有顶点，跳过...")
                continue

            # 提取顶点坐标
            label_coords = vertices[label_vertices]

            # 如果只有一个顶点，确保 label_coords 是二维的
            if label_coords.ndim == 1:
                label_coords = label_coords[np.newaxis, :]

            # 检查 label_coords 的形状
            if label_coords.ndim != 2 or label_coords.shape[1] != 3:
                print(f"标签文件 {label_file} 的坐标形状错误: {label_coords.shape}，跳过...")
                continue

            # 获取表面积并计算需要的分割区域数
            label_area = len(label_coords) * surface_area_per_vertex
            num_regions = max(1, int(label_area // target_area_per_region))

            # 使用 KMeans 进行聚类分割
            kmeans = KMeans(n_clusters=num_regions, random_state=0) 
            labels = kmeans.fit_predict(label_coords)

            # 创建子label文件
            for region_id in range(num_regions):
                region_vertices = label_vertices[labels == region_id]
                base_name = os.path.splitext(label_file)[0]  # 去掉文件后缀
                new_label_file = os.path.join(output_dir, f"{base_name}_region_{region_id}.label")

                with open(new_label_file, 'w') as f:
                    f.write(f"#!ascii label {new_label_file}\n{len(region_vertices)}\n")
                    for vertex_idx in region_vertices:
                        x, y, z = vertices[vertex_idx]
                        f.write(f"{vertex_idx} {x:.6f} {y:.6f} {z:.6f} 0.000000\n")

                print(f"Created sub-region label file: {new_label_file}")

        except Exception as e:
            print(f"处理文件 {label_file} 时出错: {e}，跳过...")
