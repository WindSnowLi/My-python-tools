from PIL import ImageEnhance
from PIL import Image
import argparse

def enhance_brightness(image_path, factor):
    # 打开图片
    image = Image.open(image_path)
    # 创建增强器
    enhancer = ImageEnhance.Brightness(image)
    # 增强图片亮度
    bright_image = enhancer.enhance(factor)
    # 显示增强后的图片
    bright_image.show()

    return bright_image


if __name__ == '__main__':
    """
    参数输入 第一参数是图片路径，第二个参数是增强倍数，第三个参数是是否保存，默认不，第四个参数是保存路径，默认是原路径
    """
    parser = argparse.ArgumentParser(description='Enhance image brightness.')
    parser.add_argument('image_path', type=str, help='Path to the image file.')
    parser.add_argument('factor', type=float, help='Enhancement factor (1.0 means no change).')
    parser.add_argument('--save', action='store_true', help='Save the enhanced image.')
    parser.add_argument('--save_path', type=str, default=None, help='Path to save the enhanced image.')
    args = parser.parse_args()

    image = enhance_brightness(args.image_path, args.factor)
    # 如果需要保存图片
    if args.save:
        # 如果没有指定保存路径，则使用原路径
        if args.save_path is None:
            args.save_path = args.image_path
        # 保存图片
        image.save(args.save_path)
        print(f"Enhanced image saved at {args.save_path}.")



