import os
import numpy as np
import nibabel as nib
import pandas as pd
from tqdm import tqdm

def load_annot(file_path):
    """加载 FreeSurfer 的 .annot 文件，返回标签、颜色表和名称列表"""
    labels, ctab, names = nib.freesurfer.io.read_annot(file_path)
    # 将字节类型的名称转换为字符串
    names = [name.decode('utf-8') for name in names]
    return labels, ctab, names

def calculate_vertex_consistency(annot_A, annot_B):
    """
    计算两个图谱在每个顶点上的一致性：返回0（不一致）或1（一致）。
    annot_A 和 annot_B 分别是两个图谱的顶点标签数组。
    """
    assert annot_A.shape == annot_B.shape, "两个图谱的顶点数不一致"
    # 计算每个顶点的一致性：如果相同，返回1；否则返回0
    consistency = (annot_A == annot_B).astype(int)
    return consistency

def compute_vertex_wise_consistency(annot_dir, atlas_names):
    """计算每个顶点的空间一致性"""
    consistency_map = {}
    
    # 遍历每个图谱
    for atlas_name in tqdm(atlas_names, desc="Processing Atlases"):
        # 根据文件夹名称构建 annot 文件路径
        lh_annot_file = os.path.join(annot_dir, atlas_name, f'lh.{atlas_name}.annot')
        rh_annot_file = os.path.join(annot_dir, atlas_name, f'rh.{atlas_name}.annot')
        
        # 加载左半球和右半球的 annot 文件
        lh_labels, lh_ctab, lh_names = load_annot(lh_annot_file)
        rh_labels, rh_ctab, rh_names = load_annot(rh_annot_file)
        
        # 初始化一致性数组
        lh_consistency = np.zeros(lh_labels.shape)
        rh_consistency = np.zeros(rh_labels.shape)
        
        # 遍历所有其他图谱，计算每个顶点的一致性
        for other_atlas_name in tqdm(atlas_names, desc=f"Comparing with {atlas_name}", leave=False):
            if atlas_name == other_atlas_name:
                continue  # 跳过自己与自己比较

            # 生成其他图谱的 annot 文件路径
            lh_other_annot_file = os.path.join(annot_dir, other_atlas_name, f'lh.{other_atlas_name}.annot')
            rh_other_annot_file = os.path.join(annot_dir, other_atlas_name, f'rh.{other_atlas_name}.annot')
            
            # 加载其他图谱的 annot 文件
            lh_other_labels, _, _ = load_annot(lh_other_annot_file)
            rh_other_labels, _, _ = load_annot(rh_other_annot_file)
            
            # 计算一致性，累加每个图谱的结果
            lh_consistency += calculate_vertex_consistency(lh_labels, lh_other_labels)
            rh_consistency += calculate_vertex_consistency(rh_labels, rh_other_labels)
        
        # 计算每个顶点的平均一致性
        lh_consistency /= (len(atlas_names) - 1)
        rh_consistency /= (len(atlas_names) - 1)
        
        # 保存一致性结果到 consistency_map
        consistency_map[atlas_name] = {
            'lh': {'consistency': lh_consistency, 'labels': lh_labels, 'names': lh_names},
            'rh': {'consistency': rh_consistency, 'labels': rh_labels, 'names': rh_names}
        }
        
        # 将一致性结果保存为 CSV 文件
        save_csv(atlas_name, consistency_map[atlas_name])
    
    return consistency_map

def save_csv(atlas_name, atlas_data):
    """将每个图谱的顶点一致性结果保存到 CSV 文件"""
    # 创建保存目录
    save_dir = './皮层尺度一致化_csv'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 合并左半球和右半球的数据
    hemispheres = ['lh', 'rh']
    all_data = []
    
    for hemi in hemispheres:
        consistency = atlas_data[hemi]['consistency']
        labels = atlas_data[hemi]['labels']
        names = atlas_data[hemi]['names']
        
        # 创建 DataFrame
        df = pd.DataFrame({
            'Vertex Index': np.arange(len(consistency)),
            'Consistency': consistency,
            'Label': labels
        })
        
        # 映射标签到脑区名称
        df['Region Name'] = df['Label'].apply(lambda x: names[x] if x < len(names) else 'Unknown')
        
        # 创建新的顶点名称：RegionName_idx
        df['Vertex Name'] = df.apply(lambda row: f"{row['Region Name']}_{int(row['Vertex Index'])}", axis=1)
        
        # 选择并重排列
        df = df[['Vertex Name', 'Region Name', 'Consistency']]
        
        all_data.append(df)
    
    # 合并左右半球的数据
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # 按照脑区名称排序
    combined_df.sort_values(by=['Region Name', 'Vertex Name'], inplace=True)
    
    # 保存为 CSV 文件
    output_path = os.path.join(save_dir, f'{atlas_name}_vertex_consistency.csv')
    combined_df.to_csv(output_path, index=False)
    print(f"图谱 {atlas_name} 的一致性已保存到：{output_path}")

# 设置图谱目录和图谱名称
annot_dir = '/home/loving/MRI_Process/brainmap_annot/'
atlas_names = os.listdir(annot_dir)  # 自动获取所有子文件夹（即图谱的名字）

# 计算一致性并保存为 CSV
consistency_map = compute_vertex_wise_consistency(annot_dir, atlas_names)
