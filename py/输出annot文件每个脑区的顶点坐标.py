import nibabel.freesurfer.io as fs
import numpy as np

# 文件路径
annot_file = "/home/loving/freesurfer/subjects/subject2/label/lh.annot_86.annot"  # .annot 文件路径
surf_file = "/home/loving/freesurfer/subjects/subject2/surf/lh.pial"  # 表面网格文件路径
output_file = "/home/loving/MRI_Process/annot_ras_coordinates.txt"  # 输出文件路径

# 加载 .annot 文件
labels_annot, ctab, names = fs.read_annot(annot_file, orig_ids=True)

# 加载表面网格文件 (pial 表面)
vertices, _ = fs.read_geometry(surf_file)

# 打开文件写入结果
with open(output_file, 'w') as f:
    f.write("脑区 RAS 坐标\n")
    f.write("=====================\n\n")

    # 遍历每个 .annot 的脑区标号
    unique_labels_annot = np.unique(labels_annot)

    for annot_label in unique_labels_annot:
        if annot_label <= 0:  # 跳过背景区域或未定义标号
            continue

        # 查找属于当前 annot_label 的顶点索引
        vertex_indices = np.where(labels_annot == annot_label)[0]

        # 获取这些顶点的表面坐标 (这些坐标已经是 RAS 坐标)
        ras_coords = vertices[vertex_indices]

        # 获取脑区名称
        ctab_indices = np.where(ctab[:, -1] == annot_label)[0]
        if len(ctab_indices) == 0:
            region_name = "Unknown"
        else:
            region_name = names[ctab_indices[0]].decode("utf-8")

        # 写入脑区名称
        f.write(f"脑区 {region_name} 的 RAS 坐标:\n")
        
        # 写入每个顶点的 RAS 坐标
        for coord in ras_coords:
            f.write(f"{coord}\n")
        
        # 写入每个脑区的顶点总数
        f.write(f"总计 {len(ras_coords)} 个顶点\n\n")

print(f"结果已保存到: {output_file}")
