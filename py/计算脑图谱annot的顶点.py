import nibabel.freesurfer.io as fsio
import numpy as np
import pandas as pd

# 读取 annot 文件
annot_file = "/home/loving/NEW_Progress/brain_map/annot_file/lh.86.annot"
labels, ctab, names = fsio.read_annot(annot_file)

# 获取唯一的 label 值（去掉背景 0）
unique_labels = np.unique(labels)

# 存储每个 label 的顶点信息
label_dict = {name.decode(): np.where(labels == label_value)[0] for label_value, name in zip(unique_labels, names)}

# 打印部分结果
for region, vertices in label_dict.items():
    print(f"Region: {region}, Number of Vertices: {len(vertices)}")

# 保存为 CSV 文件
df = pd.DataFrame([(region, len(vertices), list(vertices)) for region, vertices in label_dict.items()], 
                  columns=["Region", "Vertex_Count", "Vertices"])
df.to_csv("lh_86_labels_vertices.csv", index=False)
