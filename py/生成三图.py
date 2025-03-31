import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
file_y = "/home/loving/桌面/results.csv"
df_y = pd.read_csv(file_y, index_col=0)

# 转换数据为数值型，非数值转换为 NaN
df_y = df_y.apply(pd.to_numeric, errors='coerce')

# 放大整体图形，保持等比例布局
scale_factor = 1.1  # 可以根据需要调整
base_figsize = (8, 6)
figsize = (base_figsize[0] * scale_factor, base_figsize[1] * scale_factor)

fig, ax = plt.subplots(figsize=figsize)

# 使用蓝色渐变绘制热图
sns.heatmap(df_y, annot=False, cmap="Blues", linewidths=0.1, ax=ax, square=True, cbar_kws={'shrink': 0.3})
ax.set_title("", fontsize=16 * scale_factor)
ax.tick_params(axis='both', labelsize=12 * scale_factor)

# 自动调整布局
plt.tight_layout()
plt.savefig("heatmap_blue.svg", format="svg", dpi=300)
plt.show()
