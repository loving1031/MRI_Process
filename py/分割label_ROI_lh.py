import nibabel.freesurfer.io as fs
import numpy as np
from sklearn.cluster import KMeans
import os

# 总的表面积和顶点数（假设数据）
total_surface_area = 10273  # 总表面积 mm²
total_vertices = 14908  # 总顶点数
surface_area_per_vertex = total_surface_area / total_vertices  # 每个顶点的表面积

# 目标每个子区域的表面积
target_area_per_region = 513.65  # 目标表面积 mm²
target_vertices_per_region = target_area_per_region / surface_area_per_vertex  # 每个子区域所需的顶点数

# 指定标签文件所在的目录
label_dir = '/home/loving/NEW_Progress/ROI_analyze/left_parietal_frontal/lh_seg10'  # 替换为你的标签文件所在文件夹
output_dir = '/home/loving/NEW_Progress/ROI_analyze/left_parietal_frontal/lh_seg10_seg20'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取表面数据
subject_id = "subject2"  # 替换成你的subject ID
surf_file = f"/home/loving/freesurfer/subjects/{subject_id}/surf/lh.white"  # 或者使用 lh.pial

# 读取白质表面顶点坐标
surf_data = fs.read_geometry(surf_file)
vertices, _ = surf_data

# 自动获取文件夹中的所有 .label 文件
label_files = [
    os.path.join(label_dir, file)
    for file in os.listdir(label_dir) if file.endswith('.label')
]

# 读取每个标签文件并分割
for label_file in label_files:
    # 读取标签文件
    label_vertices = fs.read_label(label_file)

    # 过滤出对应的顶点坐标
    label_coords = vertices[label_vertices]

    # 计算标签的总表面积
    label_area = len(label_coords) * surface_area_per_vertex

    # 计算需要分割成多少个子区域
    num_regions = int(label_area // target_area_per_region)
    if num_regions < 1:
        num_regions = 1  # 确保至少有一个区域
    print(f"Label: {label_file} - Total Area: {label_area:.2f} mm², Num Regions: {num_regions}")

    # 使用 KMeans 聚类将顶点分割成目标数量的子区域
    kmeans = KMeans(n_clusters=num_regions, random_state=0)
    kmeans.fit(label_coords)  # label_coords 是标签区域内顶点的坐标数据

    # 获取每个顶点所属的区域标签
    labels = kmeans.labels_

    # 将每个区域的顶点分配到对应的区域中
    regions = {}
    for idx, region_label in enumerate(labels):
        if region_label not in regions:
            regions[region_label] = []
        regions[region_label].append(label_vertices[idx])

    # 生成新的子标签文件并保存到指定的目录
    for region_id, region_vertices in regions.items():
        # 生成每个子区域的label文件
        new_label_file = os.path.join(output_dir, f"{os.path.basename(label_file)}_region_{region_id}.label")

        # 写入label文件
        num_vertices_in_region = len(region_vertices)
        with open(new_label_file, 'w') as f:
            # 写入顶点数
            f.write(f"{num_vertices_in_region}\n")
            # 写入每个顶点的坐标和额外的0值
            for vertex_idx in region_vertices:
                x, y, z = vertices[vertex_idx]
                f.write(f"{vertex_idx} {x:.6f} {y:.6f} {z:.6f} 0.000000\n")

        print(f"Created sub-region label file: {new_label_file}")

    print(f"Finished processing label file: {label_file}")
 