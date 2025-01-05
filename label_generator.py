import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import sys

class LabelGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("攀宁二维码标签生成器")
        
        # 添加授权检查
        self.is_licensed = self.check_license()
        
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
        
        # 打开授权文件按钮（放在输出目录标签下方）
        self.license_button = ttk.Button(main_frame, text="打开授权文件", 
                                       command=self.open_license_file)
        self.license_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        
        # 添加授权状态显示
        self.license_status = ttk.Label(main_frame, text="未授权版本", foreground='red')
        self.license_status.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        # 初始检查授权状态
        self.update_license_status()
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=1, pady=10)  # 行号改为3
        
        # 生成按钮和停止按钮
        self.generate_button = ttk.Button(button_frame, text="生成标签", command=self.generate_labels)
        self.generate_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="停止生成", command=self.stop_generation, state='disabled')
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # 添加停止标志
        self.stop_flag = False
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, pady=5)  # 行号改为4
        
        # 状态标签
        self.status_var = tk.StringVar(value="请选择Excel文件")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)  # 行号改为5

        # 添加日志框
        log_frame = ttk.LabelFrame(main_frame, text="日志输出", padding="5")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)  # 行号改为6
        
        # 创建日志文本框和滚动条
        self.log_text = tk.Text(log_frame, height=8, width=60)  # 减小高度和宽度
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # 放置日志文本框和滚动条
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S), pady=5)

        # 配置网格权重
        main_frame.columnconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        
        # 设置窗口大小为自适应
        self.root.update()
        # 获取窗口需要的最小尺寸
        width = main_frame.winfo_reqwidth() + 20
        height = main_frame.winfo_reqheight() + 20
        # 设置窗口尺寸和最小尺寸
        self.root.geometry(f"{width}x{height}")
        self.root.minsize(width, height)
        # 禁止调整窗口大小
        self.root.resizable(False, False)

        # 将窗口居中显示
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"+{x}+{y}")

    def log_message(self, message):
        """添加日志消息到日志框"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)  # 滚动到最新消息
        self.root.update()

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

    def stop_generation(self):
        """停止生成标签"""
        self.stop_flag = True
        self.log_message("\n用户停止了生成过程")
        self.status_var.set("已停止生成")
        self.stop_button.configure(state='disabled')
        self.generate_button.configure(state='normal')

    def generate_labels(self):
        if not self.file_path.get():
            messagebox.showerror("错误", "请先选择Excel文件！")
            return
        
        try:
            # 重置停止标志
            self.stop_flag = False
            # 更新按钮状态
            self.generate_button.configure(state='disabled')
            self.stop_button.configure(state='normal')
            
            # 清空日志框
            self.log_text.delete(1.0, tk.END)
            self.log_message("开始处理数据...")
            
            # 读取Excel文件
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
            
            # 检查授权限制
            total_rows = len(df)
            if not self.is_licensed and total_rows > 10:
                self.log_message("\n⚠️ 未授权版本限制：")
                self.log_message("- 仅支持生成前10个标签")
                self.log_message("- 如需解除限制，请联系管理员获取授权密钥")
                self.log_message("- 将授权密钥保存在程序目录下的license.txt文件中")
                self.log_message(f"\n当前数据共 {total_rows} 行，将只处理前10行\n")
                df = df.head(10)
            
            # 格式化生产日期（只保留年月日）
            if '生产日期' in df.columns:
                df['生产日期'] = pd.to_datetime(df['生产日期']).dt.strftime('%Y-%m-%d')
            
            # 定义所有列和必填列
            all_columns = ['钢厂编码', '订单号', '物料类别', '行号', 
                          '物料编码', '物料名称', '物料材质', '母卷号', 
                          '子卷号', '材料性能', '重量kg', '生产日期']
            required_columns = ['订单号', '行号', '物料编码', '重量kg', '材料性能', 
                               '钢厂编码', '母卷号', '子卷号']
            
            # 创建输出目录
            output_dir = self.output_path.get()
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 重置进度条
            total_rows = len(df)
            self.progress['value'] = 0
            self.progress['maximum'] = total_rows
            
            # 生成标签
            success_count = 0
            for index, row in df.iterrows():
                # 检查是否需要停止
                if self.stop_flag:
                    self.log_message("\n生成过程被用户中止")
                    self.status_var.set("生成已中止")
                    break
                
                # 检查当前行的空值
                empty_fields = []
                warning_fields = []
                for column in all_columns:
                    if column not in row.index:
                        warning_fields.append(f"{column}(列不存在)")
                    elif pd.isna(row[column]) or str(row[column]).strip() == '':
                        if column in required_columns:
                            empty_fields.append(column)
                        else:
                            warning_fields.append(column)
                
                # 如果有空值，输出到日志
                if empty_fields or warning_fields:
                    self.log_message(f"\n第 {index + 1} 行数据问题:")
                    if empty_fields:
                        self.log_message(f"必填字段为空: {', '.join(empty_fields)}")
                    if warning_fields:
                        self.log_message(f"非必填字段为空: {', '.join(warning_fields)}")
                    self.log_message("当前行数据:")
                    for col in all_columns:
                        if col in row.index:
                            value = row[col]
                            if pd.isna(value):
                                value = "<空>"
                            self.log_message(f"  {col}: {value}")
                    self.log_message("")
                
                # 如果必填字段有空值，跳过此行
                if empty_fields:
                    self.log_message(f"跳过第 {index + 1} 行（存在空必填字段）\n")
                    continue
                
                try:
                    label = create_label(row)
                    output_path = os.path.join(output_dir, f'label_{index+1}.png')
                    label.save(output_path)
                    success_count += 1
                except Exception as e:
                    self.log_message(f"\n生成第 {index + 1} 个标签时出错:")
                    self.log_message(f"错误信息: {str(e)}")
                    self.log_message(f"数据: {dict(row)}\n")
                
                # 更新进度条和状态
                self.progress['value'] = index + 1
                self.status_var.set(f"正在生成: {index+1}/{total_rows}")
                self.root.update()
            
            if not self.stop_flag:
                self.status_var.set(f"完成！成功生成 {success_count} 个标签")
                self.log_message(f"\n标签生成完成！")
                self.log_message(f"总数据行数: {total_rows}")
                self.log_message(f"成功生成: {success_count}")
                if not self.is_licensed:
                    self.log_message(f"（未授权版本限制生成10个）")
                self.log_message(f"跳过行数: {total_rows - success_count}")
                self.log_message(f"保存位置: {output_dir}")
                messagebox.showinfo("成功", f"已成功生成 {success_count} 个标签！\n保存在: {output_dir}")
            
        except Exception as e:
            error_msg = f"生成过程中出现错误：\n{str(e)}"
            self.log_message(f"\n错误: {error_msg}")
            messagebox.showerror("错误", error_msg)
            self.status_var.set("生成失败")
        finally:
            # 恢复按钮状态
            self.generate_button.configure(state='normal')
            self.stop_button.configure(state='disabled')
            # 重置停止标志
            self.stop_flag = False

    def check_license(self):
        """检查授权状态"""
        try:
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
                
            license_path = os.path.join(application_path, 'license.txt')
            if os.path.exists(license_path):
                with open(license_path, 'r') as f:
                    license_key = f.read().strip()
                    return license_key == '5d9ecfb1-8d59-4296-883a-4dd7caf9d377'
        except:
            pass
        return False

    def update_license_status(self):
        """更新授权状态显示"""
        if self.check_license():
            self.license_status.config(text="已授权版本", foreground='green')
            self.is_licensed = True
        else:
            self.license_status.config(text="未授权版本", foreground='red')
            self.is_licensed = False

    def open_license_file(self):
        """打开授权文件"""
        try:
            # 获取程序运行目录
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
            
            # 授权文件路径
            license_path = os.path.join(application_path, 'license.txt')
            
            # 如果文件不存在，创建一个空文件
            if not os.path.exists(license_path):
                with open(license_path, 'w', encoding='utf-8') as f:
                    f.write('# 请在此处输入授权码，输入后保存即可实时生效\n')
            
            # 记录文件的最后修改时间
            last_modified = os.path.getmtime(license_path) if os.path.exists(license_path) else 0
            
            # 使用系统默认程序打开文件
            if sys.platform == 'win32':
                os.startfile(license_path)
            else:
                import subprocess
                subprocess.run(['xdg-open', license_path])
            
            self.log_message("已打开授权文件，请输入授权码并保存。")
            
            # 启动一个检查文件变化的循环
            def check_file_change():
                try:
                    current_modified = os.path.getmtime(license_path)
                    if current_modified > last_modified:
                        self.update_license_status()
                        self.log_message("检测到授权文件已更新，授权状态已更新。")
                        return  # 如果文件已更新，停止检查
                    self.root.after(1000, check_file_change)  # 每秒检查一次
                except Exception as e:
                    print(f"检查文件变化时出错: {e}")
            
            self.root.after(1000, check_file_change)  # 开始检查循环
            
        except Exception as e:
            messagebox.showerror("错误", f"无法打开授权文件：{str(e)}")

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

def format_decimal(value):
    """格式化小数，如果小数部分为0则不显示"""
    try:
        # 先格式化为3位小数
        formatted = f"{float(value):.3f}"
        # 移除末尾的0和不必要的小数点
        formatted = formatted.rstrip('0').rstrip('.')
        return formatted
    except:
        return str(value)

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
        # 尝试使用系统宋体
        font = ImageFont.truetype("simsun.ttc", 40)
    except:
        try:
            # 备选：尝试使用系统默认中文字体
            font = ImageFont.truetype("simhei.ttf", 40)
        except:
            # 如果都失败，使用默认字体
            font = ImageFont.load_default()
            print("Warning: 无法加载中文字体，使用默认字体")

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

    # 处理重量显示
    try:
        if pd.isna(row_data['重量kg']):
            weight_display = "0kg"
        else:
            weight_value = float(str(row_data['重量kg']).replace('kg', '').strip())
            weight_display = f"{format_decimal(weight_value)}kg"
    except:
        weight_display = "0kg"
        print(f"Warning: 无法处理重量值: {row_data['重量kg']}")

    # 生成二维码文本
    try:
        # 处理重量
        if pd.isna(row_data['重量kg']):
            weight = "0"
        else:
            weight_value = float(str(row_data['重量kg']).replace('kg', '').strip())
            weight = format_decimal(weight_value)

        # 处理日期格式
        if pd.isna(row_data['生产日期']) or str(row_data['生产日期']) == 'NaT':
            date = ''
        else:
            date_str = str(row_data['生产日期'])
            if ' ' in date_str:
                date_str = date_str.split(' ')[0]
            date = date_str

        # 按指定格式生成二维码文本，物料名称保持原样
        qr_text = (f"{row_data['订单号']}*{row_data['行号']}*{row_data['物料编码']}*"
                  f"{weight}*{date}*{row_data['子卷号']}*"
                  f"{row_data['物料材质']}*{row_data['母卷号']}*{row_data['材料性能']}*"
                  f"{row_data['钢厂编码']}")

    except Exception as e:
        print(f"Error creating QR text: {str(e)}")
        print(f"Row data: {row_data}")
        raise

    # 准备表格数据
    values = [
        '无锡攀宁物资贸易有限公司',  # 固定的供应商名称
        row_data['钢厂编码'], 
        row_data['订单号'],
        row_data['物料类别'], 
        row_data['行号'], 
        row_data['物料编码'],
        str(row_data['物料名称']).strip(),  # 只去除首尾空格，保持原格式
        row_data['物料材质'], 
        row_data['母卷号'],
        row_data['子卷号'], 
        row_data['材料性能'], 
        weight_display,
        row_data['生产日期']
    ]

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