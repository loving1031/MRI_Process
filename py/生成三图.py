import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

# 读取数据
file_x1 = "transforming_accuracy_processed.csv"
file_x2 = "transforming_accuracy_std.csv"
file_y = "atlas_consistency_reordered.csv"

df_x1 = pd.read_csv(file_x1, index_col=0)
df_x2 = pd.read_csv(file_x2, index_col=0)
df_y = pd.read_csv(file_y, index_col=0)

# 转换数据为数值型，非数值转换为 NaN
df_x1 = df_x1.apply(pd.to_numeric, errors='coerce')
df_x2 = df_x2.apply(pd.to_numeric, errors='coerce')
df_y = df_y.apply(pd.to_numeric, errors='coerce')

# 展平数据
x1_values = df_x1.values.flatten()
x2_values = df_x2.values.flatten()
y_values = df_y.values.flatten()

# 去除 NaN
def filter_valid_data(x, y):
    mask = ~np.isnan(x) & ~np.isnan(y)
    return x[mask], y[mask]

x1_filtered, y1_filtered = filter_valid_data(x1_values, y_values)
x2_filtered, y2_filtered = filter_valid_data(x2_values, y_values)

# 计算皮尔逊相关系数
def compute_pearson(x, y):
    if len(x) > 1:
        r, p = stats.pearsonr(x, y)
        return f"r={r:.2f}, p={p:.3f}"
    return "Scatter Plot (Not enough data)"

title_x1 = compute_pearson(x1_filtered, y1_filtered)
title_x2 = compute_pearson(x2_filtered, y2_filtered)

# 放大整体图形，保持等比例布局
scale_factor = 1.1  # 这里是放大的倍数，你可以再调大点
base_figsize = (20, 6)
figsize = (base_figsize[0] * scale_factor, base_figsize[1] * scale_factor)

fig, axes = plt.subplots(1, 3, figsize=figsize, gridspec_kw={'width_ratios': [1, 1, 1]})

# 左侧绘制热图
sns.heatmap(df_y, annot=False, cmap="coolwarm", linewidths=0.2, ax=axes[0], square=True, cbar_kws={'shrink': 0.7})
axes[0].set_title("Atlas Consistency", fontsize=16 * scale_factor)
axes[0].tick_params(axis='both', labelsize=12 * scale_factor)

# 中间绘制第一个散点图
sns.regplot(x=x1_filtered, y=y1_filtered, ax=axes[1], scatter_kws={'s': 50 * scale_factor}, line_kws={'color': 'red', 'linewidth': 1.5})
axes[1].set_xlabel("Transforming Accuracy (Mean)", fontsize=14 * scale_factor)
axes[1].set_ylabel("Atlas Consistency", fontsize=14 * scale_factor)
axes[1].set_title(title_x1, fontsize=14 * scale_factor)
axes[1].tick_params(axis='both', labelsize=12 * scale_factor)

# 右侧绘制第二个散点图
sns.regplot(x=x2_filtered, y=y2_filtered, ax=axes[2], scatter_kws={'s': 50 * scale_factor}, line_kws={'color': 'red', 'linewidth': 1.5})
axes[2].set_xlabel("Transforming Accuracy (Std)", fontsize=14 * scale_factor)
axes[2].set_ylabel("Atlas Consistency", fontsize=14 * scale_factor)
axes[2].set_title(title_x2, fontsize=14 * scale_factor)
axes[2].tick_params(axis='both', labelsize=12 * scale_factor)

# 自动调整布局
plt.tight_layout()
plt.savefig("combined_heatmap_scatter_scaled.svg", format="svg", dpi=300)
plt.show()
