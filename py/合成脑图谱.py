import nibabel as nib
import numpy as np
import os

# 设置标签文件夹路径
labelled_dir = '/home/loving/NEW_Progress/lh_rh_18238_18602_convertnii_labled'

# 获取该目录下所有 .nii.gz 文件
nii_files = [f for f in os.listdir(labelled_dir) if f.endswith('.nii.gz')]

# 初始化合并后的数据数组
combined_data = None

# 遍历每个 .nii.gz 文件并合并
for nii_file in nii_files:
    # 构造文件路径
    file_path = os.path.join(labelled_dir, nii_file)
    
    # 加载 NIfTI 文件
    img = nib.load(file_path)
    data = img.get_fdata()

    # 如果是第一个文件，初始化合并数据
    if combined_data is None:
        combined_data = data
    else:
        # 合并标签数据（使用最大值合并，避免覆盖）
        combined_data = np.maximum(combined_data, data)

    print(f"已合并文件：{nii_file}")

# 创建新的 NIfTI 图像
combined_img = nib.Nifti1Image(combined_data, img.affine)

# 保存为新的文件
output_path = '/home/loving/NEW_Progress/brain_map/combined_18238_18602.nii.gz'
nib.save(combined_img, output_path)

print(f"合成完成！保存为：{output_path}")
