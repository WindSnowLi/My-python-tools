import cv2
import time
import torch
import argparse
import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms
from utils.datasets import letterbox
from utils.torch_utils import select_device
from models.experimental import attempt_load
from utils.general import non_max_suppression_kpt, strip_optimizer, xyxy2xywh
from utils.plots import output_to_keypoint, plot_skeleton_kpts, colors, plot_one_box_kpt


# 封装PoseEstimation的类
class PoseEstimation:
    def __init__(self, opt):
        strip_optimizer(opt.device, opt.poseweights)
        self.device = select_device(opt.device)  # select device
        self.model = attempt_load(
            opt.poseweights, map_location=self.device)  # Load model
        self.model.eval()
        self.opt = opt
        self.device = select_device(opt.device)  # select device
        self.names = self.model.module.names if hasattr(
            self.model, 'module') else self.model.names

    def get_pose(self, frame):
        frame_width = frame.shape[1]

        orig_image = frame  # store frame
        # convert frame to RGB
        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
        image = letterbox(image, (frame_width),
                          stride=64, auto=True)[0]
        image = transforms.ToTensor()(image)
        image = torch.tensor(np.array([image.numpy()]))

        image = image.to(self.device)  # convert image data to device
        image = image.float()  # convert image to float precision (cpu)

        with torch.no_grad():  # get predictions
            output_data, _ = self.model(image)

        output_data = non_max_suppression_kpt(output_data,  # Apply non max suppression
                                              # Conf. Threshold.
                                              0.25,
                                              0.65,  # IoU Threshold.
                                              # Number of classes.
                                              nc=self.model.yaml['nc'],
                                              # Number of keypoints.
                                              nkpt=self.model.yaml['nkpt'],
                                              kpt_label=True)
        # 关键点
        posess = []
        for i, poses in enumerate(output_data):
            for pose in poses:
                pose = pose[6:]
                # 每三个元素为一个关键点的坐标，其中第一个元素为横坐标，第二个元素为纵坐标，第三个元素为置信度，忽略低于0.5的关键点
                for j in range(0, len(pose), 3):
                    if pose[j + 2] < 0.5:
                        posess.append(None)
                        continue
                    x = int(pose[j])
                    y = int(pose[j + 1])
                    posess.append((x, y))
        return output_data, image, posess

    def draw_pose(self, image, output_data):
        # Change format [b, c, h, w] to [h, w, c] for displaying the image.
        im0 = image[0].permute(1, 2, 0) * 255
        im0 = im0.cpu().numpy().astype(np.uint8)

        # reshape image format to (BGR)
        im0 = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR)

        for i, pose in enumerate(output_data):  # detections per image
            if len(output_data):  # check if no pose
                for c in pose[:, 5].unique():  # Print results
                    n = (pose[:, 5] == c).sum()  # detections per class
                    print("No of Objects in Current Frame : {}".format(n))

                # loop over poses for drawing on frame
                for det_index, (*xyxy, conf, cls) in enumerate(reversed(pose[:, :6])):
                    c = int(cls)  # integer class
                    kpts = pose[det_index, 6:]
                    print(kpts)
                    label = None if opt.hide_labels else (
                        self.names[c] if opt.hide_conf else f'{self.names[c]} {conf:.2f}')
                    plot_one_box_kpt(xyxy, im0, label=label, color=colors(c, True),
                                     line_thickness=opt.line_thickness, kpt_label=True, kpts=kpts, steps=3,
                                     orig_shape=im0.shape[:2])
        return im0

    def get_draw_pose(self, frame):
        poses, image, xys = self.get_pose(frame)
        return self.draw_pose(image, poses), xys


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--poseweights', nargs='+', type=str,
                        default='yolov7-w6-pose.pt', help='model path(s)')
    parser.add_argument('--source', type=str, default='0',
                        help='video/0 for webcam')  # video source
    parser.add_argument('--device', type=str, default='0',
                        help='cpu/0,1,2,3(gpu)')  # device arugments
    parser.add_argument('--view-img', action='store_true',
                        help='display results')  # display results
    # save confidence in txt writing
    parser.add_argument('--save-conf', action='store_true',
                        help='save confidences in --save-txt labels')
    parser.add_argument('--line-thickness', default=3, type=int,
                        help='bounding box thickness (pixels)')  # box linethickness
    parser.add_argument('--hide-labels', default=False,
                        action='store_true', help='hide labels')  # box hidelabel
    parser.add_argument('--hide-conf', default=False,
                        action='store_true', help='hide confidences')  # boxhideconf
    opt = parser.parse_args()
    return opt


# 判断1 2 0 / 16 15


if __name__ == "__main__":
    opt = parse_opt()
    pose = PoseEstimation(opt)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            frame, xys = pose.get_draw_pose(frame)
            print("XY点坐标", xys)
            cv2.imshow("Pose Estimation", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
