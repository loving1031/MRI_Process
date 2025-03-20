import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = '/home/loving/wechat_file/xwechat_files/wxid_gpkbs5kjtl9h21_edcf/msg/file/2025-03/extracted_table.csv'
df = pd.read_csv(file_path, index_col=0)

# 转置df
df = df.T

plt.rcParams['figure.dpi'] = 300
plt.rcParams.update({'font.size': 6})  # 稍微调大一点字体

n_rows, n_cols = df.shape
cell_size = 0.5  # 稍微加大格子尺寸

# 更高的figsize，避免挤压
fig, ax = plt.subplots(figsize=(n_cols * cell_size, n_rows * cell_size * 1.3))

sns.heatmap(df, cmap='Blues', annot=False, square=True, 
            cbar_kws={"shrink": 0.5}, ax=ax)

# 更好地控制标题距离
ax.set_title('The correlation of cohan and transforming cohan', 
             fontsize=7, pad=10)

# 手动调整上下左右的空白区域
plt.subplots_adjust(top=0.85, bottom=0.15, left=0.2, right=0.85)

# 保存SVG
plt.savefig('heatmap_output_v3.svg', format='svg')

plt.show()

