import nibabel as nib
import numpy as np

# 路径设置
input_annot_file = "/home/loving/freesurfer/subjects/subject2/label/lh.aparc.annot"
output_annot_file = "lh.aparc_1000.annot"
lut_path = "/home/loving/freesurfer/FreeSurferColorLUT.txt"  # FreeSurferColorLUT.txt 文件路径

# 载入 .annot 文件
vertices, labels, colortable = nib.freesurfer.read_annot(input_annot_file)

# 读取 FreeSurferColorLUT.txt 颜色映射表
def load_freesurfer_lut(lut_path):
    lut = {}
    with open(lut_path, 'r') as f:
        for line in f:
            if not line.startswith('#') and line.strip():
                fields = line.split()
                label_id = int(fields[0])
                label_name = fields[1]
                r, g, b, a = map(int, fields[2:6])
                lut[label_id] = (label_name, (r, g, b, a))
    return lut

freesurfer_lut = load_freesurfer_lut(lut_path)

# 创建新的标签和 colortable，分割成 1000 个脑区
new_labels = labels.copy()
new_colortable = []

# 生成 1000 个分割标签
for i in range(1, 1001):
    # 依据 FreeSurfer LUT 选择颜色，如果没有则默认灰色
    if i in freesurfer_lut:
        label_name, color = freesurfer_lut[i]
    else:
        label_name = f"Region_{i}"
        color = (128, 128, 128, 0)  # 默认灰色

    # 为每个新区域生成标签 ID，并更新 colortable
    new_colortable.append((label_name, color[0], color[1], color[2], color[3]))
    new_labels[labels == i] = i

# 生成 colortable 结构
new_ctab = np.zeros((len(new_colortable), 5), dtype=int)
new_names = []
for idx, (name, r, g, b, a) in enumerate(new_colortable):
    new_names.append(name.encode('utf-8'))
    new_ctab[idx] = [r, g, b, a, idx]

# 写入新的 .annot 文件
nib.freesurfer.write_annot(output_annot_file, vertices, new_labels, (new_names, new_ctab))

print(f"新的 .annot 文件已保存到 {output_annot_file}")
