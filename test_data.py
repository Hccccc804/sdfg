import pandas as pd

# 测试数据加载
print("测试数据加载...")
try:
    df = pd.read_excel("两版合并后的年报数据_完整版.xlsx")
    print(f"数据加载成功，共 {len(df)} 条记录")
    
    # 测试数据预处理
    df['股票代码'] = df['股票代码'].astype(str)
    df['企业名称'] = df['企业名称'].fillna('未知企业')
    df['企业名称'] = df['企业名称'].astype(str)
    
    print(f"数据预处理完成")
    
    # 测试默认值设置
    default_stock = "600000"
    default_year = 1999
    
    available_stocks = sorted(df['股票代码'].unique())
    available_years = sorted(df['年份'].unique())
    
    print(f"可用股票代码数量: {len(available_stocks)}")
    print(f"可用年份: {available_years}")
    
    if default_stock in available_stocks:
        print(f"默认股票代码 {default_stock} 存在")
    else:
        print(f"默认股票代码 {default_stock} 不存在")
    
    if default_year in available_years:
        print(f"默认年份 {default_year} 存在")
    else:
        print(f"默认年份 {default_year} 不存在，使用最小年份 {available_years[0]}")
    
    # 测试数据筛选
    filtered_data = df[(df['股票代码'] == default_stock) & (df['年份'] == default_year)]
    print(f"筛选后的数据数量: {len(filtered_data)}")
    
    if not filtered_data.empty:
        print("筛选后的数据:")
        print(filtered_data.head())
    else:
        print("没有找到符合条件的数据")
        
    # 测试企业名称映射
    stock_name_map = df.groupby('股票代码')['企业名称'].first().to_dict()
    if default_stock in stock_name_map:
        print(f"股票代码 {default_stock} 对应的企业名称: {stock_name_map[default_stock]}")
    
    print("测试完成！")
    
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()