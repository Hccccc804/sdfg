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
st.title("企业数字化转型指数查询与可视化")

# 数据加载函数
@st.cache_data

def load_data():
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
    # 确保股票代码为字符串格式，方便后续处理
    df['股票代码'] = df['股票代码'].astype(str)
    
    # 侧边栏 - 查询条件
    st.sidebar.header("查询条件")
    
    # 获取所有唯一的股票代码和年份
    available_stocks = sorted(df['股票代码'].unique())
    available_years = sorted(df['年份'].unique())
    
    # 处理企业名称中的空值，确保所有名称都是字符串类型
    df['企业名称'] = df['企业名称'].fillna('未知企业')
    df['企业名称'] = df['企业名称'].astype(str)
    
    # 获取股票代码与名称的映射
    stock_name_map = df.groupby('股票代码')['企业名称'].first().to_dict()
    
    # 设置默认值
    default_stock = "600000"  # 默认股票代码
    default_year = 1999  # 默认年份
    
    # 如果默认值不存在，使用可用值中的第一个
    if default_stock not in available_stocks:
        default_stock = available_stocks[0]
    if default_year not in available_years:
        default_year = available_years[0]
    
    # 股票代码搜索框
    stock_search = st.sidebar.text_input(
        "输入股票代码搜索",
        placeholder="例如: 600000",
        value=default_stock
    )
    
    # 股票名称搜索框
    name_search = st.sidebar.text_input(
        "输入企业名称搜索",
        placeholder="例如: 浦发银行"
    )
    
    # 根据搜索过滤股票
    filtered_stocks = []
    if name_search:
        filtered_stocks = [stock for stock in available_stocks if name_search in stock_name_map.get(stock, '')]
    elif stock_search:
        filtered_stocks = [stock for stock in available_stocks if stock_search in stock]
    else:
        filtered_stocks = available_stocks
    
    # 去重并排序
    filtered_stocks = sorted(list(set(filtered_stocks)))
    
    # 如果有匹配的股票代码，选择第一个；否则选择默认股票
    if filtered_stocks:
        selected_stock = filtered_stocks[0]
    else:
        selected_stock = default_stock
    
    # 显示当前选择的股票信息
    st.sidebar.write(f"**当前选择:** {selected_stock} ({stock_name_map.get(selected_stock, '未知企业')})")
    
    # 年份选择下拉框
    selected_year = st.sidebar.selectbox(
        "选择年份",
        options=available_years,
        index=available_years.index(default_year)
    )
    
    # 添加查询按钮
    st.sidebar.markdown("---")
    query_button = st.sidebar.button("查询数据", type="primary")
    
    # 数据筛选
    filtered_data = df[(df['股票代码'] == selected_stock) & (df['年份'] == selected_year)]
    
    # 显示企业基本信息
    if not filtered_data.empty:
        # 获取企业基本信息
        company_name = filtered_data['企业名称'].iloc[0]
        st.subheader(f"{company_name} ({selected_stock}) - {selected_year} 年数据")
        
        # 显示基本数据
        st.dataframe(filtered_data, width='stretch')
        
        # 数字化转型指数信息
        dt_index = filtered_data['数字化转型指数'].iloc[0]
        st.write(f"**数字化转型指数:** {dt_index:.2f}")
        
        # 统计排行与数据概览
        st.subheader("统计排行")
        col_rank1, col_rank2 = st.columns(2)
        
        with col_rank1:
            st.info("当年数字化转型指数Top 10")
            # 获取所选年份的Top 10企业
            year_top10 = df[df['年份'] == selected_year].nlargest(10, '数字化转型指数')
            year_top10['排名'] = range(1, 11)
            st.dataframe(year_top10[['排名', '股票代码', '企业名称', '数字化转型指数']], width='stretch')
        
        with col_rank2:
            st.success("该企业历年指数排名变化")
            # 获取该企业历年的排名
            company_all_years = df[df['股票代码'] == selected_stock].sort_values('年份')
            ranks = []
            for year in company_all_years['年份']:
                year_data = df[df['年份'] == year]
                year_rank = year_data[year_data['数字化转型指数'] >= company_all_years[company_all_years['年份'] == year]['数字化转型指数'].values[0]].shape[0]
                ranks.append(year_rank)
            company_all_years['年度排名'] = ranks
            st.dataframe(company_all_years[['年份', '数字化转型指数', '年度排名']], width='stretch')
        
        # 数据概览
        st.subheader("数据概览")
        col_overview1, col_overview2 = st.columns(2)
        
        with col_overview1:
            st.info("数据集统计")
            st.write(f"**数据总条数:** {len(df):,}")
            st.write(f"**包含企业数量:** {df['股票代码'].nunique():,}")
            st.write(f"**包含年份范围:** {df['年份'].min()} - {df['年份'].max()}")
            st.write(f"**年份跨度:** {df['年份'].max() - df['年份'].min() + 1} 年")
        
        with col_overview2:
            st.success("当前企业数据")
            st.write(f"**企业名称:** {company_name}")
            st.write(f"**股票代码:** {selected_stock}")
            st.write(f"**统计年份:** {selected_year}")
            st.write(f"**数字化转型指数:** {dt_index:.2f}")
            # 计算该企业在当年的排名
            current_year_rank = df[df['年份'] == selected_year][df['数字化转型指数'] >= dt_index].shape[0]
            total_companies = df[df['年份'] == selected_year].shape[0]
            st.write(f"**当年排名:** {current_year_rank}/{total_companies}")
            st.write(f"**排名百分比:** {((total_companies - current_year_rank + 1) / total_companies * 100):.1f}%")
    else:
        st.warning("未找到符合条件的数据")
        
    # 数字化转型指数分布图
    st.subheader("数字化转型指数分布图")
    
    # 直方图
    try:
        fig_hist = px.histogram(
            df,
            x='数字化转型指数',
            nbins=20,
            title="数字化转型指数整体分布直方图",
            labels={'数字化转型指数': '指数值', 'count': '企业数量'}
        )
        st.plotly_chart(fig_hist, width='stretch')
    except Exception as e:
        st.error(f"绘制直方图失败: {e}")
    
    # 折线图 - 按年份的平均数字化转型指数
    try:
        year_avg_index = df.groupby('年份')['数字化转型指数'].mean().reset_index()
        fig_line = px.line(
            year_avg_index,
            x='年份',
            y='数字化转型指数',
            title="历年平均数字化转型指数趋势",
            labels={'年份': '年份', '数字化转型指数': '平均数字化转型指数'},
            markers=True
        )
        st.plotly_chart(fig_line, width='stretch')
    except Exception as e:
        st.error(f"绘制折线图失败: {e}")
    
    # 数字化转型指数详细统计
    st.subheader("数字化转型指数详细统计")
    
    # 整体统计
    try:
        # 计算整体数字化转型指数统计
        st.info("整体数字化转型指数统计")
        overall_dt_stats = df['数字化转型指数'].describe()
        st.write(overall_dt_stats)
        
        # 按指数级别统计企业数量
        st.success("数字化转型指数级别分布")
        def get_index_level(index_value):
            if index_value >= 80:
                return "领先水平 (80-100)"
            elif index_value >= 60:
                return "良好水平 (60-79)"
            elif index_value >= 40:
                return "中等水平 (40-59)"
            elif index_value >= 20:
                return "起步水平 (20-39)"
            else:
                return "待提升 (<20)"
        
        df['指数级别'] = df['数字化转型指数'].apply(get_index_level)
        level_counts = df['指数级别'].value_counts().reset_index()
        level_counts.columns = ['指数级别', '企业数量']
        
        # 饼图展示指数级别分布
        fig_pie = px.pie(
            level_counts,
            values='企业数量',
            names='指数级别',
            title="数字化转型指数级别分布",
            hole=0.3
        )
        st.plotly_chart(fig_pie, width='stretch')
        
        # 技术维度与应用维度相关性
        st.warning("技术维度与应用维度分析")
        fig_scatter = px.scatter(
            df,
            x='技术维度',
            y='应用维度',
            title="技术维度与应用维度相关性",
            labels={'技术维度': '技术维度', '应用维度': '应用维度'},
            hover_data=['股票代码', '企业名称', '年份']
        )
        st.plotly_chart(fig_scatter, width='stretch')
        
        # 各年份指数分布箱线图
        st.info("各年份数字化转型指数分布")
        fig_box = px.box(
            df,
            x='年份',
            y='数字化转型指数',
            title="各年份数字化转型指数分布箱线图",
            labels={'年份': '年份', '数字化转型指数': '数字化转型指数'}
        )
        st.plotly_chart(fig_box, width='stretch')
        
    except Exception as e:
        st.error(f"统计分析失败: {e}")