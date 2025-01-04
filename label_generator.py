import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class LabelGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("标签生成器")
        self.root.geometry("600x400")
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 文件选择部分
        ttk.Label(main_frame, text="Excel文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_path = tk.StringVar()
        self.file_entry = ttk.Entry(main_frame, textvariable=self.file_path, width=50)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="选择文件", command=self.select_file).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出目录选择
        ttk.Label(main_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar(value="output_labels")
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_path, width=50)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="选择目录", command=self.select_output_dir).grid(row=1, column=2, padx=5, pady=5)
        
        # 生成按钮
        ttk.Button(main_frame, text="生成标签", command=self.generate_labels).grid(row=2, column=1, pady=20)
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=3, pady=10)
        
        # 状态标签
        self.status_var = tk.StringVar(value="请选择Excel文件")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")],
            title="选择Excel文件"
        )
        if file_path:
            self.file_path.set(file_path)
            self.status_var.set("已选择文件: " + os.path.basename(file_path))

    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_path.set(dir_path)

    def generate_labels(self):
        if not self.file_path.get():
            messagebox.showerror("错误", "请先选择Excel文件！")
            return
        
        try:
            # 读取Excel文件，指定特定列的类型为字符串
            df = pd.read_excel(self.file_path.get(), dtype={
                '钢厂编码': str,
                '订单号': str,
                '行号': str,
                '物料编码': str,
                '母卷号': str,
                '子卷号': str
            })
            
            # 删除全空的行
            df = df.dropna(how='all')
            
            # 删除关键字段为空的行
            required_columns = ['订单号', '行号', '物料编码', '重量kg']
            df = df.dropna(subset=required_columns)
            
            # 处理数据中的小数点，同时保留前导零
            def remove_decimal(value):
                value_str = str(value)
                # 如果包含小数点，只保留整数部分
                if '.' in value_str:
                    value_str = value_str.split('.')[0]
                # 确保数字字符串长度保持不变（保留前导零）
                if value_str.isdigit():
                    return value_str.zfill(len(str(value)))
                return value_str

            # 对特定列应用去除小数点的处理
            decimal_columns = ['订单号', '行号', '物料名称']
            for col in decimal_columns:
                if col in df.columns:
                    df[col] = df[col].apply(remove_decimal)
            
            # 确保所有列都被当作字符串处理，但保留前导零
            for col in df.columns:
                if col not in ['重量kg']:  # 除了重量以外的列都保持原始格式
                    df[col] = df[col].astype(str)
            
            # 删除完全重复的行
            df = df.drop_duplicates(keep='first')
            
            # 重置索引
            df = df.reset_index(drop=True)
            
            total_rows = len(df)
            print(f"总行数: {total_rows}")
            print("处理的数据行：")
            print(df)  # 打印处理后的数据，方便调试
            
            # 创建输出目录
            output_dir = self.output_path.get()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 重置进度条
            self.progress['value'] = 0
            self.progress['maximum'] = total_rows
            
            # 生成标签
            for index, row in df.iterrows():
                label = create_label(row)
                output_path = os.path.join(output_dir, f'label_{index+1}.png')
                label.save(output_path)
                
                # 更新进度条和状态
                self.progress['value'] = index + 1
                self.status_var.set(f"正在生成: {index+1}/{total_rows}")
                self.root.update()
            
            self.status_var.set(f"完成！已生成 {total_rows} 个标签")
            messagebox.showinfo("成功", f"已成功生成 {total_rows} 个标签！\n保存在: {output_dir}")
            
        except Exception as e:
            messagebox.showerror("错误", f"生成过程中出现错误：\n{str(e)}")
            self.status_var.set("生成失败")
            print(f"Error details: {str(e)}")  # 打印详细错误信息

def create_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1
    )
    qr.add_data(text)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def create_label(row_data):
    # 设置DPI和尺寸转换
    DPI = 300  # 标准打印DPI
    MM_TO_INCH = 1 / 25.4  # 1英寸 = 25.4毫米
    
    # 计算像素尺寸（毫米转换为像素）
    width_mm = 150
    height_mm = 100
    width_pixels = int(width_mm * MM_TO_INCH * DPI)
    height_pixels = int(height_mm * MM_TO_INCH * DPI)
    
    # 创建空白图片
    image = Image.new('RGB', (width_pixels, height_pixels), 'white')
    draw = ImageDraw.Draw(image)
    
    # 设置图片DPI信息
    image.info['dpi'] = (DPI, DPI)
    
    # 加载字体
    try:
        # 使用小四号字（约40像素）
        font = ImageFont.truetype("simsun.ttc", 40)
    except:
        font = ImageFont.load_default()

    # 表格边距和单元格大小
    margin = 20
    cell_height = (height_pixels - 2 * margin) // 13  # 13行
    qr_width = width_pixels // 4  # 二维码宽度
    table_width = width_pixels - qr_width - margin  # 表格宽度
    
    # 绘制表格内容
    labels = ['供应商名称', '钢厂编码', '订单号', '物料类别', '行号', 
             '物料编码', '物料名称', '物料材质', '母卷号', 
             '子卷号', '材料性能', '重量', '生产日期']
    
    # 处理数据中的小数点，同时保留前导零
    def remove_decimal(value):
        value_str = str(value)
        if '.' in value_str:
            value_str = value_str.split('.')[0]
        # 确保数字字符串长度保持不变（保留前导零）
        if value_str.isdigit():
            return value_str.zfill(len(str(value)))
        return value_str

    # 处理特定字段的小数点
    row_data = row_data.copy()
    decimal_fields = ['订单号', '行号', '物料名称']
    for field in decimal_fields:
        if field in row_data:
            row_data[field] = remove_decimal(row_data[field])

    # 处理重量显示
    try:
        if pd.isna(row_data['重量kg']):
            weight_display = "0kg"
        else:
            weight_str = str(row_data['重量kg']).replace('kg', '').strip()
            weight_str = remove_decimal(weight_str)
            weight_display = f"{weight_str}kg"
    except:
        weight_display = "0kg"
        print(f"Warning: 无法处理重量值: {row_data['重量kg']}")

    values = ['无锡拳宁物资贸易有限公司', row_data['钢厂编码'], row_data['订单号'], 
             row_data['物料类别'], row_data['行号'], row_data['物料编码'], 
             row_data['物料名称'], row_data['物料材质'], row_data['母卷号'], 
             row_data['子卷号'], row_data['材料性能'], weight_display, 
             row_data['生产日期']]

    # 绘制表格和文字
    current_y = margin
    for label, value in zip(labels, values):
        # 绘制边框
        draw.rectangle([margin, current_y, table_width, current_y+cell_height], 
                      outline='black')
        
        # 绘制分隔线
        mid_x = margin + (table_width - margin) // 2
        draw.line([mid_x, current_y, mid_x, current_y+cell_height], 
                 fill='black')
        
        # 计算文字大小
        label_bbox = draw.textbbox((0, 0), label, font=font)
        value_bbox = draw.textbbox((0, 0), str(value), font=font)
        
        # 计算文字位置（水平和垂直居中）
        label_width = label_bbox[2] - label_bbox[0]
        label_height = label_bbox[3] - label_bbox[1]
        value_width = value_bbox[2] - value_bbox[0]
        value_height = value_bbox[3] - value_bbox[1]
        
        # 左侧文字位置
        label_x = margin + (mid_x - margin - label_width) // 2
        label_y = current_y + (cell_height - label_height) // 2
        
        # 右侧文字位置
        value_x = mid_x + (table_width - mid_x - value_width) // 2
        value_y = current_y + (cell_height - value_height) // 2
        
        # 写入文字
        draw.text((label_x, label_y), label, font=font, fill='black')
        draw.text((value_x, value_y), str(value), font=font, fill='black')
        
        current_y += cell_height

    # 生成二维码文本
    try:
        # 处理重量
        if pd.isna(row_data['重量kg']):
            weight = "0"
        else:
            weight_str = str(row_data['重量kg']).replace('kg', '').strip()
            weight = remove_decimal(weight_str)

        # 处理日期格式（只保留年月日）
        if pd.isna(row_data['生产日期']) or str(row_data['生产日期']) == 'NaT':
            date = ''
        else:
            try:
                # 如果日期中包含时分秒，只保留年月日
                date_str = str(row_data['生产日期'])
                if ' ' in date_str:  # 如果包含时间部分
                    date_str = date_str.split(' ')[0]  # 只取日期部分
                if '-' in date_str:  # 如果已经是yyyy-mm-dd格式
                    date = date_str
                else:
                    # 尝试转换其他格式为yyyy-mm-dd
                    date = pd.to_datetime(date_str).strftime('%Y-%m-%d')
            except:
                date = str(row_data['生产日期'])

        # 按指定格式生成二维码文本
        qr_text = (f"{row_data['订单号']}*{row_data['行号']}*{row_data['物料编码']}*"
                  f"{weight}*{date}*{row_data['子卷号']}*"
                  f"{row_data['物料材质']}*{row_data['母卷号']}*{row_data['材料性能']}*"
                  f"{row_data['钢厂编码']}")
    except Exception as e:
        print(f"Error creating QR text: {str(e)}")
        print(f"Row data: {row_data}")
        raise

    # 生成两个相同的二维码并粘贴到图片上
    qr_img = create_qr_code(qr_text)
    qr_size = height_pixels // 3  # 二维码大小
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # 计算二维码垂直位置
    total_height = height_pixels - 2 * margin  # 可用总高度
    gap = (total_height - 2 * qr_size) // 3  # 三等分间隔（顶部间隔、中间间隔、底部间隔）
    
    # 计算二维码区域的边框位置
    qr_area_left = table_width  # 从表格右边界开始
    qr_area_top = margin
    qr_area_right = width_pixels - margin
    qr_area_bottom = current_y  # 使用表格的当前高度作为底部边界
    
    # 绘制二维码区域的边框（确保与表格对齐）
    draw.line([qr_area_left, qr_area_top, qr_area_right, qr_area_top], fill='black', width=1)  # 顶线
    draw.line([qr_area_right, qr_area_top, qr_area_right, qr_area_bottom], fill='black', width=1)  # 右线
    draw.line([qr_area_left, qr_area_bottom, qr_area_right, qr_area_bottom], fill='black', width=1)  # 底线
    
    # 重新绘制表格右边线（确保与二维码区域边框完全对齐）
    draw.line([table_width, margin, table_width, current_y], fill='black', width=1)
    
    # 粘贴二维码
    first_qr_y = margin + gap
    image.paste(qr_img, (table_width + margin, first_qr_y))
    
    second_qr_y = first_qr_y + qr_size + gap
    image.paste(qr_img, (table_width + margin, second_qr_y))

    return image

def main():
    root = tk.Tk()
    app = LabelGeneratorApp(root)
    root.mainloop()

if __name__ == '__main__':
    main() 