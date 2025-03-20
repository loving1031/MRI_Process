import numpy as np
import nibabel as nib
import nibabel.freesurfer.io as fs
from sklearn.neighbors import NearestNeighbors

def load_annot(file_path):
    """
    加载 .annot 文件，提取顶点标号和脑区名称。
    """
    labels, ctab, names = fs.read_annot(file_path)
    region_names = []
    
    # 获取脑区名称
    for entry in ctab:
        if isinstance(entry[-1], bytes):
            region_names.append(entry[-1].decode('utf-8'))
        else:
            region_names.append(str(entry[-1]))  # 转换为字符串
    return labels, region_names

def load_mgz(file_path):
    """
    加载 .mgz 文件，提取体素数据并展平为 1D 数组。
    """
    mgz_img = nib.load(file_path)
    mgz_data = mgz_img.get_fdata()
    return mgz_data

def extract_ras_coordinates(surface_file):
    """
    加载 FreeSurfer 表面文件（如 lh.white），提取顶点的 RAS 坐标。
    """
    coords, _ = nib.freesurfer.io.read_geometry(surface_file)
    return coords

def match_annot_to_mgz(annot_labels, annot_coords, mgz_data, surface_coords, tolerance=1e-3):
    """
    通过顶点坐标比对，匹配 .annot 和 .mgz 文件的脑区编号。
    使用 KD树进行近邻匹配。
    """
    matches = {}
    unique_annot_labels = np.unique(annot_labels)

    # 使用 KD 树进行匹配
    nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto', metric='euclidean').fit(surface_coords)
    
    # 展平 mgz_data 体积数据为 1D 数组
    mgz_data_flat = mgz_data.flatten()

    # 为每个 annot 标号找到最近的 mgz 标号
    for annot_label in unique_annot_labels:
        if annot_label == 0:  # 跳过背景区域
            continue

        # 获取 annot 文件中该标号的所有顶点坐标
        annot_indices = np.where(annot_labels == annot_label)[0]
        annot_region_coords = annot_coords[annot_indices]

        # 找到最近的 mgz 顶点
        distances, indices = nbrs.kneighbors(annot_region_coords)

        # 判断最近邻匹配的数量
        if np.all(distances < tolerance):  # 如果匹配的距离小于容忍度，则认为匹配成功
            # 使用 indices 查找对应的 mgz 数据
            # 因为 mgz_data 已经展平为 1D，我们需要正确映射
            flat_index = indices[0][0]  # 获取索引
            mgz_label = mgz_data_flat[flat_index]  # 使用展平后的索引访问数据
            matches[annot_label] = mgz_label

    return matches

def save_results(results, annot_names, output_file):
    """
    保存匹配结果到文件。
    """
    with open(output_file, 'w') as f:
        f.write("Annot Label, Annot Name, MGZ Label\n")
        for annot_label, mgz_label in results.items():
            annot_name = annot_names[annot_label] if annot_label < len(annot_names) else "Unknown"
            f.write(f"{annot_label}, {annot_name}, {mgz_label}\n")

def main():
    # 输入文件路径
    annot_file = "/home/loving/freesurfer/subjects/subject2/label/lh.annot_86.annot"
    mgz_file = "/home/loving/NEW_Progress/segmap_200_cortex.mgz"
    surface_file = "/home/loving/freesurfer/subjects/subject2/surf/lh.white"  # FreeSurfer表面文件

    # 加载数据
    annot_labels, annot_names = load_annot(annot_file)
    mgz_data = load_mgz(mgz_file)
    surface_coords = extract_ras_coordinates(surface_file)

    # 匹配 .annot 和 .mgz
    results = match_annot_to_mgz(annot_labels, surface_coords, mgz_data, surface_coords)

    # 保存结果
    output_file = "annot_mgz_matches.txt"
    save_results(results, annot_names, output_file)
    print(f"匹配结果已保存到 {output_file}")

if __name__ == "__main__":
    main()
