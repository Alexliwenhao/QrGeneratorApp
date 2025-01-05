from PIL import Image
import os

def convert_png_to_ico(png_path, ico_path):
    img = Image.open(png_path)
    # 确保图片是正方形
    size = max(img.size)
    new_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    new_img.paste(img, ((size - img.size[0]) // 2, (size - img.size[1]) // 2))
    
    # 保存多个尺寸的图标
    icon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    new_img.save(ico_path, format='ICO', sizes=icon_sizes)

if __name__ == '__main__':
    png_path = r"D:\vscode\python\qr\二维码.png"
    ico_path = "app.ico"
    convert_png_to_ico(png_path, ico_path)
    print(f"Icon created at: {os.path.abspath(ico_path)}") 