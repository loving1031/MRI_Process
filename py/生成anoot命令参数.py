import os

# 获取当前工作目录
current_directory = '/home/loving/NEW_Progress/lh_label_seg_86_195_381_762_1519_2963'

# 列出当前目录下的所有文件，并按字母顺序排序
files = sorted(os.listdir(current_directory))

# 初始化输出列表
output = []

# 生成每个文件的路径
for file in files:
    # 确保只处理文件，不处理目录
    if os.path.isfile(os.path.join(current_directory, file)):
        output.append(f"--l {os.path.join(current_directory, file)}")

# 定义输出文件名
output_file_name = "生成annot文件命令参数.txt"

# 将内容输出到文件中
with open(output_file_name, 'w') as f:
    f.write(" ".join(output))