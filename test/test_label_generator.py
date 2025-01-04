import unittest
import os
import sys
import pandas as pd
from PIL import Image
import shutil
from pathlib import Path

# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from label_generator import create_label, create_qr_code
from test.test_data_generator import generate_test_data

class TestLabelGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """测试开始前的设置"""
        cls.test_output_dir = "test/test_output"
        cls.test_data = generate_test_data(1000)
        
        # 创建测试输出目录
        if not os.path.exists(cls.test_output_dir):
            os.makedirs(cls.test_output_dir)

    @classmethod
    def tearDownClass(cls):
        """测试结束后的清理"""
        # 删除测试输出目录
        if os.path.exists(cls.test_output_dir):
            shutil.rmtree(cls.test_output_dir)

    def test_create_label_basic(self):
        """测试标签生成的基本功能"""
        # 测试第一条数据
        row_data = self.test_data.iloc[0]
        label = create_label(row_data)
        
        # 验证生成的标签是否为PIL Image对象
        self.assertIsInstance(label, Image.Image)
        
        # 验证图片尺寸（150mm x 100mm @ 300DPI）
        expected_width = int(150 * 300 / 25.4)  # 毫米转像素
        expected_height = int(100 * 300 / 25.4)
        self.assertEqual(label.size, (expected_width, expected_height))

    def test_create_label_batch(self):
        """测试批量生成标签"""
        success_count = 0
        error_count = 0
        errors = []

        for index, row in self.test_data.iterrows():
            try:
                label = create_label(row)
                # 保存标签用于视觉检查
                output_path = os.path.join(self.test_output_dir, f'test_label_{index}.png')
                label.save(output_path)
                success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Row {index}: {str(e)}")

        # 打印测试结果
        print(f"\n生成标签测试结果:")
        print(f"成功: {success_count}")
        print(f"失败: {error_count}")
        if errors:
            print("\n错误详情:")
            for error in errors[:10]:  # 只显示前10个错误
                print(error)

        # 验证至少95%的标签生成成功
        success_rate = success_count / len(self.test_data)
        self.assertGreaterEqual(success_rate, 0.95, 
                              f"标签生成成功率({success_rate:.2%})低于预期(95%)")

    def test_qr_code_generation(self):
        """测试二维码生成"""
        # 测试不同长度的文本
        test_texts = [
            "简单文本",
            "DD00000001*001*WL00000001*1000*2024-01-01*ZJ0001*Q235*MJ000001*普通*GC000001",
            "包含特殊字符!@#$%^&*()",
            "中文测试数据"
        ]

        for text in test_texts:
            qr_image = create_qr_code(text)
            self.assertIsInstance(qr_image, Image.Image)
            
            # 验证二维码尺寸
            self.assertEqual(qr_image.size[0], qr_image.size[1],
                           "二维码应该是正方形")

    def test_edge_cases(self):
        """测试边界情况"""
        # 创建包含边界情况的测试数据
        edge_cases = pd.DataFrame({
            '钢厂编码': ['', 'GC999999', None],
            '订单号': ['DD00000001', 'DD99999999', 'DD00000001'],
            '行号': ['001', '999', '001'],
            '物料编码': ['WL00000001', 'WL99999999', 'WL00000001'],
            '物料类别': ['钢材', None, '特殊材料'],
            '物料名称': ['测试物料', None, '特殊物料名称'*10],  # 测试超长名称
            '物料材质': ['Q235', None, '特殊材质'],
            '母卷号': ['MJ000001', None, 'MJ999999'],
            '子卷号': ['ZJ0001', None, 'ZJ9999'],
            '材料性能': ['普通', None, '特殊性能'],
            '重量kg': [0, 9999999.99, None],
            '生产日期': ['2024-01-01', None, '2024-12-31']
        })

        for index, row in edge_cases.iterrows():
            try:
                label = create_label(row)
                output_path = os.path.join(self.test_output_dir, f'edge_case_{index}.png')
                label.save(output_path)
            except Exception as e:
                self.fail(f"边界情况测试失败 (行 {index}): {str(e)}")

if __name__ == '__main__':
    unittest.main(verbosity=2) 