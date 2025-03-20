import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# 设置基础目录
base_dir = "/home/loving/MRI_Process/topo"

# 遍历 topo 目录下的所有子文件夹
for folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder)

    # 确保是文件夹
    if os.path.isdir(folder_path):
        print(f"正在处理文件夹: {folder}")

        for subfolder in ["hub", "nohub"]:
            subfolder_path = os.path.join(folder_path, subfolder, "topological")

            # 确保 topological 文件夹存在
            if os.path.exists(subfolder_path):
                print(f"  处理子文件夹: {subfolder_path}")

                # 创建 "相关性分析" 目录
                output_dir = os.path.join(subfolder_path, "相关性分析")
                os.makedirs(output_dir, exist_ok=True)

                # 遍历 CSV 文件
                for file in os.listdir(subfolder_path):
                    if file.endswith(".csv"):
                        csv_path = os.path.join(subfolder_path, file)
                        df = pd.read_csv(csv_path, index_col=0)

                        # 确保 Degree 和 Local Efficiency 存在
                        if "Degree" in df.index and "Local Efficiency" in df.index:
                            degree = df.loc["Degree"].dropna().values  # 去除 NaN
                            local_efficiency = df.loc["Local Efficiency"].dropna().values  # 去除 NaN

                            # 如果数据量小于 2，则跳过
                            if len(degree) < 2 or len(local_efficiency) < 2:
                                print(f"    ⚠️ {file} 数据不足（少于2个点），跳过。")
                                continue

                            # 计算皮尔逊相关系数
                            r, p = pearsonr(degree, local_efficiency)

                            # 绘制散点图
                            plt.figure(figsize=(6, 5))
                            sns.regplot(x=degree, y=local_efficiency, 
                                        scatter_kws={"s": 50, "color": "red"}, 
                                        line_kws={"color": "blue"}, ci=95)

                            # 设置标题（包含 r 和 p 值）
                            plt.title(f"{file} (Pearson r={r:.4f}, p={p:.4f})", fontsize=12)
                            plt.xlabel("Degree", fontsize=12)
                            plt.ylabel("Local Efficiency", fontsize=12)
                            plt.grid(True)

                            # 保存图像
                            output_path = os.path.join(output_dir, f"{file}_correlation.png")
                            plt.savefig(output_path, dpi=300, bbox_inches="tight")
                            plt.close()  # 关闭图像，释放内存
                        else:
                            print(f"    ⚠️ {file} 缺少 Degree 或 Local Efficiency，跳过。")

                print(f"  相关性分析完成，结果已保存在: {output_dir}")

print("所有分析完成！")
