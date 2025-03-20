import streamlit as st
import pandas as pd
import plotly.express as px

# 加载所有矩阵文件，并更新分辨率
files = {
    "Original": "/home/loving/NEW_Progress/connectome/connectome_orgin.csv",
    "173x173 (86+87)": "/home/loving/NEW_Progress/connectome/connectome_86_87.csv",
    "390x390 (195+195)": "/home/loving/NEW_Progress/connectome/connectome_195_195.csv",
    "756x756 (381+375)": "/home/loving/NEW_Progress/connectome/connectome_381_375.csv",
}

matrices = {key: pd.read_csv(file, header=None) for key, file in files.items()}

# Streamlit 页面标题
st.title("连接矩阵交互可视化")

# 矩阵选择器
resolution = st.selectbox("选择矩阵分辨率:", list(files.keys()))

# 根据选择加载矩阵
matrix = matrices[resolution]

# 显示矩阵信息
st.write(f"当前显示矩阵: **{resolution}** 分辨率 ({matrix.shape[0]} x {matrix.shape[1]})")

# 渲染矩阵为热力图
fig = px.imshow(matrix, color_continuous_scale="Viridis", aspect="auto",
                labels={"x": "节点 X", "y": "节点 Y", "color": "值"})
st.plotly_chart(fig, use_container_width=True)
