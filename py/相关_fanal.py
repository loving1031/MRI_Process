import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np

# 所有的分辨率文件夹名字
folder_names = [
    "roi_matrix_173", "roi_matrix_390", "roi_matrix_756", 
    "roi_matrix_1518", "roi_matrix_3030", "roi_matrix_5976", 
    "roi_matrix_12853", "roi_matrix_36840"
]

# 定义父目录路径
base_path = "/home/loving/MRI_Process/topo"

# 遍历每个文件夹
for folder_name in folder_names:
    # 动态生成 Hub 和 Non-Hub 文件夹路径
    hub_dir = f"{base_path}/{folder_name}/hub/topological"
    nonhub_dir = f"{base_path}/{folder_name}/nohub/topological"
    
    # 用于存储 Degree 和 Global Efficiency 值
    degree_values = []
    global_eff_values = []

    # 遍历 Hub 和 Non-Hub 文件夹中的所有 CSV 文件
    for folder in [hub_dir, nonhub_dir]:
        for file in os.listdir(folder):
            if file.endswith(".csv"):  # 确保是 CSV 文件
                file_path = os.path.join(folder, file)
                data = pd.read_csv(file_path)

                # 检查是否同时包含 Degree 和 Global Efficiency 数据
                if "Degree" in data.iloc[:, 0].values and "Global Efficiency" in data.iloc[:, 0].values:
                    # 提取 Degree 和 Global Efficiency 的值（确保索引对应）
                    degree = data.loc[data.iloc[:, 0] == "Degree"].iloc[:, 1:].values.flatten()
                    global_eff = data.loc[data.iloc[:, 0] == "Global Efficiency"].iloc[:, 1:].values.flatten()

                    # 过滤掉缺失值并确保 Degree 和 Global Efficiency 对应位置匹配
                    valid_indices = ~pd.isna(degree) & ~pd.isna(global_eff)
                    degree = degree[valid_indices]
                    global_eff = global_eff[valid_indices]

                    # 添加到列表中
                    degree_values.extend(degree)
                    global_eff_values.extend(global_eff)
    
    # 转换为 pandas Series 并去除空值
    degree_values = pd.Series(degree_values).dropna().astype(float)
    global_eff_values = pd.Series(global_eff_values).dropna().astype(float)

    # 检查数据是否足够进行相关性分析
    if len(degree_values) > 1 and len(global_eff_values) > 1:
        # 计算皮尔逊相关系数
        corr, _ = pearsonr(degree_values, global_eff_values)
        print(f"分辨率: {folder_name}")
        print(f"相关系数: {corr}\n")
        
        # 绘制散点图
        plt.figure(figsize=(8, 6))
        
        # 使用不同的颜色表示 Hub 和 Non-Hub 数据
        hub_indices = degree_values.index < len(degree_values) // 2
        nonhub_indices = ~hub_indices
        plt.scatter(degree_values[hub_indices], global_eff_values[hub_indices], alpha=0.7, color='blue', edgecolors='k', label="Hub", s=50)
        plt.scatter(degree_values[nonhub_indices], global_eff_values[nonhub_indices], alpha=0.7, color='red', edgecolors='k', label="Non-Hub", s=50)

        # 拟合并绘制回归直线
        p = np.polyfit(degree_values, global_eff_values, 1)
        plt.plot(degree_values, np.polyval(p, degree_values), color='black', linestyle='--', label=f"Fit Line (r = {corr:.2f})")
        
        plt.title(f"Degree vs Global Efficiency ({folder_name})", fontsize=16)
        plt.xlabel("Degree", fontsize=14)
        plt.ylabel("Global Efficiency", fontsize=14)
        plt.legend(fontsize=12)
        plt.grid(alpha=0.5)
        
        # 保存图片
        output_file = f"{folder_name}_degreeandglobleff.png"
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
    else:
        print(f"分辨率: {folder_name} 数据不足，无法进行相关性分析。\n")