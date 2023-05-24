import qrcode

# 创建QRCode对象
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)

# 设置二维码内容
qr.add_data("https://www.baidu.com/")

# 生成二维码图像
img = qr.make_image(fill_color="black", back_color="white")

# 显示二维码图像
img.show()

# 保存到文件
img.save("qr.png")
