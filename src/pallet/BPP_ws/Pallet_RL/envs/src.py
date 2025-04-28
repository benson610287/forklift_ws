import pybullet as p
import numpy as np
import pybullet_data
import random
from math import pi, tan, radians, floor

class Plane:
    def __init__(self):
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.planeID = p.loadURDF("plane.urdf")

class Bin:
    def __init__(self, args):
        self.args = args
        if self.args.bin_model == 1:
            self.Bin_pos = [2.55, 1.05, 0] # bin_2 30x20x15
            self.Bin = p.loadURDF("Pallet_RL/envs/bin_description/urdf/bin_2.urdf", self.Bin_pos, useFixedBase=True) 
            self.L = 30
            self.W = 20
            self.H = 15

        elif self.args.bin_model == 2:
            self.Bin_pos = [3.05, 1.55, 0] # bin_4 40x30x20
            self.Bin = p.loadURDF("Pallet_RL/envs/bin_description/urdf/bin_4.urdf", self.Bin_pos, useFixedBase=True) 
            self.L = 40
            self.W = 30
            self.H = 20
        
        elif self.args.bin_model == 3:
            self.Bin_pos = [2.8, 1.8, 0] # bin_5 35x35x24
            self.Bin = p.loadURDF("Pallet_RL/envs/bin_description/urdf/bin_5.urdf", self.Bin_pos, useFixedBase=True) 
            self.L = 35
            self.W = 35
            self.H = 24

        self.V = self.L * self.W * self.H

class box:
    def __init__(self, args):
        self.args = args
        if self.args.box_model == 1:
            self.num = random.randint(1,4)
        elif self.args.box_model == 2:
            self.num = random.randint(5,9)
        elif self.args.box_model == 3:
            self.num = random.randint(10,16)

        self.pre_box_pos = [5, 5, 0]
        self.pre_box_ori = p.getQuaternionFromEuler([0, 0, 0])

    def rand_box(self):

#-------------------------------------bin_2------------------------------------------------------
        if self.num == 1:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_1.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 5
            self.W = 10
            self.H = 2
        elif self.num == 2:
            self.box_1 = p.loadURDF("//Pallet_RL/envs/box_description/urdf/box_2.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 6
            self.W = 6
            self.H = 1
        elif self.num == 3:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_3.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 5
            self.W = 5
            self.H = 5
        elif self.num == 4:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_4.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 3
            self.W = 9
            self.H = 1

#-------------------------------------bin_4------------------------------------------------------
        elif self.num == 5:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_5.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 3
            self.W = 4
            self.H = 2
        elif self.num == 6:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_6.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 3
            self.W = 5
            self.H = 2
        elif self.num == 7:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_7.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 4
            self.W = 5
            self.H = 2
        elif self.num == 8:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_8.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 3
            self.W = 5
            self.H = 4
        elif self.num == 9:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_9.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 4
            self.W = 5
            self.H = 3
# ---------------------------------------------------real_box-------------------------------------
        elif self.num == 10:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_10.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 21
            self.W = 28
            self.H = 10

        elif self.num == 11:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_11.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 21
            self.W = 25
            self.H = 12
        elif self.num == 12:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_12.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 12
            self.W = 25
            self.H = 23
        elif self.num == 13:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_13.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 21
            self.W = 4
            self.H = 10
        elif self.num == 14:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_14.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 22
            self.W = 6
            self.H = 11
        elif self.num == 15:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_15.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 11
            self.W = 7
            self.H = 18

        elif self.num == 16:
            self.box_1 = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_16.urdf", self.pre_box_pos, self.pre_box_ori)

            self.L = 21
            self.W = 28
            self.H = 10
        
    
        # ----------------------------------real_box----------------------------------
        self.V = self.L * self.W * self.H

    def stack(self, pos, ori):
        select = str(self.num)
        #remove random_box
        p.removeBody(self.box_1)
        
        #stack select box to bin or tray
        self.stack_box = p.loadURDF("Pallet_RL/envs/box_description/urdf/box_"+ select +".urdf", pos, ori, useFixedBase=True)

class camera:
    def __init__(self):
        self.width = 1280
        self.height = 1280
        self.fov = 50
        self.aspect = 1
        self.near = 0.1
        self.far = 120

        self.Correction_x_val = 0.00570333
        self.Correction_y_val = 0.00571693
        self.Correction_d_val = 0.034

        self.cameraPos = [5,5,3]
        self.targetPos = [5,5,0]
        self.cameraupPos = [1,0,0]

        self.viewMatrix = p.computeViewMatrix(
            cameraEyePosition = self.cameraPos,
            cameraTargetPosition = self.targetPos,
            cameraUpVector = self.cameraupPos,
            physicsClientId = 0
        )

        self.projection_matrix = p.computeProjectionMatrixFOV(self.fov, self.aspect, self.near, self.far)

    def get_img(self):
        self.width, self.height, self.rgb, self.depth_img, self.seg = p.getCameraImage(self.width, self.height, self.viewMatrix, self.projection_matrix, renderer=p.ER_BULLET_HARDWARE_OPENGL, shadow=1, lightDirection=[1, 1, 1], physicsClientId = 0)       
    
    def get_information(self):
        self.get_img()

        tran_matrix = np.array(self.viewMatrix).reshape(4,4)
        pro_matrix = np.array(self.projection_matrix).reshape(4,4)

        #get object_pixels
        depth_buffer = np.reshape(self.depth_img, [self.width, self.height])
        depth_real = self.far * self.near / (self.far - (self.far - self.near) * depth_buffer)
        depth_threshold = 0.967  # 设置深度阈值，用于检测物体
        object_pixels = np.where(self.depth_img < depth_threshold)

        #get_first_pixels
        first_x, first_y = object_pixels[1][0], object_pixels[0][0]
        first_depth_value = self.depth_img[first_y, first_x]

        #get_end_pixels
        end_x, end_y = object_pixels[1][-1], object_pixels[0][-1]
        end_depth_value = self.depth_img[end_y, end_x]

        #coordinate trans 
        f_x_ndc = (2 * first_x / self.width) - 1
        f_y_ndc = 1 - (2 * first_y / self.height)

        f_x_proj = f_x_ndc * 0.1
        f_y_proj = f_y_ndc * 0.1
        first_pix = np.array([f_x_proj, f_y_proj, -1,1]).T

        f_world_point = np.dot(np.linalg.inv(pro_matrix), first_pix)
        f_world_point = f_world_point / f_world_point[3]
        f_world_point = np.dot(np.linalg.inv(tran_matrix), f_world_point)

        e_x_ndc = (2 * end_x / self.width) - 1
        e_y_ndc = 1 - (2 * end_y / self.height)

        e_x_proj = e_x_ndc * 0.1
        e_y_proj = e_y_ndc * 0.1
        end_pix = np.array([e_x_proj, e_y_proj, -1,1]).T

        e_world_point = np.dot(np.linalg.inv(pro_matrix), end_pix)
        e_world_point = e_world_point / e_world_point[3]
        e_world_point = np.dot(np.linalg.inv(tran_matrix), e_world_point)

        #calculate length, width, height
        length = e_world_point[0] - f_world_point[0]
        width = e_world_point[1] - f_world_point[1]

        length = length / self.Correction_x_val / ((1 - end_depth_value) / self.Correction_d_val)
        width = width / self.Correction_y_val / ((1 - end_depth_value) / self.Correction_d_val)

        object_length = round(length, 1) * 10
        object_width  = round(width, 1) * 10
        object_depth = np.max(depth_real[object_pixels[1], object_pixels[0]]) - np.min(depth_real[object_pixels[1], object_pixels[0]])
        object_depth = floor(round(object_depth, 1) * 10)

        return int(object_length), int(object_width), int(object_depth) 