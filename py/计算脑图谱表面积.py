import nibabel as nib
import numpy as np
import pandas as pd

# 读取 NIfTI 文件
nii_file = "/home/loving/NEW_Progress/brain_map/combined_381_375.nii.gz"
img = nib.load(nii_file)
data = img.get_fdata()

# 获取所有唯一的标签（排除背景 0）
labels = np.unique(data)
labels = labels[labels > 0]  # 去掉 0（假设 0 是背景）

# 获取体素尺寸（单位mm）
voxel_sizes = img.header.get_zooms()
voxel_area = voxel_sizes[0] * voxel_sizes[1]  # 计算体素面积（假设是2D面积）

# 计算每个脑区的面积
area_dict = {}
for label in labels:
    voxel_count = np.sum(data == label)  # 计算该标签的体素数
    area_dict[label] = voxel_count * voxel_area  # 计算面积

# 转换为 DataFrame 方便查看
area_df = pd.DataFrame(list(area_dict.items()), columns=["Region_Label", "Area_mm2"])
print(area_df)

# 保存到 CSV
area_df.to_csv("brain_region_areas.csv", index=False)
