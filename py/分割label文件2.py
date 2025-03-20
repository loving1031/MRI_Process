import nibabel.freesurfer.io as fs
import numpy as np
import os

# 总表面积和顶点数
total_surface_area = 93452  # 总表面积 mm²
total_vertices = 142909  # 总顶点数
surface_area_per_vertex = total_surface_area / total_vertices  # 每个顶点的表面积

# 目标每个子区域的表面积
target_area_per_region = 93.452  # 目标表面积 mm²
target_vertices_per_region = int(target_area_per_region / surface_area_per_vertex)  # 每个子区域的目标顶点数

# 标签文件列表
label_files = ['lh.middletemporal.label', 'lh.rostralanteriorcingulate.label', 'lh.superiorfrontal.label', 'lh.frontalpole.label', 'lh.insula.label', 'lh.parsopercularis.label', 'lh.bankssts.label', 'lh.medialorbitofrontal.label', 'lh.precuneus.label', 'lh.lateraloccipital.label', 'lh.isthmuscingulate.label', 'lh.superiortemporal.label', 'lh.lateralorbitofrontal.label', 'lh.inferiorparietal.label', 'lh.transversetemporal.label', 'lh.parsorbitalis.label', 'lh.caudalmiddlefrontal.label', 'lh.supramarginal.label', 'lh.superiorparietal.label', 'lh.rostralmiddlefrontal.label', 'lh.entorhinal.label', 'lh.parahippocampal.label', 'lh.parstriangularis.label', 'lh.posteriorcingulate.label', 'lh.precentral.label', 'lh.paracentral.label', 'lh.lingual.label', 'lh.caudalanteriorcingulate.label', 'lh.temporalpole.label', 'lh.pericalcarine.label', 'lh.postcentral.label', 'lh.fusiform.label', 'lh.cuneus.label', 'lh.inferiortemporal.label']

# 输出目录
output_dir = 'label_seg2'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 表面数据
subject_id = "subject2"  # 替换成你的subject ID
surf_file = f"/home/loving/freesurfer/subjects/{subject_id}/surf/lh.white"

# 读取白质表面顶点坐标
surf_data = fs.read_geometry(surf_file)
vertices, _ = surf_data

# 递归分割函数
def recursive_split(label_vertices, region_id, target_vertices, base_file_name):
    num_vertices = len(label_vertices)

    # 如果当前区域小于目标顶点数，则直接保存
    if num_vertices <= target_vertices:
        save_label_file(label_vertices, f"{base_file_name}_region_{region_id}.label")
        return region_id + 1

    # 随机拆分区域
    midpoint = num_vertices // 2
    region_id = recursive_split(label_vertices[:midpoint], region_id, target_vertices, base_file_name)
    region_id = recursive_split(label_vertices[midpoint:], region_id, target_vertices, base_file_name)
    return region_id

# 保存文件函数
def save_label_file(region_vertices, filename):
    # 获取区域的顶点数
    num_vertices_in_region = len(region_vertices)
    filepath = os.path.join(output_dir, filename)
    
    # 写入文件
    with open(filepath, 'w') as f:
        f.write(f"#!ascii label {filepath} , from subject vox2ras=\n")
        f.write(f"{num_vertices_in_region}\n")
        for vertex_idx in region_vertices:
            x, y, z = vertices[vertex_idx]
            f.write(f"{vertex_idx} {x:.6f} {y:.6f} {z:.6f} 0.0000000000\n")
    
    print(f"Created sub-region label file: {filename}")

# 读取和分割每个标签文件
for label_file in label_files:
    # 读取标签文件
    label_vertices = fs.read_label(label_file)

    # 递归分割区域
    base_file_name = os.path.basename(label_file)
    recursive_split(label_vertices, 0, target_vertices_per_region, base_file_name)

    print(f"Finished processing label file: {label_file}")
