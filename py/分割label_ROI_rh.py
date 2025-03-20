
import nibabel.freesurfer.io as fs
import numpy as np
import torch
from sklearn.cluster import KMeans
import os

# 初始设定
total_surface_area = 11924  # 总表面积 mm²
total_vertices = 14908  # 总顶点数
surface_area_per_vertex = total_surface_area / total_vertices  # 每个顶点的表面积
target_area_per_region = 596.2  # 目标每个子区域表面积
target_vertices_per_region = target_area_per_region / surface_area_per_vertex


# 路径设定
label_files_path = '/home/loving/NEW_Progress/ROI_analyze/right_parietal_frontal/rh_seg10'  # 设置label文件路径
output_dir = '/home/loving/NEW_Progress/ROI_analyze/right_parietal_frontal/rh_seg10_seg20'  # 输出路径

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取表面数据
subject_id = "subject2"
surf_file = f"/home/loving/freesurfer/subjects/{subject_id}/surf/rh.pial"  # rh.pial

# 读取pial表面顶点坐标
vertices, _ = fs.read_geometry(surf_file)

# 遍历label文件并进行分割
for label_file in os.listdir(label_files_path):
    if label_file.endswith('.label'):
        # 读取每个label文件
        label_vertices = fs.read_label(os.path.join(label_files_path, label_file))
        label_coords = vertices[label_vertices]

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
            new_label_file = os.path.join(output_dir, f"{os.path.basename(label_file)}_region_{region_id}.label")
            
            with open(new_label_file, 'w') as f:
                f.write(f"#!ascii label {new_label_file}\n{len(region_vertices)}\n")
                for vertex_idx in region_vertices:
                    x, y, z = vertices[vertex_idx]
                    f.write(f"{vertex_idx} {x:.6f} {y:.6f} {z:.6f} 0.000000\n")
                    
            print(f"Created sub-region label file: {new_label_file}")
