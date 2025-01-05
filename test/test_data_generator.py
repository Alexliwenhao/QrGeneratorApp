import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def format_decimal(value):
    """格式化小数，如果小数部分为0则不显示"""
    if isinstance(value, (int, float)):
        # 先格式化为3位小数
        formatted = f"{float(value):.3f}"
        # 移除末尾的0和不必要的小数点
        formatted = formatted.rstrip('0').rstrip('.')
        return formatted
    return str(value)

def generate_test_data(num_records=1000):
    # 基础数据模板
    base_data = {
        '钢厂编码': '07',
        '订单号': '1000917199',
        '物料类别': '钢卷',
        '行号': '0020',
        '物料编码': 'N046001-002194-000',
        '物料名称': '锌铝镁卷-90*2.1',
        '物料材质': 'S350GD-ZM275',
        '材料性能': '446-579-17.5',
        '生产日期': '2024-12-30'
    }
    
    # 生成数据列表
    data = []
    mother_coils = [f'24E{str(i).zfill(8)}' for i in range(num_records // 6 + 1)]
    
    # 基础物料名称模板（使用完全匹配的格式）
    base_names = [
        '锌铝镁卷-90*2.1',
        '锌铝镁卷-90*2.12',
        '锌铝镁卷-90*2.123',
        '锌铝镁卷-90*0.1',
        '锌铝镁卷-90*0.12',
        '锌铝镁卷-90*0.123'
    ]
    
    # 基础重量模板（带小数点）
    base_weights = [
        1657.123,  # 三位小数
        1657.45,   # 两位小数
        1658.7,    # 一位小数
        1658.0,    # 整数（带小数点）
        3900.789,  # 三位小数
        2560       # 整数
    ]
    
    # 生成带随机小数的重量列表
    weights = []
    for base_weight in base_weights:
        if isinstance(base_weight, int):
            weights.append(format_decimal(base_weight))
        else:
            # 在基础重量上增加随机小数（最多3位）
            decimal = random.randint(0, 999) / 1000
            weight = round(base_weight + decimal, 3)
            weights.append(format_decimal(weight))
    
    for i in range(num_records):
        mother_coil = mother_coils[i // 6]  # 每6个子卷使用一个母卷号
        row = base_data.copy()
        row['母卷号'] = mother_coil
        row['子卷号'] = f'{mother_coil}-{str((i % 6) + 1).zfill(2)}'
        
        # 设置物料名称（按照实际格式循环）
        row['物料名称'] = str(base_names[i % 6])  # 确保是字符串类型
        
        # 设置重量（带小数点）
        row['重量kg'] = weights[i % 6]
        
        data.append(row)
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 设置列的顺序
    columns = ['钢厂编码', '订单号', '物料类别', '行号', '物料编码', '物料名称', 
              '物料材质', '母卷号', '子卷号', '材料性能', '重量kg', '生产日期']
    df = df[columns]
    
    # 确保物料名称列是字符串类型
    df['物料名称'] = df['物料名称'].astype(str)
    
    return df

def save_test_data():
    """生成测试数据并保存到Excel文件"""
    # 确保目录存在
    os.makedirs('test/test_data', exist_ok=True)
    
    df = generate_test_data(1000)  # 生成1000条测试数据
    
    # 在保存前检查数据
    print("\n物料名称示例:")
    print(df['物料名称'].head(6).to_string())
    
    # 使用特定的Excel写入选项
    with pd.ExcelWriter('test/test_data/test_labels.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    print(f"\n已生成测试数据，共 {len(df)} 条记录")
    print("\n数据预览（前6条）:")
    print(df.head(6))
    print("\n数据统计:")
    print(f"总记录数: {len(df)}")
    print(f"母卷数量: {len(df['母卷号'].unique())}")
    return df

if __name__ == '__main__':
    save_test_data() 