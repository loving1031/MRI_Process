import os
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# 所有的分辨率文件夹名字
folder_names = [
    "roi_matrix_173", "roi_matrix_390", "roi_matrix_756", 
    "roi_matrix_1518", "roi_matrix_3030", "roi_matrix_5976", 
    "roi_matrix_12853", "roi_matrix_36840"
]

# 定义父目录路径
base_path = "/home/loving/MRI_Process/topo"

# 用于存储结果
results = {"Resolution": [], "T-Value": [], "P-Value": []}

# 遍历每个文件夹并执行分析
for folder_name in folder_names:
    # 动态生成 Hub 和非-Hub 文件夹路径
    hub_dir = f"{base_path}/{folder_name}/hub/topological"
    nonhub_dir = f"{base_path}/{folder_name}/nohub/topological"

    # 用于存储全局效率值
    hub_efficiency = []
    nonhub_efficiency = []

    # 遍历 Hub 文件夹中的所有 CSV 文件，提取全局效率
    for file in os.listdir(hub_dir):
        if file.endswith(".csv"):  # 确保是 CSV 文件
            file_path = os.path.join(hub_dir, file)
            data = pd.read_csv(file_path)
            # 提取全局效率 (Global Efficiency) 一行的值
            global_eff = data.loc[data.iloc[:, 0] == "Local Efficiency"].iloc[:, 1:].values.flatten()
            hub_efficiency.extend(global_eff)

    # 遍历非-Hub 文件夹中的所有 CSV 文件，提取全局效率
    for file in os.listdir(nonhub_dir):
        if file.endswith(".csv"):  # 确保是 CSV 文件
            file_path = os.path.join(nonhub_dir, file)
            data = pd.read_csv(file_path)
            # 提取全局效率 (Global Efficiency) 一行的值
            global_eff = data.loc[data.iloc[:, 0] == "Local Efficiency"].iloc[:, 1:].values.flatten()
            nonhub_efficiency.extend(global_eff)
    print(hub_efficiency)
    print(nonhub_efficiency)
    # 转换为 pandas Series 并去除空值
    hub_efficiency = pd.Series(hub_efficiency).dropna().astype(float)
    nonhub_efficiency = pd.Series(nonhub_efficiency).dropna().astype(float)

    # 检查是否有足够数据进行 T 检验
    if len(hub_efficiency) > 1 and len(nonhub_efficiency) > 1:
        # 执行 T 检验
        t_stat, p_value = stats.ttest_ind(hub_efficiency, nonhub_efficiency, equal_var=True)

        # 存储结果
        results["Resolution"].append(folder_name)
        results["T-Value"].append(t_stat)
        results["P-Value"].append(p_value)
        
        # 输出结果
        print(f"分辨率: {folder_name}")
        print(f"T 统计量: {t_stat}")
        print(f"P 值: {p_value}")

        # 判断显著性
        if p_value < 0.05:
            print("Hub 节点与非-Hub 节点的局部效率存在显著差异。\n")
        else:
            print("Hub 节点与非-Hub 节点的局部效率没有显著差异。\n")
    else:
        print(f"分辨率: {folder_name} 数据不足，无法进行 T 检验。\n")
        results["Resolution"].append(folder_name)
        results["T-Value"].append(None)
        results["P-Value"].append(None)

# 将结果转换为 DataFrame
results_df = pd.DataFrame(results)

# 绘制双坐标轴图
fig, ax1 = plt.subplots(figsize=(12, 7))

# 绘制 P 值曲线
ax1.plot(results_df["Resolution"], results_df["P-Value"], marker='o', color='blue', label="P-Value")
ax1.axhline(0.05, color='red', linestyle='--', label="Significance Threshold (p=0.05)")
ax1.set_ylabel("P-Value", fontsize=14, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_ylim(0, 1.05)

# 添加 T 值的第二坐标轴
ax2 = ax1.twinx()
ax2.plot(results_df["Resolution"], results_df["T-Value"], marker='o', color='green', label="T-Value")
ax2.set_ylabel("T-Value", fontsize=14, color='green')
ax2.tick_params(axis='y', labelcolor='green')

# 设置标题和 X 轴
plt.title("T-Value and P-Value Across Resolutions", fontsize=16)
ax1.set_xlabel("Resolution", fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12) 
# 添加图例
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.9), fontsize=12)
ax1.set_ylim(-1, 1) 
# 添加网格
ax1.grid(alpha=0.5)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()
