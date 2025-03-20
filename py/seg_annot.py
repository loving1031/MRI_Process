import nibabel as nib
import numpy as np
import os
import random

# 加载 FreeSurfer 的 .annot 文件
vertices, labels, colortable = nib.freesurfer.read_annot("lh.aparc.annot")

# 创建输出目录
output_dir = "annot_output"
os.makedirs(output_dir, exist_ok=True)

# 初始化新的标签数组
new_labels = np.zeros_like(labels)

# 初始化新的颜色映射表 (标签ID, RGBA 颜色)
new_color_table = []
label_names = []  # 存储标签名（字符串列表）

label_counter = 1  # 新标签ID的计数器

# 遍历每个旧标签并进行细分
for old_label in np.unique(labels):
    if old_label == 0:
        continue  # 跳过背景标签

    # 找到属于当前标签的顶点索引
    vertex_indices = np.where(labels == old_label)[0]

    # 细分成 N 个区域 (可以根据需求调整)
    N = 5  # 每个区域分为 5 个子区域
    split_size = len(vertex_indices) // N

    for i in range(N):
        # 获取当前子区域的顶点索引
        if i == N - 1:  # 最后一部分包含剩余的所有顶点
            sub_indices = vertex_indices[i * split_size:]
        else:
            sub_indices = vertex_indices[i * split_size:(i + 1) * split_size]

        # 分配新的标签ID
        new_labels[sub_indices] = label_counter

        # 生成随机颜色 (R, G, B, A)， Alpha 通道设置为 0
        color = [random.randint(0, 255) for _ in range(3)] + [0]
        new_color_table.append(color)  # 只保留颜色，不添加标签ID

        # 存储标签名（确保是字符串）
        label_names.append(f"ROI_{label_counter}")

        label_counter += 1

# 将颜色映射表转换为 numpy 数组格式
new_color_table_array = np.array(new_color_table, dtype=np.int32)

# 确保标签名是字节字符串（字节数组），并添加 null 字符
label_names_bytes = [name.encode('utf-8') + b'\x00' for name in label_names]  # 添加结尾的 null 字符

# 保存新的 .annot 文件
new_annot_path = os.path.join(output_dir, "lh.aparc_subdivided.annot")

# 使用 nibabel 的 write_annot 函数写入 .annot 文件
nib.freesurfer.write_annot(
    new_annot_path,
    vertices,
    new_labels,
    (label_names_bytes, new_color_table_array)
)

print(f"新的 .annot 文件已保存为：{new_annot_path}")
print(f"包含 {label_counter - 1} 个新标签区域。")
