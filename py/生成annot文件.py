import os
import nibabel.freesurfer.io as fs
import numpy as np

# 路径配置
output_annot = "/home/loving/freesurfer/subjects/subject2/label/rh.87.annot"
label_dir = "/home/loving/NEW_Progress/rh_label_seg_87/"  # 包含所有 label 文件的目录
lut_file = "/home/loving/NEW_Progress/generated_lut.txt"  # 颜色映射表文件

# 1. 读取颜色映射表 (格式: <label_id> <name> <R> <G> <B> <A>)
lut = np.loadtxt(lut_file, dtype={"names": ("id", "name", "r", "g", "b", "a"),
                                  "formats": ("i4", "S255", "i4", "i4", "i4", "i4")})
ctab = np.zeros((len(lut), 5), dtype=int)  # 存储颜色表 (R, G, B, A, ID)
names = []

for i, row in enumerate(lut):
    ctab[i, :4] = [row["r"], row["g"], row["b"], row["a"]]
    ctab[i, 4] = row["id"]
    names.append(row["name"].decode('utf-8'))

# 2. 初始化顶点标签数组
# 获取标签目录下所有的 .label 文件
label_files = [os.path.join(label_dir, f) for f in os.listdir(label_dir) if f.endswith(".label")]

# 获取顶点总数，假设是从 0 到 n-1
n_vertices = 0
for label_file in label_files:
    # 检查文件是否为空
    if os.path.getsize(label_file) > 0:
        try:
            # 手动读取文件并跳过非数字行
            with open(label_file, 'r') as f:
                lines = f.readlines()
                # 跳过前两行元数据（这两行是 FreeSurfer label 文件的标准头部）
                vertices = []
                for line in lines[2:]:  # 从第三行开始读取顶点数据
                    try:
                        # 尝试转换为整数，如果成功则为顶点
                        vertex = int(line.split()[0])  # 假设第一个字段是顶点索引
                        vertices.append(vertex)
                    except ValueError:
                        continue  # 如果转换失败，跳过当前行
                vertices = np.array(vertices)
                
                if vertices.size > 0:  # 确保顶点数据不为空
                    n_vertices = max(n_vertices, np.max(vertices) + 1)  # 更新顶点总数
        except Exception as e:
            print(f"跳过文件 {label_file}，读取时遇到错误：{e}")

labels = np.zeros(n_vertices, dtype=int)

# 3. 读取所有 .label 文件并更新顶点标签
for label_id, label_file in enumerate(label_files, start=1):  # 标签 ID 从 1 开始
    # 检查文件是否为空
    if os.path.getsize(label_file) > 0:
        try:
            # 手动读取文件并跳过非数字行
            with open(label_file, 'r') as f:
                lines = f.readlines()
                # 跳过前两行元数据（这两行是 FreeSurfer label 文件的标准头部）
                vertices = []
                for line in lines[2:]:  # 从第三行开始读取顶点数据
                    try:
                        # 尝试转换为整数，如果成功则为顶点
                        vertex = int(line.split()[0])  # 假设第一个字段是顶点索引
                        vertices.append(vertex)
                    except ValueError:
                        continue  # 如果转换失败，跳过当前行
                vertices = np.array(vertices)
                
                if vertices.size > 0:  # 确保顶点数据不为空
                    labels[vertices] = label_id  # 更新顶点标签
        except Exception as e:
            print(f"跳过文件 {label_file}，读取时遇到错误：{e}")

# 4. 写入 .annot 文件
fs.write_annot(output_annot, labels, ctab, names)

print(f"成功生成 .annot 文件: {output_annot}")
