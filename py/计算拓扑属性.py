import pandas as pd
import numpy as np
import os

# 定义文件对应关系，仅保留 36840 分辨率
FILE_MAPPINGS = {
    '36840': {
        'region_file': 'A_filename_36840.txt',
        'matrix_file': 'connectome_18238_18602.csv'
    }
}

def extract_region_matrix_by_chunks(region_prefix, resolution, chunksize=1000):
    """
    使用逐块读取方法提取特定分辨率下的脑区矩阵
    :param region_prefix: 脑区前缀
    :param resolution: 分辨率标识（如'36840'）
    :param chunksize: 每次读取的块大小（行数）
    """
    if resolution not in FILE_MAPPINGS:
        print(f"不支持的分辨率: {resolution}")
        return
    
    # 获取对应的文件路径
    files = FILE_MAPPINGS[resolution]
    region_file = files['region_file']
    matrix_file = files['matrix_file']
    
    # 读取脑区名称文件
    with open(region_file, 'r') as f:
        region_names = [line.strip() for line in f.readlines()]
    
    # 找到所有匹配前缀的索引
    matched_indices = [i for i, name in enumerate(region_names) if name.startswith(region_prefix)]
    
    if not matched_indices:
        print(f"没有找到与前缀 {region_prefix} 匹配的脑区")
        return

    # 创建输出目录
    output_dir = f'roi_csv_{resolution}'
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建空 DataFrame 用于拼接子矩阵
    sub_matrix = pd.DataFrame(index=matched_indices, columns=matched_indices)
    
    # 逐块读取连接矩阵并提取子矩阵
    matrix_path = os.path.join('/home/loving/NEW_Progress/connectome', matrix_file)
    print(f"开始逐块读取 {matrix_path}...")
    for start_row in range(0, len(region_names), chunksize):
        end_row = min(start_row + chunksize, len(region_names))
        print(f"正在处理行 {start_row}-{end_row}...")
        
        # 读取当前块（只加载所需列）
        chunk = pd.read_csv(matrix_path, skiprows=start_row, nrows=(end_row - start_row), header=None, usecols=matched_indices)
        
        # 将子矩阵拼接到结果中
        for i, global_row in enumerate(range(start_row, end_row)):
            if global_row in matched_indices:
                local_row = matched_indices.index(global_row)  # 对应的局部索引
                sub_matrix.iloc[local_row, :] = chunk.iloc[i, :].values
    
    # 提取对应的脑区名称
    matched_names = [region_names[i] for i in matched_indices]
    
    # 设置行列名
    sub_matrix.index = matched_names
    sub_matrix.columns = matched_names
    
    # 保存到新文件
    output_file = os.path.join(output_dir, f"{region_prefix.replace('.', '')}_{resolution}.csv")
    sub_matrix.to_csv(output_file)
    
    # 输出详细信息
    print(f"\n=== {region_prefix} ({resolution}) 提取结果详情 ===")
    print(f"已保存到文件: {output_file}")
    print(f"\n提取的脑区及其索引:")
    for idx, name in zip(matched_indices, matched_names):
        print(f"索引 {idx}: {name}")
    print(f"\n索引范围: {min(matched_indices)} - {max(matched_indices)}")
    print(f"矩阵大小: {sub_matrix.shape}")
    print(f"\n提取的子矩阵在原矩阵中的位置:")
    print(f"行/列: {matched_indices}")
    print("=" * 50)

if __name__ == "__main__":
    # 定义要提取的脑区列表
    regions = [
        'lh.insula',
        'lh.superiorfrontal',
        'lh.caudalmiddlefrontal',
        'lh.precentral',
        'rh.insula',
        'rh.superiorfrontal',
        'lh.inferiorparietal',
        'lh.posteriorcingulate'
    ]
    
    # 固定处理 36840 分辨率
    resolution = '36840'
    
    # 逐块提取每个脑区的矩阵
    for region in regions:
        extract_region_matrix_by_chunks(region, resolution)
