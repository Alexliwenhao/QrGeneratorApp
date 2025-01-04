import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_material_performance():
    """生成材料性能数据，格式如：350-420-16%"""
    # 生成第一个数值（通常是屈服强度）
    first = random.choice([235, 275, 315, 345, 350, 390, 420])
    # 生成第二个数值（通常是抗拉强度，比第一个值大50-100）
    second = first + random.randint(50, 100)
    # 生成延伸率（通常在10-30%之间）
    extension = random.randint(10, 30)
    return f"{first}-{second}-{extension}%"

def generate_test_data(num_records=1000):
    # 生成基础数据
    data = {
        '供应商名称': ['无锡拳宁物资贸易有限公司'] * num_records,
        '钢厂编码': [f'GC{str(i).zfill(6)}' for i in range(num_records)],
        '订单号': [f'DD{str(i).zfill(8)}' for i in range(num_records)],
        '物料类别': ['钢材', '铁材', '铝材', '铜材'] * ((num_records + 3) // 4),
        '行号': [str(i).zfill(3) for i in range(num_records)],
        '物料编码': [f'WL{str(i).zfill(8)}' for i in range(num_records)],
        '物料名称': [f'测试物料{i}' for i in range(num_records)],
        '物料材质': ['Q235', 'Q345', 'Q390', '304'] * ((num_records + 3) // 4),
        '母卷号': [f'MJ{str(i).zfill(6)}' for i in range(num_records)],
        '子卷号': [f'ZJ{str(i).zfill(4)}' for i in range(num_records)],
        '材料性能': [generate_material_performance() for _ in range(num_records)],
        '重量kg': [round(random.uniform(100, 5000), 2) for _ in range(num_records)],
        '生产日期': [(datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d') 
                  for _ in range(num_records)]
    }
    
    # 确保所有列的长度一致
    for key, value in data.items():
        if len(value) > num_records:
            data[key] = value[:num_records]
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 验证数据完整性
    required_columns = ['订单号', '行号', '物料编码', '重量kg', '材料性能', '钢厂编码', '母卷号', '子卷号']
    for column in required_columns:
        if df[column].isnull().any():
            print(f"警告：{column} 列存在空值！")
            # 填充空值
            if column == '重量kg':
                df[column] = df[column].fillna(0)
            elif column == '材料性能':
                df[column] = df[column].fillna('350-420-16%')
            else:
                df[column] = df[column].fillna(f'DEFAULT_{column}')
    
    # 数据验证
    print("\n数据验证:")
    for column in df.columns:
        null_count = df[column].isnull().sum()
        if null_count > 0:
            print(f"{column}: {null_count} 个空值")
    
    return df

def save_test_data():
    """生成测试数据并保存到Excel文件"""
    # 确保目录存在
    os.makedirs('test/test_data', exist_ok=True)
    
    df = generate_test_data(1000)
    
    # 最终验证
    print("\n最终数据验证:")
    print("数据形状:", df.shape)
    print("\n空值统计:")
    print(df.isnull().sum())
    
    # 保存数据
    df.to_excel('test/test_data/test_labels.xlsx', index=False)
    print(f"\n已生成测试数据，共 {len(df)} 条记录")
    print("\n数据预览:")
    print(df.head())
    
    return df

if __name__ == '__main__':
    save_test_data() 