import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# 设定 lausanne120 和 lausanne250 目录
lausanne120_dir = "/home/loving/MRI_Process/lausanne120"
lausanne250_dir = "/home/loving/MRI_Process/schaefer300-yeo7"
output_base_dir = "/home/loving/MRI_Process/Corr"  # 结果保存路径
correlation_file = os.path.join(output_base_dir, "corr_Schaefer300toDK114.csv")  # 相关性系数保存路径

# 获取 lausanne120 和 lausanne250 目录下的文件夹名
lausanne120_folders = {
    re.search(r"fc_(\w+)_lausanne120", folder).group(1): os.path.join(lausanne120_dir, folder, "symmetric_matrix.csv")
    for folder in os.listdir(lausanne120_dir)
    if os.path.isdir(os.path.join(lausanne120_dir, folder)) and re.search(r"fc_(\w+)_lausanne120", folder)
}

lausanne250_folders = {
    re.search(r"fc_(\w+)_schaefer300-yeo7", folder).group(1): os.path.join(lausanne250_dir, folder, "transformed_Schaefer300toDK114.csv")
    for folder in os.listdir(lausanne250_dir)
    if os.path.isdir(os.path.join(lausanne250_dir, folder)) and re.search(r"fc_(\w+)_schaefer300-yeo7", folder)
}

# 用于存储相关性结果
correlation_results = []

# 遍历匹配的文件夹对
for key in lausanne120_folders.keys() & lausanne250_folders.keys():  # 取交集，找到匹配的 XXX
    symmetric_matrix_path = lausanne120_folders[key]
    transformed_tval_path = lausanne250_folders[key]

    print(f"处理匹配的文件对：\n  X: {symmetric_matrix_path}\n  Y: {transformed_tval_path}")

    # 读取 symmetric_matrix.csv（包含脑区名称）
    df_x = pd.read_csv(symmetric_matrix_path, header=None)

    # 读取 transformed_tval.csv（无脑区名称）
    df_y = pd.read_csv(transformed_tval_path, header=None)

    # 提取数值部分（仅取上三角）
    x_values = df_x.values[np.triu_indices_from(df_x, k=1)]
    y_values = df_y.values[np.triu_indices_from(df_y, k=1)]

    # 计算皮尔逊相关性
    corr, p_value = pearsonr(x_values, y_values)

    # 生成散点图
    plt.figure(figsize=(8, 6))
    sns.regplot(x=x_values, y=y_values, scatter_kws={"s": 5}, line_kws={"color": "red"}, ci=None)

    # 设置标题和标签
    plt.xlabel("lausanne120")
    plt.ylabel("Schaefer300")
    plt.title(f"Pearson Correlation ({key}): r = {corr:.3f}, p = {p_value:.3g}")

    # 确保保存目录存在
    output_dir = os.path.join(output_base_dir, key)
    os.makedirs(output_dir, exist_ok=True)

    # 保存散点图，文件名固定为 scatter_DK219toDK114.svg
    output_path = os.path.join(output_dir, "scatter_Schaefer300toDK114.svg")
    plt.savefig(output_path, format="svg")
    plt.close()

    print(f"散点图已保存至 {output_path}")
    print(f"皮尔逊相关系数: {corr:.3f}, p 值: {p_value:.3g}")

    # 记录相关性结果
    correlation_results.append([key, corr, p_value])

# 转换为 DataFrame 并保存
df_corr = pd.DataFrame(correlation_results, columns=["Dataset", "Pearson_r", "P_value"])
df_corr.to_csv(correlation_file, index=False)

print(f"所有相关性系数已保存至 {correlation_file}")
print("所有匹配的文件对处理完成！")
