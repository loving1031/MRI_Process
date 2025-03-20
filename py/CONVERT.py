import os
import pandas as pd
from TACOS import convertStatistics

# 设定主目录
root_dir = "/home/loving/MRI_Process/schaefer300-yeo7"

# 遍历主目录下的所有子文件夹
for folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder)

    # 确保是文件夹
    if os.path.isdir(folder_path):
        source_file = os.path.join(folder_path, "symmetric_matrix.csv")

        # 检查文件是否存在
        if os.path.exists(source_file):
            print(f"正在处理: {source_file}")

            try:
                # 逐行读取文件
                cleaned_data = []
                with open(source_file, "r") as f:
                    for line in f:
                        cleaned_row = []
                        for value in line.strip().split(","):  # 以逗号分隔
                            try:
                                cleaned_row.append(float(value))  # 转换为浮点数
                            except ValueError:
                                cleaned_row.append(0)  # 不能转换的设为 0
                        cleaned_data.append(cleaned_row)

                # 重新保存到 cleaned_symmetric_matrix.csv
                cleaned_file = os.path.join(folder_path, "cleaned_symmetric_matrix.csv")
                with open(cleaned_file, "w") as f:
                    for row in cleaned_data:
                        f.write(",".join(map(str, row)) + "\n")

                print(f"已清理数据并保存为: {cleaned_file}")

                # 进行转换
                transformed_tval = convertStatistics(
                    source_tval=cleaned_file,  # 使用清理后的文件
                    source_atlas="Schaefer300",
                    target_atlas="DK114",
                    type="functional",
                )

                # 转换为 DataFrame 并保存
                df_transformed = pd.DataFrame(transformed_tval)
                output_file = os.path.join(folder_path, "transformed_Schaefer300toDK114.csv")
                df_transformed.to_csv(output_file, index=False, header=False)

                print(f"转换后的 cohen 统计量已保存到 {output_file}")

            except Exception as e:
                print(f"处理 {source_file} 时出错：{e}")

print("所有文件处理完成！")
