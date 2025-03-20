import pandas as pd
import numpy as np

# 原始 CSV 文件路径
input_csv = "/home/loving/MRI_Process/hcp-mmp-b/fc_bipolar_hcp-mmp-b/symmetric_matrix.csv"
output_csv = "/home/loving/MRI_Process/hcp-mmp-b/fc_bipolar_hcp-mmp-b/cleaned_symmetric_matrix.csv"

try:
    # 读取 CSV 文件
    df = pd.read_csv(input_csv, header=None)  # 让 pandas 自己推断数据类型

    # 处理数据：确保所有值为数值，非数值的填充为 0
    def convert_to_number(x):
        if isinstance(x, (int, float)):  # 已经是数值，直接返回
            return x
        try:
            return float(x)  # 尝试转换为浮点数
        except ValueError:
            return 0  # 转换失败的（字符串）替换为 0

    df_cleaned = df.applymap(convert_to_number)

    # 保存清理后的数据
    df_cleaned.to_csv(output_csv, index=False, header=False)

    print(f"清理后的数据已保存到: {output_csv}")

except Exception as e:
    print(f"处理文件时出错：{e}")
