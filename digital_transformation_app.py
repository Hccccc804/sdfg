import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 设置页面标题和布局
st.set_page_config(
    page_title="企业数字化转型指数查询",
    page_icon="📊",
    layout="wide"
)

# 页面标题
st.title("📊 企业数字化转型指数查询")

# 数据加载函数
@st.cache_data
def load_data():
    """加载数据文件"""
    try:
        df = pd.read_excel("两版合并后的年报数据_完整版.xlsx")
        return df
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        return None

# 加载数据
df = load_data()

if df is not None:
    # 数据预处理
    df['股票代码'] = df['股票代码'].astype(str)
    df['企业名称'] = df['企业名称'].fillna('未知企业')
    df['企业名称'] = df['企业名称'].astype(str)
    
    # 获取所有唯一的股票代码和年份
    available_stocks = sorted(df['股票代码'].unique())
    available_years = sorted(df['年份'].unique())
    
    # 获取股票代码与名称的映射
    stock_name_map = df.groupby('股票代码')['企业名称'].first().to_dict()
    
    # 侧边栏 - 查询条件
    st.sidebar.header("🔍 查询条件")
    
    # 设置默认值
    default_stock = "600003"  # 默认股票代码
    if default_stock not in available_stocks:
        default_stock = available_stocks[0]
    
    # 股票代码搜索框
    stock_search = st.sidebar.text_input(
        "输入股票代码搜索",
        placeholder="例如: 600003",
        value=default_stock
    )
    
    # 年份选择滑块
    selected_year = st.sidebar.slider(
        "选择年份",
        min_value=int(available_years[0]),
        max_value=int(available_years[-1]),
        value=int(1999),
        step=1
    )
    
    # 显示当前选择的股票信息
    if stock_search:
        st.sidebar.info(f"📌 **{stock_search}** ({stock_name_map.get(stock_search, '未知企业')})")
    
    # 数据筛选
    company_all_data = df[df['股票代码'] == stock_search].sort_values('年份')
    filtered_data = df[(df['股票代码'] == stock_search) & (df['年份'] == selected_year)]
    
    # 主内容区域
    st.header(f"📈 {stock_name_map.get(stock_search, '未知企业')} ({stock_search})")
    
    # ========== 数据概览 ==========
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("平均指数", f"{df['数字化转型指数'].mean():.2f}")
    with col2:
        st.metric("指数最大值", f"{df['数字化转型指数'].max():.2f}")
    with col3:
        st.metric("企业数量", f"{df['股票代码'].nunique():,}")
    with col4:
        st.metric("年份范围", f"{df['年份'].min()}-{df['年份'].max()}")
    
    # ========== 当前企业数据 ==========
    if not filtered_data.empty:
        company_name = filtered_data['企业名称'].iloc[0]
        dt_index = filtered_data['数字化转型指数'].iloc[0]
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("企业名称", company_name[:10])
        with c2:
            st.metric("当前年份", f"{selected_year}")
        with c3:
            st.metric("当前指数", f"{dt_index:.2f}")
        
        # 计算排名
        current_year_rank = df[df['年份'] == selected_year][df['数字化转型指数'] >= dt_index].shape[0]
        total_companies = df[df['年份'] == selected_year].shape[0]
        with c4:
            st.metric("当年排名", f"{current_year_rank}/{total_companies}")
    
    st.markdown("---")
    
    # ========== 数字化转型指数趋势 ==========
    st.subheader("📈 数字化转型指数趋势")
    
    if len(company_all_data) > 1:
        # 创建折线图
        fig_line = px.line(
            company_all_data,
            x='年份',
            y='数字化转型指数',
            title=f"历年数字化转型指数变化趋势",
            labels={'年份': '年份', '数字化转型指数': '数字化转型指数'},
            markers=True,
            line_shape='spline'
        )
        
        # 标记当前选择的年份
        current_point = company_all_data[company_all_data['年份'] == selected_year]
        if not current_point.empty:
            fig_line.add_trace(go.Scatter(
                x=current_point['年份'],
                y=current_point['数字化转型指数'],
                mode='markers+text',
                marker=dict(size=15, color='red', symbol='star'),
                text=[f'{dt_index:.2f}'],
                textposition='top center',
                name=f'{selected_year}年'
            ))
        
        fig_line.update_traces(
            line=dict(color='#1f77b4', width=4),
            marker=dict(size=10)
        )
        
        fig_line.update_layout(
            xaxis=dict(tickmode='linear', tick0=available_years[0], dtick=1),
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("该企业数据不足，无法绘制趋势图")
    
    st.markdown("---")
    
    # ========== 指数分布 ==========
    st.subheader("🥧 数字化转型指数分布")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        # 按指数区间划分
        bins = [0, 20, 40, 60, 80, 100]
        labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
        df['指数区间'] = pd.cut(df['数字化转型指数'], bins=bins, labels=labels, include_lowest=True)
        
        pie_data = df['指数区间'].value_counts().reset_index()
        pie_data.columns = ['指数区间', '企业数量']
        pie_data = pie_data.sort_values('指数区间')
        
        fig_pie = px.pie(
            pie_data,
            values='企业数量',
            names='指数区间',
            title='企业数字化转型指数区间分布',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_right:
        # 各年份平均指数柱形图
        year_avg_data = df.groupby('年份')['数字化转型指数'].mean().reset_index()
        
        fig_bar = px.bar(
            year_avg_data,
            x='年份',
            y='数字化转型指数',
            title='各年份平均数字化转型指数',
            color='数字化转型指数',
            color_continuous_scale='Viridis'
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # ========== 各企业历年平均指数排名 ==========
    st.subheader("📊 各企业历年平均指数排名")
    
    # 计算每家企业的平均指数
    company_avg = df.groupby('股票代码')['数字化转型指数'].mean().reset_index()
    company_avg.columns = ['股票代码', '平均指数']
    company_avg = company_avg.sort_values('平均指数', ascending=False).head(20)
    
    # 添加企业名称
    company_avg['企业名称'] = company_avg['股票代码'].map(stock_name_map)
    
    # 柱形图
    fig_company_bar = px.bar(
        company_avg,
        x='平均指数',
        y='股票代码',
        title='企业平均数字化转型指数排名 TOP20',
        color='平均指数',
        color_continuous_scale='RdYlGn',
        orientation='h'
    )
    fig_company_bar.update_layout(height=500)
    st.plotly_chart(fig_company_bar, use_container_width=True)

else:
    st.error("❌ 数据加载失败，请检查数据文件是否存在")

