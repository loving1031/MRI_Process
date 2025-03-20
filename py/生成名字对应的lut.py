import os
import numpy as np

def generate_lut_from_file(input_file, output_file):
    """
    从指定的文件中读取文件名，并生成一个随机颜色的 LUT 文件。
    
    :param input_file: 输入文件名列表的路径
    :param output_file: 生成的 LUT 文件路径
    """
    try:
        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            print(f"输入文件 '{input_file}' 不存在！")
            return
        
        # 读取文件名列表
        with open(input_file, "r") as f:
            file_names = [line.strip() for line in f if line.strip()]
        
        # 创建 LUT 条目
        lut_entries = []
        for i, file_name in enumerate(file_names, start=1):
            # 去掉后缀以获取区域名称
            region_name = os.path.splitext(file_name)[0]
            # 随机生成 RGB 颜色
            r, g, b = np.random.randint(0, 256, size=3)
            # 添加到 LUT 列表
            lut_entries.append(f"{i} {region_name} {r} {g} {b} 0")
        
        # 写入 LUT 文件
        with open(output_file, "w") as f:
            f.write("\n".join(lut_entries))
        
        print(f"LUT 文件已生成：{output_file}")
    
    except PermissionError:
        print(f"没有权限访问文件 '{input_file}' 或写入 '{output_file}'！")
    except Exception as e:
        print(f"发生错误：{e}")

# 示例用法
input_file_path = "filename.txt"  # 替换为你的输入文件路径
output_file_path = "/home/loving/NEW_Progress/lh_lut_91.txt"  # 指定输出文件路径
generate_lut_from_file(input_file_path, output_file_path)
