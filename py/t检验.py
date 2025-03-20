import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# 设置路径
base_path = "/home/loving/MRI_Process/topo"
roi_folders = [
    "roi_matrix_173", "roi_matrix_390", "roi_matrix_756", "roi_matrix_1518",
    "roi_matrix_3030", "roi_matrix_5976", "roi_matrix_12853", "roi_matrix_36840"
]

# 结果存储
results = []

for roi_folder in roi_folders:
    print(f"Processing {roi_folder}...")    
    
    hub_path = os.path.join(base_path, roi_folder, "hub", "topological")
    nohub_path = os.path.join(base_path, roi_folder, "nohub", "topological")

    def extract_local_efficiency(folder_path):
        """提取Local Efficiency的所有数值，并计算每个CSV文件的均值"""
        values_list = []
        avg_list = []
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(".csv"):
                    file_path = os.path.join(folder_path, file)
                    df = pd.read_csv(file_path)
                    
                    # 查找 Local Efficiency 所在行
                    local_eff_row = df[df.iloc[:, 0] == "Local Efficiency"]
                    if not local_eff_row.empty:
                        values = local_eff_row.iloc[0, 1:].astype(float).values
                        values_list.append(values)
                        avg_list.append(np.mean(values))
        
        return values_list, avg_list

    # 处理 hub 和 nohub 目录
    hub_values, hub_avg = extract_local_efficiency(hub_path)
    nohub_values, nohub_avg = extract_local_efficiency(nohub_path)

    # 保存数据到 CSV
    hub_df = pd.DataFrame(hub_values)
    hub_df.to_csv(f"/home/loving/MRI_Process/topo/{roi_folder}_hub_raw.csv", index=False)
    pd.DataFrame(hub_avg, columns=["Hub Local Efficiency Mean"]).to_csv(f"/home/loving/MRI_Process/topo/{roi_folder}_hub_avg.csv", index=False)

    nohub_df = pd.DataFrame(nohub_values)
    nohub_df.to_csv(f"{roi_folder}_nohub_raw.csv", index=False)
    pd.DataFrame(nohub_avg, columns=["NoHub Local Efficiency Mean"]).to_csv(f"/home/loving/MRI_Process/topo/{roi_folder}_nohub_avg.csv", index=False)

    # 进行两种T检验
    # 基于原始数据的T检验
    try:
        hub_all = np.concatenate(hub_values) if hub_values else np.array([])
        nohub_all = np.concatenate(nohub_values) if nohub_values else np.array([])
        t_stat_raw, p_value_raw = stats.ttest_ind(hub_all, nohub_all, equal_var=False)
    except:
        t_stat_raw = p_value_raw = np.nan

    # 基于均值的T检验
    try:
        t_stat_avg, p_value_avg = stats.ttest_ind(hub_avg, nohub_avg, equal_var=False)
    except:
        t_stat_avg = p_value_avg = np.nan

    results.append((roi_folder, t_stat_raw, p_value_raw, t_stat_avg, p_value_avg))

# 绘制T检验结果折线图（双坐标轴）
fig, ax1 = plt.subplots(figsize=(12, 6))

# 提取结果数据
roi_labels = [r[0] for r in results]
t_stats_raw = [r[1] for r in results]
p_values_raw = [r[2] for r in results]
t_stats_avg = [r[3] for r in results]
p_values_avg = [r[4] for r in results]

# T统计量（主坐标轴）
ax1.plot(roi_labels, t_stats_raw, 'b-', marker='o', label="T-Statistic (Raw)")
ax1.plot(roi_labels, t_stats_avg, 'b--', marker='x', label="T-Statistic (Avg)")
ax1.set_xlabel("Resolution")
ax1.set_ylabel("T-Statistic", color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_ylim(-5, 5)  # 根据实际数据调整范围

# P值（次坐标轴）
ax2 = ax1.twinx()
ax2.plot(roi_labels, p_values_raw, 'r-', marker='s', label="P-Value (Raw)")
ax2.plot(roi_labels, p_values_avg, 'r--', marker='d', label="P-Value (Avg)")
ax2.set_ylabel("P-Value", color='r')
ax2.tick_params(axis='y', labelcolor='r')
ax2.set_ylim(-0.05, 1.05)
ax2.axhline(y=0.05, color='g', linestyle=':', label="Significance Level (0.05)")

# 合并图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title("T-test Results Comparison: Raw Data vs. Averaged Data")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# 输出 T 检验结果
t_test_df = pd.DataFrame(results, columns=[
    "Resolution", 
    "Raw_T-Statistic", 
    "Raw_P-Value", 
    "Avg_T-Statistic", 
    "Avg_P-Value"
])
t_test_df.to_csv("/home/loving/MRI_Process/topo/t_test_results_comparison.csv", index=False)

plt.show()
print("Processing completed. Results saved.")