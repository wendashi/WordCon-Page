#!/usr/bin/env python3
"""
PDF to JPG Converter Script
批量将PDF文件转换为JPG格式
"""

import os
import sys
import fitz  # PyMuPDF
from PIL import Image
import argparse

def convert_pdf_to_jpg(pdf_path, output_dir, dpi=300, quality=95):
    """
    将单个PDF文件转换为JPG格式
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
        dpi: 分辨率（默认300）
        quality: JPG质量（默认95）
    """
    try:
        # 打开PDF文件
        pdf_document = fitz.open(pdf_path)
        
        # 获取文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        # 转换每一页
        for page_num in range(len(pdf_document)):
            # 获取页面
            page = pdf_document.load_page(page_num)
            
            # 设置缩放矩阵（根据DPI调整）
            mat = fitz.Matrix(dpi/72, dpi/72)
            
            # 渲染页面为图片
            pix = page.get_pixmap(matrix=mat)
            
            # 转换为PIL Image
            img_data = pix.tobytes("ppm")
            img = Image.open(io.BytesIO(img_data))
            
            # 生成输出文件名
            if len(pdf_document) == 1:
                output_filename = f"{base_name}.jpg"
            else:
                output_filename = f"{base_name}_page_{page_num + 1}.jpg"
            
            output_path = os.path.join(output_dir, output_filename)
            
            # 保存为JPG
            img.save(output_path, "JPEG", quality=quality, optimize=True)
            print(f"✓ 已转换: {pdf_path} -> {output_path}")
        
        pdf_document.close()
        return True
        
    except Exception as e:
        print(f"✗ 转换失败 {pdf_path}: {str(e)}")
        return False

def batch_convert_pdfs(pdf_dir, output_dir, dpi=300, quality=95):
    """
    批量转换PDF文件
    
    Args:
        pdf_dir: PDF文件目录
        output_dir: 输出目录
        dpi: 分辨率
        quality: JPG质量
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取所有PDF文件
    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("未找到PDF文件")
        return
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    print(f"输出目录: {output_dir}")
    print(f"DPI: {dpi}, 质量: {quality}")
    print("-" * 50)
    
    success_count = 0
    total_count = len(pdf_files)
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        if convert_pdf_to_jpg(pdf_path, output_dir, dpi, quality):
            success_count += 1
    
    print("-" * 50)
    print(f"转换完成: {success_count}/{total_count} 个文件成功转换")

def main():
    parser = argparse.ArgumentParser(description='批量转换PDF文件为JPG格式')
    parser.add_argument('--pdf_dir', default='/Users/wendashi/Desktop/proj-page/pdfs',
                       help='PDF文件目录路径')
    parser.add_argument('--output_dir', default='./static/images',
                       help='输出目录路径')
    parser.add_argument('--dpi', type=int, default=300,
                       help='输出图片DPI (默认: 300)')
    parser.add_argument('--quality', type=int, default=95,
                       help='JPG质量 (默认: 95)')
    
    args = parser.parse_args()
    
    # 检查PDF目录是否存在
    if not os.path.exists(args.pdf_dir):
        print(f"错误: PDF目录不存在: {args.pdf_dir}")
        sys.exit(1)
    
    # 执行批量转换
    batch_convert_pdfs(args.pdf_dir, args.output_dir, args.dpi, args.quality)

if __name__ == "__main__":
    import io  # 导入io模块
    main() 