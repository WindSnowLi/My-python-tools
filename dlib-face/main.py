import sys
import os
import dlib
import cv2 as cv


# 加载人脸检测器
detector = dlib.get_frontal_face_detector()
# 加载人脸关键点检测模型
predictor_path = "shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)

def face_landmark_detect(imgfile):
    win = dlib.image_window()

    print("Processing file: {}".format(imgfile))
    img = dlib.load_rgb_image(imgfile)

    win.clear_overlay()
    win.set_image(img)

    # 检测每个人脸的边界框
    dets = detector(img, 1)
    shapes = []
    # len(dets) 是检测到的人脸数量
    print("Number of faces detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))

        # 检测 box d 内的人脸关键点
        shape = predictor(img, d)
        print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
                                                  shape.part(1)))
        # 画出人脸关键点
        win.add_overlay(shape)
        shapes.append(shape)
    win.add_overlay(dets)
    dlib.hit_enter_to_continue()
    return shapes

if __name__ == '__main__':
    imgfile = "./test.jpg"
    shapes = face_landmark_detect(imgfile)
    img = cv.imread(imgfile)
    for shape in shapes:
        for i in range(68):
            cv.circle(img, (shape.part(i).x, shape.part(i).y), 2, (0, 0, 255), -1)
    cv.imshow('img', img)
    cv.waitKey(0)
