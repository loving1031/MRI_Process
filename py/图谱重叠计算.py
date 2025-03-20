import nibabel as nib
import numpy as np
import os
import csv
from tqdm import tqdm  # 导入进度条库

# 1. 加载图谱文件
atlas_dir = '/home/loving/MRI_Process/brainmap_nii'  # 图谱所在文件夹
atlas_files = [f for f in os.listdir(atlas_dir) if f.endswith('.nii.gz')]

# 加载所有图谱
atlases = {}
for atlas_file in atlas_files:
    atlas_path = os.path.join(atlas_dir, atlas_file)
    atlas_img = nib.load(atlas_path)
    atlases[atlas_file] = atlas_img.get_fdata()

# 2. 计算每对图谱之间的共享区域表面积
def compute_shared_surface_area(atlas_A, atlas_B):
    """
    计算两个图谱中每个区域的共享表面积
    筛选标号大于等于1000的区域，输出到CSV文件
    """
    # 只考虑标号大于等于1000的脑区
    unique_A = np.unique(atlas_A)
    unique_B = np.unique(atlas_B)
    
    # 筛掉标号小于1000的脑区
    unique_A = unique_A[unique_A >= 1000]
    unique_B = unique_B[unique_B >= 1000]
    
    # 输出筛选后的 unique_A 和 unique_B 到 CSV
    with open('/home/loving/MRI_Process/brainmap_nii/unique_brain_regions.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Region_A", "Region_B"])
        for region_A in unique_A:
            for region_B in unique_B:
                writer.writerow([region_A, region_B])
    
    shared_area = {}
    
    for region_A in unique_A:
        for region_B in unique_B:
            overlap = np.sum((atlas_A == region_A) & (atlas_B == region_B))
            if overlap > 0:
                if region_A not in shared_area:
                    shared_area[region_A] = {}
                shared_area[region_A][region_B] = overlap
                
    return shared_area, unique_A, unique_B

# 3. 计算区域一致性
def compute_region_consistency(shared_area, atlas_A, atlas_B):
    """
    根据共享表面积计算区域一致性
    """
    region_consistency = {}
    
    for region_A in shared_area:
        total_area_A = np.sum(atlas_A == region_A)
        max_consistency = 0
        for region_B in shared_area[region_A]:
            shared = shared_area[region_A][region_B]
            consistency = shared / total_area_A
            max_consistency = max(max_consistency, consistency)
        region_consistency[region_A] = max_consistency
        
    return region_consistency

# 4. 计算图谱对之间的整体一致性
def compute_global_consistency(region_consistency):
    """
    计算每对图谱的一致性评分
    """
    return np.mean(list(region_consistency.values()))

# 5. 计算所有图谱对之间的一致性并保存一致性矩阵
n = len(atlases)
consistency_matrix = np.zeros((n, n))

# 用于存储所有共享区域表面积和区域一致性0
shared_area_data = []
region_consistency_data = []

# 使用 tqdm 为外层循环添加进度条
for i, (file_A, atlas_A) in enumerate(tqdm(atlases.items(), desc="Processing atlas pairs", unit="pair")):
    for j, (file_B, atlas_B) in enumerate(atlases.items()):
        # 计算共享区域表面积
        shared_area, unique_A, unique_B = compute_shared_surface_area(atlas_A, atlas_B)
        # 计算区域一致性
        region_consistency = compute_region_consistency(shared_area, atlas_A, atlas_B)
        
        # 将共享区域表面积存储到 CSV
        for region_A in shared_area:
            for region_B in shared_area[region_A]:
                shared_area_data.append([file_A, file_B, region_A, region_B, shared_area[region_A][region_B]])
        
        # 将区域一致性存储到 CSV
        for region_A in region_consistency:
            region_consistency_data.append([file_A, file_B, region_A, region_consistency[region_A]])
        
        # 计算全局一致性
        global_consistency = compute_global_consistency(region_consistency)
        # 将一致性值填充到矩阵中
        consistency_matrix[i, j] = global_consistency

# 6. 输出共享区域表面积到 CSV
with open('/home/loving/MRI_Process/brainmap_nii/shared_area.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Atlas_A", "Atlas_B", "Region_A", "Region_B", "Shared_Area"])
    for row in shared_area_data:
        writer.writerow(row)

# 7. 输出区域一致性到 CSV
with open('/home/loving/MRI_Process/brainmap_nii/region_consistency.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Atlas_A", "Atlas_B", "Region_A", "Consistency"])
    for row in region_consistency_data:
        writer.writerow(row)


# 8.使用 pandas 保存为更易读的 CSV 格式
import pandas as pd
consistency_df = pd.DataFrame(consistency_matrix, index=atlas_files, columns=atlas_files)
consistency_df.to_csv('/home/loving/MRI_Process/brainmap_nii/atlas_consistency_matrix.csv')

# 9. 可视化一致性矩阵
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取 CSV 文件到 DataFrame，假设文件中已经包含行列名
df = pd.read_csv('/home/loving/MRI_Process/brainmap_nii/atlas_consistency_matrix.csv', index_col=0)

# 设置 Seaborn 样式
sns.set(style="whitegrid")

# 绘制热图
plt.figure(figsize=(12, 10))
sns.heatmap(df, cmap='nipy_spectral', fmt=".2f")

# 设置标题和轴标签
plt.title('Atlas Consistency Matrix', fontsize=14)
plt.xlabel('Atlas', fontsize=12)
plt.ylabel('Atlas', fontsize=12)

# 调整刻度标签角度，使其更易读
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)

# 显示热图
plt.show()



