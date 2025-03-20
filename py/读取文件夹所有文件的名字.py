import os

def list_sorted_files(directory, output_file="/home/loving/MRI_Process/topo/A.txt"):
    """
    列出指定文件夹中所有文件的名字，按字母顺序排序，并保存到文件中，
    保存时去掉 `.nii.gz` 后缀。

    :param directory: 文件夹路径
    :param output_file: 保存文件名的文件路径，默认为 'A_filename_1518.txt'
    """
    try:
        # 获取文件夹中所有文件的名字，去掉 `.nii.gz` 后缀
        file_names = [os.path.splitext(f)[0].replace(".nii", "") for f in os.listdir(directory)
                      if os.path.isfile(os.path.join(directory, f)) and f.endswith(".nii.gz")]
        # 按字母顺序排序
        sorted_file_names = sorted(file_names)
        
        # 保存到文件
        with open(output_file, "a") as f:
            for file_name in sorted_file_names:
                f.write(file_name + "\n")
        
        print(f"文件名列表（去掉 .nii.gz 后缀）已保存到 '{output_file}' 中！")
    except FileNotFoundError:
        print(f"文件夹 '{directory}' 不存在！")
    except PermissionError:
        print(f"没有权限访问文件夹 '{directory}'！")

# 示例：指定文件夹路径
folder_path = "/home/loving/MRI_Process/topo"  # 替换为你的文件夹路径
list_sorted_files(folder_path)
