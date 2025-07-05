import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 设置页面标题和图标
st.set_page_config(
    page_title="数据可视化分析工具",
    page_icon="📊",
    layout="wide"
)

# 标题和说明
st.title("📊 交互式数据探索工具")
st.markdown("上传您的CSV文件或使用示例数据进行探索性分析")

# 创建侧边栏
with st.sidebar:
    st.header("数据设置")
    # 选择数据源
    data_source = st.radio("选择数据源:",
                           ("上传文件", "使用示例数据"))

    # 根据选择加载数据
    df = None
    if data_source == "上传文件":
        uploaded_file = st.file_uploader("上传CSV文件", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success("文件上传成功!")
    else:
        dataset = st.selectbox("选择示例数据集:",
                               ("鸢尾花数据集", "泰坦尼克号数据集", "钻石数据集"))

        if dataset == "鸢尾花数据集":
            df = sns.load_dataset('iris')
        elif dataset == "泰坦尼克号数据集":
            df = sns.load_dataset('titanic')
        else:  # 钻石数据集
            df = sns.load_dataset('diamonds')
            df = df.sample(1000)  # 取部分样本提高性能

# 主内容区
if df is None:
    st.info("请上传数据文件或选择示例数据集开始分析")
    st.stop()

# 显示数据
st.subheader("数据预览")
st.dataframe(df.head(), height=250)
st.caption(f"数据集形状: {df.shape[0]} 行 × {df.shape[1]} 列")

# 基本统计信息
st.subheader("数据统计摘要")
st.write(df.describe())

# 创建选项卡进行不同分析
tab1, tab2, tab3, tab4 = st.tabs(["📈 分布分析", "🔍 关系分析", "📋 数据透视", "⚙️ 数据转换"])

with tab1:
    st.subheader("变量分布分析")
    col1, col2 = st.columns(2)

    # 选择分析的列
    selected_column = col1.selectbox("选择分析列:", df.columns)

    # 图表类型选择
    chart_type = col2.selectbox("选择图表类型:",
                                ("直方图", "箱线图", "密度图", "饼图"))

    # 根据选择绘制图表
    if chart_type == "直方图":
        fig = px.histogram(df, x=selected_column, nbins=30)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_type == "箱线图":
        fig = px.box(df, y=selected_column)
        st.plotly_chart(fig, use_container_width=True)
    elif chart_type == "密度图":
        fig = px.density_contour(df, x=selected_column)
        st.plotly_chart(fig, use_container_width=True)
    else:  # 饼图
        if df[selected_column].nunique() > 10:
            st.warning("该列有太多唯一值，不适合饼图")
        else:
            fig = px.pie(df, names=selected_column)
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("变量关系分析")
    col1, col2, col3 = st.columns(3)

    x_axis = col1.selectbox("X轴变量:", df.columns, index=0)
    y_axis = col2.selectbox("Y轴变量:", df.columns, index=1)
    color_by = col3.selectbox("按颜色分组(可选):", [None] + list(df.columns))

    # 关系图类型选择
    rel_chart = st.radio("选择关系图类型:",
                         ("散点图", "折线图", "柱状图", "热力图"))

    if rel_chart == "散点图":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by)
        st.plotly_chart(fig, use_container_width=True)
    elif rel_chart == "折线图":
        fig = px.line(df, x=x_axis, y=y_axis, color=color_by)
        st.plotly_chart(fig, use_container_width=True)
    elif rel_chart == "柱状图":
        fig = px.bar(df, x=x_axis, y=y_axis, color=color_by)
        st.plotly_chart(fig, use_container_width=True)
    else:  # 热力图
        if df.select_dtypes(include=np.number).shape[1] < 2:
            st.error("需要至少两个数值列来创建热力图")
        else:
            corr = df.select_dtypes(include=np.number).corr()
            fig = px.imshow(corr, text_auto=True)
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("数据透视分析")
    col1, col2, col3 = st.columns(3)

    index_col = col1.selectbox("行索引:", df.columns)
    columns_col = col2.selectbox("列索引(可选):", [None] + list(df.columns))
    values_col = col3.selectbox("计算值:", df.select_dtypes(include=np.number).columns)

    agg_func = st.selectbox("聚合函数:",
                            ("平均值", "总和", "计数", "最大值", "最小值"))

    if st.button("生成透视表"):
        pivot_df = df.pivot_table(
            index=index_col,
            columns=columns_col,
            values=values_col,
            aggfunc=agg_func.lower().replace('值', '')
        )
        st.dataframe(pivot_df.style.background_gradient(cmap='Blues'), height=400)

with tab4:
    st.subheader("数据转换工具")
    col1, col2 = st.columns(2)

    # 缺失值处理
    with col1:
        st.markdown("#### 缺失值处理")
        if df.isnull().sum().sum() > 0:
            na_strategy = st.selectbox("处理策略:",
                                       ("不处理", "删除含缺失值的行", "填充均值", "填充中位数", "填充众数"))

            if na_strategy != "不处理":
                if na_strategy == "删除含缺失值的行":
                    df = df.dropna()
                else:
                    for col in df.columns:
                        if df[col].isnull().sum() > 0:
                            if na_strategy == "填充均值" and pd.api.types.is_numeric_dtype(df[col]):
                                df[col].fillna(df[col].mean(), inplace=True)
                            elif na_strategy == "填充中位数" and pd.api.types.is_numeric_dtype(df[col]):
                                df[col].fillna(df[col].median(), inplace=True)
                            elif na_strategy == "填充众数":
                                df[col].fillna(df[col].mode()[0], inplace=True)
            st.success(f"缺失值已处理! 剩余缺失值: {df.isnull().sum().sum()}")
        else:
            st.info("数据中没有缺失值")

    # 数据类型转换
    with col2:
        st.markdown("#### 数据类型转换")
        convert_col = st.selectbox("选择要转换的列:", df.columns)
        new_type = st.selectbox("转换为新类型:",
                                ("自动检测", "数值型", "字符串", "分类", "日期时间"))

        if st.button("应用转换"):
            if new_type == "数值型":
                df[convert_col] = pd.to_numeric(df[convert_col], errors='coerce')
            elif new_type == "字符串":
                df[convert_col] = df[convert_col].astype(str)
            elif new_type == "分类":
                df[convert_col] = df[convert_col].astype('category')
            elif new_type == "日期时间":
                df[convert_col] = pd.to_datetime(df[convert_col], errors='coerce')
            st.success(f"列 '{convert_col}' 已转换为 {new_type} 类型")

# 添加下载处理后的数据功能
st.sidebar.divider()
st.sidebar.markdown("### 导出数据")
if st.sidebar.download_button("下载处理后的数据",
                              df.to_csv(index=False).encode('utf-8'),
                              file_name="processed_data.csv",
                              mime="text/csv"):
    st.sidebar.success("数据已准备好下载!")

# 添加作者信息
st.sidebar.divider()
st.sidebar.caption("由 Streamlit 构建 | 数据可视化工具 v1.0")