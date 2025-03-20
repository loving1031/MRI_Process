import nibabel.freesurfer.io as fs

# 文件路径
input_annot = "/home/loving/freesurfer/subjects/subject2/label/rh.annot_86.annot"  # 替换为输入的 .annot 文件路径
output_annot = "/home/loving/NEW_Progress/rh.annot_modified"  # 替换为输出的 .annot 文件路径
filename_txt = "filename.txt"  # 替换为包含脑区名称的文件路径

# 读取文件名并去掉后缀
with open(filename_txt, "r") as f:
    new_names = [line.strip().replace(".label", "") for line in f if line.strip()]

# 加载 .annot 文件
labels, ctab, names = fs.read_annot(input_annot, orig_ids=True)

# 检查新名字数量是否匹配
if len(new_names) != len(names):
    raise ValueError(f"文件中的脑区名称数量 ({len(new_names)}) 与 .annot 文件中的数量 ({len(names)}) 不匹配！")

# 替换脑区名称
for i, new_name in enumerate(new_names):
    print(f"替换脑区: {names[i].decode('utf-8')} -> {new_name}")
    names[i] = new_name.encode("utf-8")  # 将新名字编码为字节格式

# 保存修改后的 .annot 文件
fs.write_annot(output_annot, labels, ctab, names)
print(f"修改后的 .annot 文件已保存到: {output_annot}")
