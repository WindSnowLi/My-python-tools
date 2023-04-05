from moviepy.editor import *

# 默认转，文件极大
# clip = VideoFileClip("input.mp4")

clip = (VideoFileClip("input.mp4")
        # 缩放
        .resize(0.5)
        # 倍速
        .speedx(2))
clip.write_gif("output.gif", fps=15, opt="nq")