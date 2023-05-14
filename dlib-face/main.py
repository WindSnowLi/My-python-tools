import dlib
import cv2 as cv
import math


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

# 计算单只眼睛的 EAR 值
def euclidean_distance(p1, p2):
    distance = 0.0
    for i in range(len(p1)):
        distance += (p1[i] - p2[i]) ** 2
    return math.sqrt(distance)

# 计算单只眼睛的 EAR 值
def eye_aspect_ratio(eye):
    # 计算两组垂直方向上的欧氏距离
    A = euclidean_distance([eye[1].x, eye[1].y], [eye[5].x,eye[5].y])
    B = euclidean_distance([eye[2].x, eye[2].y], [eye[4].x,eye[4].y])
    # 计算水平方向上的欧氏距离
    C = euclidean_distance([eye[0].x, eye[0].y], [eye[3].x,eye[3].y])

    # 直接计算计算欧氏距离

    # ear值
    ear = (A + B) / (2.0 * C)
    return ear

# 根据关键点检查是否疲劳
def check_fatigue(shapes):
    if len(shapes) == 0:
        return False
    shape = shapes[0]
    # 左眼关键点
    left_eye = [shape.part(36), shape.part(37), shape.part(38), shape.part(39), shape.part(40), shape.part(41)]
    # 右眼关键点
    right_eye = [shape.part(42), shape.part(43), shape.part(44), shape.part(45), shape.part(46), shape.part(47)]
    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)
    ear = (left_ear + right_ear) / 2.0
    print("ear: ", ear)
    # 检查是否疲劳
    return ear < 0.18

if __name__ == '__main__':
    imgfile = "./test.jpg"
    shapes = face_landmark_detect(imgfile)
    print("FATIGUE" if check_fatigue(shapes) else "NORMAL")
    img = cv.imread(imgfile)
    for shape in shapes:
        for i in range(68):
            cv.circle(img, (shape.part(i).x, shape.part(i).y), 2, (0, 0, 255), -1)
    cv.imshow('img', img)
    cv.waitKey(0)
