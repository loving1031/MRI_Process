import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# 定义需要遍历的文件夹名称
folder_names = ['roi_matrix_173', 'roi_matrix_390', 'roi_matrix_756', 'roi_matrix_1518', 
                'roi_matrix_3030', 'roi_matrix_5976', 'roi_matrix_12853', 'roi_matrix_36840']

# 遍历每个分辨率
for folder in folder_names:
    # 文件夹路径
    hub_dir = f"/home/loving/MRI_Process/topo/{folder}/hub/topological"
    nonhub_dir = f"/home/loving/MRI_Process/topo/{folder}/nohub/topological"
    
    # 初始化Global Efficiency和Degree的列表
    global_efficiency_list = []
    degree_list = []
    
    # 遍历hub_dir和nonhub_dir中的所有csv文件
    for directory in [hub_dir, nonhub_dir]:
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                # 读取csv文件
                csv_path = os.path.join(directory, filename)
                df = pd.read_csv(csv_path, index_col=0)  # 读取文件并设置第一列为行索引
                
                # 提取Global Efficiency和Degree行
                if 'Global Efficiency' in df.index and 'Degree' in df.index:
                    global_efficiency_list.extend(df.loc['Global Efficiency'].values)
                    degree_list.extend(df.loc['Degree'].values)
    
    # 转换为numpy数组并删除NaN和inf值
    global_efficiency_list = np.array(global_efficiency_list)
    degree_list = np.array(degree_list)
    
    # 删除NaN和inf值
    valid_indices = np.isfinite(global_efficiency_list) & np.isfinite(degree_list)
    global_efficiency_list = global_efficiency_list[valid_indices]
    degree_list = degree_list[valid_indices]
    
    # 检查数据是否为空
    if len(global_efficiency_list) == 0 or len(degree_list) == 0:
        print(f"Warning: No valid data for {folder}. Skipping this folder.")
        continue
    
    # 进行皮尔逊相关系数分析
    correlation, p_value = pearsonr(global_efficiency_list, degree_list)
    
    # 在控制台输出p值
    print(f"Folder: {folder} | Pearson correlation: {correlation:.2f} | p-value: {p_value:.4f}")
    
    # 绘制散点图及相关直线
    plt.figure(figsize=(8, 6))
    
    # 让散点图颜色更亮，可以使用色图或者颜色设置
    plt.scatter(degree_list, global_efficiency_list, c='blue', alpha=0.6, edgecolors='w', s=50)  # 更亮的蓝色，并设置边缘颜色
    
    # 绘制相关直线
    plt.plot(degree_list, np.poly1d(np.polyfit(degree_list, global_efficiency_list, 1))(degree_list), color='red', label='Fit Line')
    
    # 设置坐标轴标签
    plt.xlabel('Degree')  # 横纵坐标交换
    plt.ylabel('Global Efficiency')
    plt.title(f'{folder}_GlobalEfficiency_vs_Degree')
    plt.legend()
    
    # 保存图片
    plt.savefig(f"{folder}_globleeffangdegree_final.png")
    plt.close()  # 关闭当前图形，释放内存
    
    # 清空列表以便进行下一个分辨率的处理
    global_efficiency_list = np.array([])  # 重新初始化为空数组
    degree_list = np.array([])  # 重新初始化为空数组
