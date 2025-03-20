import pandas as pd
import numpy as np
import os

# 定义文件对应关系
FILE_MAPPINGS = {
    '173': {
        'region_file': 'A_filename_173.txt',
        'matrix_file': 'connectome_86_87.csv'
    },
    '390': {
        'region_file': 'A_filename_390.txt',
        'matrix_file': 'connectome_195_195.csv'
    },
    '756': {
        'region_file': 'A_filename_756.txt',
        'matrix_file': 'connectome_381_375.csv'
    },
    '1518': {
        'region_file': 'A_filename_1518.txt',
        'matrix_file': 'connectome_762_756.csv'
    },
    '3030': {
        'region_file': 'A_filename_3030.txt',
        'matrix_file': 'connectome_1519_1511.csv'
    },
    '5976': {
        'region_file': 'A_filename_5976.txt',
        'matrix_file': 'connectome_2963_3013.csv'
    },
    '12853': {
        'region_file': 'A_filename_12853.txt',
        'matrix_file': 'connectome_6337_6516.csv'
    },
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
    output_dir = f'roi_csv_{resolution}/nohub'
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建空 DataFrame 用于拼接子矩阵
    sub_matrix = pd.DataFrame(index=matched_indices, columns=matched_indices)
    
    # 逐块读取连接矩阵并提取子矩阵
    matrix_path = os.path.join('/home/loving/NEW_Progress/connectome', matrix_file)
    print(f"开始逐块读取 {matrix_path}...")
    for start_row in range(0, len(region_names), chunksize):
        end_row = min(start_row + chunksize, len(region_names))
        chunk = pd.read_csv(matrix_path, skiprows=start_row, nrows=(end_row - start_row), header=None, usecols=matched_indices)
        
        for i, global_row in enumerate(range(start_row, end_row)):
            if global_row in matched_indices:
                local_row = matched_indices.index(global_row)
                sub_matrix.iloc[local_row, :] = chunk.iloc[i, :].values

    matched_names = [region_names[i] for i in matched_indices]
    sub_matrix.index = matched_names
    sub_matrix.columns = matched_names

    output_file = os.path.join(output_dir, f"{region_prefix.replace('.', '')}_{resolution}.csv")
    sub_matrix.to_csv(output_file)
    print(f"已保存到文件: {output_file}")

def extract_region_matrix(region_prefix, resolution):
    """
    提取特定分辨率下的脑区矩阵（不使用逐块读取）
    """
    files = FILE_MAPPINGS[resolution]
    region_file = files['region_file']
    matrix_file = files['matrix_file']
    
    with open(region_file, 'r') as f:
        region_names = [line.strip() for line in f.readlines()]
    
    matched_indices = [i for i, name in enumerate(region_names) if name.startswith(region_prefix)]
    if not matched_indices:
        print(f"没有找到与前缀 {region_prefix} 匹配的脑区")
        return
    
    matrix_path = os.path.join('/home/loving/NEW_Progress/connectome', matrix_file)
    matrix = pd.read_csv(matrix_path, header=None)
    
    print(f"矩阵大小: {matrix.shape}")  # 调试输出矩阵的形状
    print(f"匹配到的脑区索引: {matched_indices}")  # 调试输出匹配的脑区索引
    
    # 确保索引不超出矩阵的范围
    if max(matched_indices) >= matrix.shape[0] or max(matched_indices) >= matrix.shape[1]:
        print("警告: 匹配的脑区索引超出矩阵范围")
        return
    
    sub_matrix = matrix.iloc[matched_indices, matched_indices]

    matched_names = [region_names[i] for i in matched_indices]
    sub_matrix.index = matched_names
    sub_matrix.columns = matched_names

    output_dir = f'roi_csv_{resolution}/nohub'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"{region_prefix.replace('.', '')}_{resolution}.csv")
    sub_matrix.to_csv(output_file)
    print(f"已保存到文件: {output_file}")

def batch_extract_regions(region_list, resolutions):
    """
    批量提取多个脑区的矩阵，支持多个分辨率
    """
    for resolution in resolutions:
        print(f"处理分辨率 {resolution}...")
        for region in region_list:
            if resolution == '36840':
                extract_region_matrix_by_chunks(region, resolution)
            else:
                extract_region_matrix(region, resolution)
    print("所有脑区矩阵提取完成！")

if __name__ == "__main__":
    regions = [
    'lh.caudalanteriorcingulate',
    'lh.cuneus',
    'lh.entorhinal',
    'lh.frontalpole',
    'rh.precentral',
    'rh.precuneus',
    'lh.bankssts',
    'lh.fusiform',
    'lh.inferiortemporal',
    'lh.parsopercularis',
    'lh.isthmuscingulate',
    'lh.middletemporal',
    'lh.postcentral',
    'lh.precuneus',
    'lh.superiortemporal',
    'lh.supramarginal',
    'lh.lingual',
    'lh.paracentral',
    'lh.parahippocampal',
    'lh.pericalcarine',
    'lh.rostralmiddlefrontal',
    'rh.fusiform',
    'rh.inferiortemporal',
    'rh.isthmuscingulate',
    'rh.lingual',
    'rh.postcentral',
    'rh.superiortemporal',
    'rh.supramarginal',
    'lh.lateraloccipital',
    'lh.lateralorbitofrontal',
    'lh.medialorbitofrontal',
    'lh.parsorbitalis',
    'lh.parstriangularis',
    'lh.rostralanteriorcingulate',
    'lh.superiorparietal',
    'lh.temporalpole',
    'lh.transversetemporal',
    'rh.bankssts',
    'rh.caudalanteriorcingulate',
    'rh.caudalmiddlefrontal',
    'rh.cuneus',
    'rh.entorhinal',
    'rh.frontalpole',
    'rh.inferiorparietal',
    'rh.lateraloccipital',
    'rh.lateralorbitofrontal',
    'rh.medialorbitofrontal',
    'rh.middletemporal',
    'rh.paracentral',
    'rh.parahippocampal',
    'rh.parsopercularis',
    'rh.parsorbitalis',
    'rh.parstriangularis',
    'rh.pericalcarine',
    'rh.posteriorcingulate',
    'rh.rostralanteriorcingulate',
    'rh.rostralmiddlefrontal',
    'rh.superiorparietal',
    'rh.temporalpole',
    'rh.transversetemporal'
]

    resolutions = ['173', '756', '390', '1518', '3030', '5976', '12853', '36840']
    batch_extract_regions(regions, resolutions)
