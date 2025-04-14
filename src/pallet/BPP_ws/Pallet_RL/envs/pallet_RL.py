import gym
import pybullet as p
from gym import spaces
import numpy as np
import time
from math import pi
from .argument import get_args 
from .src import Plane,Bin,box,camera

class Pallet_env(gym.Env):
    def __init__(self):
        physicsClient = p.connect(p.GUI)
        p.setGravity(0, 0, -9.8)
        p.setRealTimeSimulation(1)
        Plane()

        self.args = get_args()
        self.box_order = 0
        self.camera = camera()
        self.camera.get_img()
        self.Bin = Bin(self.args)
        self.box1 = box(self.args)
        self.box1.rand_box()

        low_action = np.array([-10, -10, -10, -10],dtype=np.float32)
        high_action = np.array([10, 10, 10, 10],dtype=np.float32)
        self.action_space = spaces.MultiDiscrete([3, 2])
        self.observation_space = spaces.Dict(
            {
                "Bin_state": spaces.Box(low=-2, high=1, shape=(self.Bin.L + 1, self.Bin.W + 1, self.Bin.H), dtype=np.int32),
                "Grid_score": spaces.Box(low=-10, high=10, shape=(self.Bin.L, self.Bin.W, self.Bin.H), dtype=np.float32),
            }
        )
        
        self.space_flag = None
        self.mask_space = np.zeros(shape = ((self.Bin.L +1), (self.Bin.W +1), (self.Bin.H)), dtype=np.int32)
        self.mask_space[:, :, 0] = 1
        self.mask_space[self.Bin.L, :, :] = -1
        self.mask_space[:, self.Bin.W, :] = -1

        self.score_space = np.zeros(shape = ((self.Bin.L), (self.Bin.W), (self.Bin.H)), dtype=np.float32)
        self.init_score_space()

        self.select_pos = None
        
        self.pos_ep1 = None
        self.pos_ep2 = None
        self.pos_ep3 = None

        self.bef_ep1 = None
        self.bef_ep2 = None
        self.bef_ep3 = None

        self.rotate_flag = False
        self.non_flag = False
        self.select_3_flag = False
        self.select_other_flag = False
        self.non_full_flag = False

        self.eps = []
        self.eps_stage = []
        self.eps_ground = []
        self.init_eps_ground()

        self.success_stack = None
        self.score = 0
        self.score_count = 0
        self.cur_action = 0 
        self.count_action = 0       

        # self.hitRayColor = [1, 0, 1]
        # self.missRayColor = [0, 1, 0]
        # self.rayFroms = None
        # self.rayTos = None

        self.rewardlst = []
        self.step_reward = []
        self.trainreward = []
        self.timesteps = 0
        self.total_V = 0
        self.testtime = 0
        self.successtime = 0

        self.count = 0

        # first box stack
        self.origin_pos = [1.05, 0.05, 0.075]
        self.box_pos = [0, 0, 0]
        self.origin_ori = [0, 0, 0]
        self.pos = [1.05, 0.05, 0.075]
        self.com_pos = [0, 0, 0]
        self.ori = [0, 0, 0]
        self.rotation_compensation_W = 0
        self.rotation_compensation_L = 0
        self.waste_space_score = 0
        self.waste_bottom_space = 0
        self.ratio = 0
        self.ratios = []
        self.item = []



        self.box_list = []
        self.box_long_list = []
        self.box_pos_list = []
        self.Z_space_list = []
        self.select_space = []
        self.corner_list = []  # ----------+ ----------+
                               # |         | |         |
                               # |         | |         |
                               # |         | ----------+
                               # |         | corner_space
                               # ----------+
                               #[[L,W,H,V,count], [x, y, z]]
    # input stack box_ori 
    def step(self, action):

        reward = 0
        stack_score = 0
        self.select_other_flag = False
        self.non_full_flag = False
        self.box1 = box(self.args)
        self.box1.rand_box()
        _, _, _= self.camera.get_information()

        # first box stack origin point
        if self.count == 0:
            self.box1.stack(self.origin_pos, p.getQuaternionFromEuler(self.origin_ori))
            self.save_box()

            self.mask_space = self.calculate_mask(self.mask_space)
            self.calculate_e_pos()
            self.normal_eps(self.pos_ep3)
            self.del_fake_eps()
            self.calculate_score()
    
        else:    
            # box 6 status select(get box ori)
            #select remain space small --> big
            self.box_status_select(action[1])
            rotate = action[1]
            self.save_box()

            if (len(self.eps) > 0):
                self.calculate_eps_score()

            self.select_action(action[0])

           

            #change ----> refound eps and reward reduce 
            while(not self.success_stack):

                # self.score += -3
                self.select_other_eps()
                self.select_other_flag = True

                if((self.count_action == 3) and (self.rotate_flag) and (not self.success_stack) and (self.non_flag) and (self.non_full_flag)):
                    self.done=True
                    self.waste_bottom_space = self.calculate_waste_bottom()
                    reward = self.get_reward()
                    self.successtime += 1
                    obs = self.get_obs()

                    print("--------------------stack end----------------------")
                    print("ratio",self.ratio)
                    

                    self.ratios.append(self.ratio)
                    self.item.append(self.count + 1)

                    return obs, reward, self.done, {}
                
                elif(self.count_action == 3) and (not self.success_stack):
                    
                    # self.score += -3
                    self.select_non_eps()
                    self.non_flag = True

                    if(not self.success_stack) and (not self.rotate_flag):

                        # self.score += -5
                        rotate = self.box_rotate(rotate)
                        self.non_flag = False
                        self.calculate_eps_score()

                    elif(not self.success_stack) and (self.rotate_flag) and (not self.non_full_flag):
                        self.non_full_stack()
                        self.non_full_flag = True

                        if (not self.success_stack):
                            # rotate
                            rotate = self.box_rotate(rotate)
                            self.calculate_eps_score()
                            self.non_full_stack()
                        
                    self.count_action = 0

                    

                if (self.success_stack) and (self.rotate_flag):
                    self.score += -5  

            self.non_flag = False
            self.rotate_flag = False
            self.select_3_flag = False
            self.count_action = 0

            self.mask_space = self.calculate_mask(self.mask_space)
            self.calculate_e_pos()
            self.normal_eps(self.pos_ep3)
            # self.calculate_eps_score()
            self.waste_space_score = self.calculate_waste_space() 
            self.del_fake_eps()
            # self.e_pos_min()
            self.eps = self.arrange_eps(self.eps)
            self.eps_ground = self.arrange_eps(self.eps_ground)
            self.eps_stage = self.arrange_eps(self.eps_stage)

            #-----------before reward--------------------
            # if (self.select_other_flag == True) and (self.non_flag == False):
            #     if (self.cur_action == 0) or (self.cur_action == 1):
            #         self.score += (self.stack_score(self.score_space) * 0.7 + self.waste_space_score) * 0.4
            #         reward = (self.stack_score(self.score_space) * 0.7 + self.waste_space_score) * 0.4
            #         self.score_count += 1
            #     elif self.box_pos[2] == 0:
            #         self.score += (self.stack_score(self.score_space) * 0.7 + self.waste_space_score) * 0.4
            #         reward = (self.stack_score(self.score_space) * 0.7 + self.waste_space_score) * 0.4
            #         self.score_count += 1
            #     else :
            #         self.score += 0
            #         reward = 0

            # elif(self.select_other_flag == False):
            #     if(action[0] == 0) or (action[0] == 1):
            #         self.score += (self.stack_score(self.score_space) * 0.7 + self.waste_space_score) * 0.4
            #         reward = (self.stack_score(self.score_space) * 0.7 + self.waste_space_score) * 0.4
            #         self.score_count += 1
            #     elif self.box_pos[2] == 0:
            #         self.score += (self.stack_score(self.score_space) * 0.7 + self.waste_space_score) * 0.4
            #         reward = (self.stack_score(self.score_space) * 0.7 + self.waste_space_score) * 0.4
            #         self.score_count += 1
            #     else :
            #         self.score += 0
            #         reward = 0

            # elif (self.select_other_flag == True) and (self.non_flag == True):
            #     self.score += 0
            #     reward = 0

            #-----------before reward--------------------
            # # ----final reward--------
            if (self.select_other_flag == True) and (self.non_flag == False):
                if (self.cur_action == 0) or (self.cur_action == 1):
                    self.score += (self.stack_score(self.score_space) * 0.7 + self.waste_space_score * 0.5) * 0.4
                    reward = (self.stack_score(self.score_space) * 0.7 + self.waste_space_score * 0.5) * 0.4
                    self.score_count += 1

                elif self.box_pos[2] == 0:
                    self.score += self.stack_score(self.score_space) * 0.3 
                    reward = self.stack_score(self.score_space) * 0.3 + self.step_reward[-1]
                    self.score_count += 1

                else :
                    self.score += self.stack_score(self.score_space) * 0.2 
                    reward = self.stack_score(self.score_space) * 0.2 + self.step_reward[-1]
                    self.score_count += 1

            elif(self.select_other_flag == False):
                if(action[0] == 0) or (action[0] == 1):
                    self.score += (self.stack_score(self.score_space) * 0.7 + self.waste_space_score * 0.5) * 0.4
                    reward = (self.stack_score(self.score_space) * 0.7 + self.waste_space_score * 0.5) * 0.4
                    self.score_count += 1

                elif self.box_pos[2] == 0:
                    self.score += self.stack_score(self.score_space) * 0.3 
                    reward = self.stack_score(self.score_space) * 0.3 + self.step_reward[-1]
                    self.score_count += 1

                else :
                    if(len(self.step_reward) > 0):
                        self.score += self.stack_score(self.score_space) * 0.2 
                        reward = self.stack_score(self.score_space) * 0.2 + self.step_reward[-1]
                        self.score_count += 1

            elif (self.select_other_flag == True) and (self.non_flag == True):
                self.score += 0
                reward = self.step_reward[-1]
            # #----final reward-------
            self.step_reward.append(reward)
            # self.score += (self.stack_score(self.score_space) * 0.7 + self.waste_space_score) * 0.4
            # reward = (self.stack_score(self.score_space) * 0.7 + self.waste_space_score) * 0.4
            stack_score = self.stack_score(self.score_space)
            # reward = self.get_reward()       
            self.calculate_score()
            self.bpos_to_pos()
            self.stack_action()
             
        self.total_V += self.box1.V
        self.ratio = self.total_V / self.Bin.V * 100

        obs = self.get_obs()

        self.rotation_compensation_W = 0
        self.rotation_compensation_L = 0
        self.com_pos = [0,0,0]
        self.count +=1
        # time.sleep(1)
        
        return obs, reward, self.done, {}

    def reset(self):

        # Plane()
        reward = self.get_reward()
        self.trainreward.append(reward)

        self.mask_space = np.zeros(shape = (self.Bin.L + 1, self.Bin.W + 1, self.Bin.H), dtype=np.int32)
        self.mask_space[:, :, 0] = 1
        self.mask_space[self.Bin.L, :, :] = -1
        self.mask_space[:, self.Bin.W, :] = -1

        self.score_space = np.zeros(shape = (self.Bin.L, self.Bin.W, self.Bin.H), dtype=np.float32)
        self.init_score_space()

        self.pos_ep1 = None
        self.pos_ep2 = None
        self.pos_ep3 = None
        self.eps = []
        self.eps_stage = []
        self.success_stack = None
        self.cur_action = 0
        self.count_action = 0
        self.waste_space_score = 0
        self.rotate = False
        self.non_flag = False
        self.select_other_flag = False

        self.box_order = 0

        # if self.testtime>0:jrdlst))

        # self.box1 = box()
        # self.box1.rand_box()

        # pos = [1.1, 0.1, 0.3]
        # ori = [0, 0, 0]

        # self.box1.stack(pos, p.getQuaternionFromEuler(ori))

        # self.rewardlst = []
        # self.timesteps = 0
        self.pos = [1.05, 0.05, 0.075]
        self.box_pos = [0, 0, 0]
        self.ori = [0, 0, 0]
        self.rotation_compensation_W = 0
        self.rotation_compensation_L = 0
        self.ratio = 0

        self.score = 0
        self.score_count = 0

        self.box_list = []
        self.box_long_list = []
        self.box_pos_list = []
        self.Z_space_list = []
        self.X_space = []
        self.X_space_list = []
        self.Y_space = []
        self.Y_space_list = []
        self.select_space = []
        self.corner_list = []
        self.count = 0
        self.testtime += 1
        self.done = False
        self.total_V = 0
        self.waste_bottom_space = 0
        # self.targetpos = self.target.reset_spawn()
        # self.rayFroms = np.array(self.targetpos, dtype=np.float32)
        # self.rayTos = np.array(self.targetpos + np.array([0, 0, 1]), dtype=np.float32)
        
        obs = self.get_obs()
        p.resetSimulation()
        Plane()
        self.Bin = Bin(self.args)
        self.init_eps_ground()
        print("testtime:", self.testtime)
        return obs

    def render(self, mode='human', clode=False):
        pass

    def close(self):
        p.disconnect()

    def get_obs(self):
        # left = np.array(p.getLinkState(self.r2d2.r2d2ID, 0)[0])
        # right = np.array(p.getLinkState(self.r2d2.r2d2ID, 4)[0])
        # self.rx, self.ry, self.rz = pos = (left+right)/2
        # dis = np.linalg.norm(pos-self.targetpos)
        # r2d2_quaternion = p.getBasePositionAndOrientation(self.r2d2.r2d2ID)[1]
        # self.r2d2_angle = p.getEulerFromQuaternion(r2d2_quaternion)[2] + np.pi / 2
        # tx, ty, _ = self.targetpos 
        # self.target_angle = np.arctan(ty / tx)
        # obs = np.array([self.rx,self.ry,tx,ty])
        # obs = np.append(obs, dis)
        # obs = np.append(obs, self.r2d2_angle)
        # obs = np.append(obs, self.target_angle)
        # obs = np.array([self.Bin.V - self.total_V])#, self.box1.V])
        # obs = np.append(obs,self.box1.L)
        # obs = np.append(obs,self.box1.W)
        # obs = np.append(obs,self.box1.H)
        # obs = np.append(obs,self.pos)
        # obs = np.append(obs,self.ori)
        # print("obs_pos",self.pos)

        return {"Bin_state": self.mask_space,"Grid_score": self.score_space}

    def get_reward(self):
        # score = self.total_V / self.Bin.V * 100
        # reward = score - 80
        reward = (self.ratio - 60)*0.1 + (self.score / (self.score_count + 1))*0.8 + (-self.waste_bottom_space) * 0.1
        # reward = (self.score / (self.count + 1) / 20)*0.5 + self.waste_space_score * 0.5
        # pos=self.get_obs()[0:2]
        # pos_reward = -np.linalg.norm(pos-self.targetpos[0:2])
        # angle_reward = -abs(self.r2d2_angle-self.target_angle)

        #space usage ratio (80)

        return reward
        #return pos_reward+angle_reward

    # box 6 status select for stack and switch W H L 
    # def box_status_select(self, rem_space):
    #     if (self.box1.L <= rem_space[0]) and (self.box1.W <= rem_space[1]) and (self.box1.H <= rem_space[2]):
    #         self.ori = [0, 0, 0]
    #         return True

    #     elif (self.box1.W <= rem_space[0]) and (self.box1.L <= rem_space[1]) and (self.box1.H <= rem_space[2]):
    #         self.ori = [0, 0, -pi/2]
    #         self.box1.L, self.box1.W = self.box1.W, self.box1.L
    #         self.rotation_compensation_W = self.box1.W
    #         return True 
        
    #     elif (self.box1.H <= rem_space[0]) and (self.box1.W <= rem_space[1]) and (self.box1.L <= rem_space[2]):
    #         self.ori = [0, -pi/2, 0]
    #         self.box1.L, self.box1.H = self.box1.H, self.box1.L
    #         self.rotation_compensation_L = self.box1.L
    #         return True

    #     elif (self.box1.L <= rem_space[0]) and (self.box1.H <= rem_space[1]) and (self.box1.W <= rem_space[2]):
    #         self.ori = [pi/2, 0, 0]
    #         self.box1.W, self.box1.H = self.box1.H, self.box1.W
    #         self.rotation_compensation_W = self.box1.W
    #         return True

    #     elif (self.box1.H <= rem_space[0]) and (self.box1.L <= rem_space[1]) and (self.box1.W <= rem_space[2]):
    #         self.ori = [pi/2, 0, pi/2]
    #         self.box1.L, self.box1.W, self.box1.H = self.box1.H, self.box1.L, self.box1.W
    #         return True

    #     elif (self.box1.W <= rem_space[0]) and (self.box1.H <= rem_space[1]) and (self.box1.L <= rem_space[2]):
    #         self.ori = [0, -pi/2, -pi/2]
    #         self.box1.L, self.box1.W, self.box1.H = self.box1.W, self.box1.H, self.box1.L
    #         return True
    #     else:
    #         return False
    
    #RL direction select
    def box_status_select(self, action):
        if (action == 0):
            self.ori = [0, 0, 0]

        elif (action == 1):
            self.ori = [0, 0, -pi/2]
            self.box1.L, self.box1.W = self.box1.W, self.box1.L
            self.rotation_compensation_W = self.box1.W * 0.1
             
    def box_rotate(self, action):
        self.rotate_flag = True

        if (action == 0):
            self.ori = [0, 0, -pi/2]
            self.box1.L, self.box1.W = self.box1.W, self.box1.L
            self.rotation_compensation_W = self.box1.W * 0.1
            return 1

        elif(action == 1):
            self.ori = [0, 0, 0]
            self.box1.L, self.box1.W = self.box1.W, self.box1.L
            return 0

    # use box_num get stack box pos
    def get_box_pos(self):
        
        self.pos = self.select_space[1]


        

                
    def calculate_V(self,L,W,H):
        return L * W * H


    def save_box(self):
        
        self.box_list.append([self.box1.L, self.box1.W, self.box1.H])
        self.box_list = list(set(tuple(t) for t in self.box_list))
        self.box_list = list(list(t) for t in self.box_list)
                
        
    #basic heuristics cut space (not use)
    def calculate_space(self):
         # First space remain L W H
        if self.count == 0:
            self.space_rem_L = self.Bin.L - self.box_list[0][0][0] 
            self.space_rem_W = self.Bin.W - self.box_list[0][0][1]
            self.space_rem_H = self.Bin.H - self.box_list[0][0][2] - self.pos[2]

            # First space remaining calculate 
            self.Z_V = self.calculate_V(self.box1.L, self.box1.W , self.space_rem_H)
            self.Z_space = [self.box1.L, self.box1.W, self.space_rem_H, self.Z_V, self.count]
            self.Z_pos = [self.pos[0], self.pos[1],self.pos[2] + self.box1.H]

            self.X_space = [self.space_rem_L, self.box1.W, self.Bin.H]
            self.X_pos = [self.pos[0] + self.box1.L, self.pos[1],self.origin_pos[2]]

            self.Y_space = [self.box1.L, self.space_rem_W, self.Bin.H]
            self.Y_pos = [self.pos[0], self.pos[1] + self.box1.W, self.origin_pos[2]]

            self.trans_space = [self.space_rem_L, self.space_rem_W, self.Bin.H]

            #trans_space for big space ---> (incomolete)2.1,
            if self.X_space[0] * self.X_space[1] >= self.Y_space[0] * self.Y_space[1]:
                    self.X_space[1] += self.trans_space[1]

            else:
                self.Y_space[0] += self.trans_space[0]

            self.X_V = self.calculate_V(self.X_space[0], self.X_space[1], self.X_space[2])
            self.Y_V = self.calculate_V(self.Y_space[0], self.Y_space[1], self.Y_space[2]) 
            
            self.X_space_list = [self.X_space, self.X_pos]
            self.Y_space_list = [self.Y_space, self.Y_pos]

            self.combine_area = [self.box1.L, self.box1.W]

            self.Z_space_list.append([self.Z_space, self.Z_pos])
            self.long_normal(self.Z_space_list)

        else:
            if self.space_flag == 'C':
                for i in range(len(self.box_list)):
                    if self.select_space[0][4] == self.box_list[i][0][4]:
                        z_space_V = self.calculate_V(self.box1.L, self.box1.W, self.Bin.H - self.pos[2] - self.box1.H)
                        z_space_long = [self.box1.L, self.box1.W, self.Bin.H - self.pos[2] - self.box1.H, z_space_V, self.count]
                        z_space_pos = [self.pos[0], self.pos[1], self.pos[2] + self.box1.H]

                        self.Z_space_list.append([z_space_long, z_space_pos])
                        self.long_normal(self.Z_space_list)

                        cor_x_V = self.calculate_V(self.select_space[0][0] - self.box1.L, self.select_space[0][1],self.box1.H)
                        cor_x_long = [self.select_space[0][0] - self.box1.L, self.select_space[0][1],self.box1.H, cor_x_V, self.count]
                        cor_x_pos = [self.pos[0] + self.box1.L, self.pos[1], self.pos[2]]

                        cor_y_V = self.calculate_V(self.box1.L, self.select_space[0][1] - self.box1.W, self.box1.H)
                        cor_y_long = [self.box1.L, self.select_space[0][1] - self.box1.W, self.box1.H, cor_y_V, self.count]
                        cor_y_pos = [self.pos[0], self.pos[1] + self.box1.W, self.pos[2]]

                        self.corner_list.append([cor_x_long, cor_x_pos])
                        self.corner_list.append([cor_y_long, cor_y_pos])
                        self.long_normal(self.corner_list)

                        break
                        
                        
            elif self.space_flag == 'Z':
                for i in range(len(self.box_list)):
                    if self.select_space[0][4] == self.box_list[i][0][4]:
                        cor_x_V = self.calculate_V(self.box_list[i][0][0] - self.box1.L, self.box1.W, self.box1.H)
                        cor_x_long = [self.box_list[i][0][0] - self.box1.L, self.box1.W, self.box1.H, cor_x_V, self.count]
                        cor_x_pos = [self.pos[0] + self.box1.L, self.pos[1], self.pos[2]]

                        cor_y_V = self.calculate_V(self.box1.L, self.box_list[i][0][1] - self.box1.W, self.box1.H)
                        cor_y_long = [self.box1.L, self.box_list[i][0][1] - self.box1.W, self.box1.H, cor_y_V, self.count]
                        cor_y_pos = [self.pos[0], self.pos[1] + self.box1.W, self.pos[2]]

                        z_space_V = self.calculate_V(self.box1.L, self.box1.W, self.Bin.H - self.pos[2] - self.box1.H)
                        z_space_long = [self.box1.L, self.box1.W, self.Bin.H - self.pos[2] - self.box1.H, z_space_V, self.count]
                        z_space_pos = [self.pos[0], self.pos[1], self.pos[2] + self.box1.H]


                        self.corner_list.append([cor_x_long, cor_x_pos])
                        self.corner_list.append([cor_y_long, cor_y_pos])
                        self.Z_space_list.append([z_space_long, z_space_pos])

                        self.long_normal(self.Z_space_list)
                        self.long_normal(self.corner_list)
                        
                        break
            
            elif self.space_flag == 'Y':
                if self.box1.L <= self.combine_area[0]:
                    cor_V = self.calculate_V(self.combine_area[0]-self.box1.L, self.box1.W, self.Bin.H)
                    cor_long = [self.combine_area[0]-self.box1.L, self.box1.W, self.Bin.H, cor_V, self.count]
                    cor_pos = [self.pos[0] + self.box1.L, self.pos[1], self.origin_pos[2]]

                    self.corner_list.append([cor_long, cor_pos])
                    self.long_normal(self.corner_list)
                    
                    #Recalculate combine_area
                    self.combine_area[1] =  self.combine_area[1] + self.box1.W
                   

                else:
                    cor_V = self.calculate_V(self.box1.L - self.combine_area[0], self.combine_area[1], self.Bin.H)
                    cor_long = [self.box1.L - self.combine_area[0], self.combine_area[1], self.Bin.H, cor_V, self.count]
                    cor_pos = [self.pos[0] + self.combine_area[0], self.pos[1] - self.combine_area[1], self.origin_pos[2]]

                    self.corner_list.append([cor_long, cor_pos])
                    self.long_normal(self.corner_list)

                    #Recalculate combine_area
                    self.combine_area[1] = self.combine_area[1] + self.box1.W

                #Recalculate X_space and Y_space
                self.X_space = [self.Bin.L - self.combine_area[0], self.combine_area[1], self.Bin.H]
                self.Y_space = [self.combine_area[0], self.Bin.W - self.combine_area[1], self.Bin.H]
                self.trans_space = [self.Bin.L - self.combine_area[0], self.Bin.W - self.combine_area[1], self.Bin.H]

                #trans_space for big space
                if self.X_space[0] * self.X_space[1] >= self.Y_space[0] * self.Y_space[1]:
                    self.X_space[1] += self.trans_space[1]

                else:
                    self.Y_space[0] += self.trans_space[0]

                            
                z_space_V = self.calculate_V(self.box1.L, self.box1.W, self.Bin.H - self.pos[2] - self.box1.H)
                z_space_long = [self.box1.L, self.box1.W, self.Bin.H - self.pos[2] - self.box1.H, z_space_V, self.count]
                z_space_pos = [self.pos[0], self.pos[1], self.pos[2] + self.box1.H]    
                
                self.Z_space_list.append([z_space_long, z_space_pos])
                self.long_normal(self.Z_space_list)
                self.X_V = self.calculate_V(self.X_space[0], self.X_space[1], self.X_space[2])
                self.Y_V = self.calculate_V(self.Y_space[0], self.Y_space[1], self.Y_space[2])

                self.X_pos = [self.combine_area[0] + self.origin_pos[0],self.origin_pos[1],self.origin_pos[2]]
                self.Y_pos = [self.origin_pos[0], self.combine_area[1] + self.origin_pos[1], self.origin_pos[2]]

                self.X_space_list = [self.X_space, self.X_pos]
                self.Y_space_list = [self.Y_space, self.Y_pos]

            elif self.space_flag == 'X':
                if self.box1.W <= self.combine_area[1]:
                    cor_V = self.calculate_V(self.box1.L, self.combine_area[1]-self.box1.W, self.Bin.H)
                    cor_long = [self.box1.L, self.combine_area[1]-self.box1.W, self.Bin.H, cor_V, self.count]
                    cor_pos = [self.pos[0], self.pos[1] + self.box1.W, self.origin_pos[2]]

                    self.corner_list.append([cor_long, cor_pos])
                    self.long_normal(self.corner_list)
                    
                    #Recalculate combine_area
                    self.combine_area[0] = self.combine_area[0] + self.box1.L
                    
                    
                else:
                    cor_V = self.calculate_V(self.combine_area[0], self.box1.W - self.combine_area[1], self.Bin.H)
                    cor_long = [self.combine_area[0], self.box1.W - self.combine_area[1], self.Bin.H, cor_V, self.count]
                    cor_pos = [self.pos[0] - self.combine_area[0], self.pos[1] + self.combine_area[1], self.origin_pos[2]]

                    self.corner_list.append([cor_long, cor_pos])
                    self.long_normal(self.corner_list)

                    #Recalculate combine_area
                    self.combine_area[0] = self.combine_area[0] + self.box1.L
                    
                #Recalculate X_space and Y_space
                self.X_space = [self.Bin.L - self.combine_area[0], self.combine_area[1], self.Bin.H]
                self.Y_space = [self.combine_area[0], self.Bin.W - self.combine_area[1], self.Bin.H]
                self.trans_space = [self.Bin.L - self.combine_area[0], self.Bin.W - self.combine_area[1], self.Bin.H]

                #trans_space for big space
                if self.X_space[0] * self.X_space[1] >= self.Y_space[0] * self.Y_space[1]:
                    self.X_space[1] += self.trans_space[1]

                else:
                    self.Y_space[0] += self.trans_space[0]


                z_space_V = self.calculate_V(self.box1.L, self.box1.W, self.Bin.H - self.pos[2] - self.box1.H)
                z_space_long = [self.box1.L, self.box1.W, self.Bin.H - self.pos[2] - self.box1.H, z_space_V, self.count]
                z_space_pos = [self.pos[0], self.pos[1], self.pos[2] + self.box1.H]    
                
                self.Z_space_list.append([z_space_long, z_space_pos])
                self.long_normal(self.Z_space_list)
                self.X_V = self.calculate_V(self.X_space[0], self.X_space[1], self.X_space[2])
                self.Y_V = self.calculate_V(self.Y_space[0], self.Y_space[1], self.Y_space[2])

                self.X_pos = [self.combine_area[0] + self.origin_pos[0], self.origin_pos[1],self.origin_pos[2]]
                self.Y_pos = [self.origin_pos[0], self.combine_area[1] + self.origin_pos[1], self.origin_pos[2]]

                self.X_space_list = [self.X_space, self.X_pos]
                self.Y_space_list = [self.Y_space, self.Y_pos]

    #select remain space small --> big (not use)
    def space_stack(self):
        if self.count > 0:
            #------------------------------------------method 1 cor -> Z -> Y -> X---------------------------------------------------------
            if(len(self.corner_list) > 0):
                for i in range(len(self.corner_list)):
                    if(self.box_status_select(self.corner_list[i][0])):
                        self.space_flag = 'C'
                        self.select_space = self.corner_list[i]
                        self.corner_list.pop(i)
                        break

                    elif i == len(self.corner_list) - 1 and not(self.box_status_select(self.corner_list[i][0])):
                        for i in range(len(self.Z_space_list)):
                            if(self.box_status_select(self.Z_space_list[i][0])):
                                self.space_flag = 'Z'
                                self.select_space = self.Z_space_list[i]
                                self.Z_space_list.pop(i)
                                break

                            elif i == len(self.Z_space_list) - 1 and not(self.box_status_select(self.Z_space_list[i][0])) and (self.Y_V < self.X_V):
                                if(self.box_status_select(self.Y_space_list[0])):
                                    self.space_flag = 'Y'
                                    self.select_space = self.Y_space_list
                                    continue
                                else:
                                    if(self.box_status_select(self.X_space_list[0])):
                                        self.space_flag = 'X'
                                        self.select_space = self.X_space_list
                                        continue
                            
                            elif i == len(self.Z_space_list) - 1 and not(self.box_status_select(self.Z_space_list[i][0])) and (self.Y_V > self.X_V):
                                if(self.box_status_select(self.X_space_list[0])):
                                    self.space_flag = 'X'
                                    self.select_space = self.X_space_list
                                    continue
                                    
                                else:
                                    if(self.box_status_select(self.Y_space_list[0])):
                                        self.space_flag = 'Y'
                                        self.select_space = self.Y_space_list
                                        continue
                                    else:
                                        self.select_space = None
                            else:
                                if(self.box_status_select(self.Y_space_list[0])):
                                    self.space_flag = 'Y'
                                    self.select_space = self.Y_space_list
                                    continue
                                else:
                                    self.select_space = None
                                
                                
            else:
                for i in range(len(self.Z_space_list)):
                    if(self.box_status_select(self.Z_space_list[i][0])):
                        self.space_flag = 'Z'
                        self.select_space = self.Z_space_list[i]
                        self.Z_space_list.pop(i)
                        break
                
                    elif i == len(self.Z_space_list) - 1 and not(self.box_status_select(self.Z_space_list[i][0])) and (self.Y_V < self.X_V):
                        if(self.box_status_select(self.Y_space_list[0])):
                            self.space_flag = 'Y'
                            self.select_space = self.Y_space_list
                            
                        else:
                            if(self.box_status_select(self.X_space_list[0])):
                                self.space_flag = 'X'
                                self.select_space = self.X_space_list
                            else:
                                self.select_space = None
                            
                    elif i == len(self.Z_space_list) - 1 and not(self.box_status_select(self.Z_space_list[i][0])) and (self.X_V < self.Y_V):
                        if(self.box_status_select(self.X_space_list[0])):
                            self.space_flag = 'X'
                            self.select_space = self.X_space_list
                            
                        else:
                            if(self.box_status_select(self.Y_space_list[0])):
                                self.space_flag = 'Y'
                                self.select_space = self.Y_space_list
                            
                            else:
                                self.select_space = None
            #------------------------------------------------------------------------------------------------------------

            #---------------------------------------------------method2 Z -> cor -> Y -> X-------------------------------
            # for i in range(len(self.Z_space_list)):
            #     if(self.box_status_select(self.Z_space_list[i][0])):
            #         self.space_flag = 'Z'
            #         self.select_space = self.Z_space_list[i]
            #         self.Z_space_list.pop(i)
            #         break

            #     elif i == len(self.Z_space_list) - 1 and not (self.box_status_select(self.corner_list[i][0])):
            #         for i in range(len(self.corner_list)):
            #             if(self.box_status_select(self.corner_list[i][0])):
            #                 self.space_flag = 'C'
            #                 self.select_space = self.corner_list[i]
            #                 self.corner_list.pop(i)
            #                 break

            #             elif i == len(self.corner_list) - 1 and not(self.box_status_select(self.corner_list[i][0])) and (self.Y_V < self.X_V):
            #                 if(self.box_status_select(self.Y_space_list[0])):
            #                     self.space_flag = 'Y'
            #                     self.select_space = self.Y_space_list
            #                 else:
            #                     if(self.box_status_select(self.X_space_list[0])):
            #                         self.space_flag = 'X'
            #                         self.select_space = self.X_space_list

            #                     else:
            #                         self.select_space = None
                                
            #             elif i == len(self.corner_list) - 1 and not(self.box_status_select(self.corner_list[i][0])) and (self.X_V < self.Y_V):
            #                 if(self.box_status_select(self.X_space_list[0])):
            #                     self.space_flag = 'X'
            #                     self.select_space = self.X_space_list
            #                 else:
            #                     if(self.box_status_select(self.Y_space_list[0])):
            #                         self.space_flag = 'Y'
            #                         self.select_space = self.Y_space_list

            #                     else:
            #                         self.select_space = None
            #-------------------------------------------------------------------------------------------------------------            

    #stack box
    def stack_action(self):
        
        self.com_pos = [self.pos[0], self.pos[1], self.pos[2]]
        
        #rotation compensatin
        if (self.ori[0] == pi/2) and (self.ori[1] == 0) and (self.ori[2] == 0):
            self.com_pos[1] = self.com_pos[1] + self.rotation_compensation_W
            
        elif (self.ori[1] == -pi/2) and (self.ori[0] == 0) and (self.ori[2] == 0):
            self.com_pos[0] = self.com_pos[0] + self.rotation_compensation_L

            
        elif (self.ori[2] == -pi/2) and (self.ori[0] == 0) and (self.ori[1] == 0):
            self.com_pos[1] = self.com_pos[1] + self.rotation_compensation_W

        self.box1.stack(self.com_pos, p.getQuaternionFromEuler(self.ori))
        


    #normalize (not use)
    def long_normal(self,num_list):
        for i in num_list:
            for j in range(4):
                if i[0][j] < 0:
                    i[0][j] = 0

    def calculate_mask(self, mask_space):

        mask_space[self.box_pos[0]:self.box_pos[0] + self.box1.L, self.box_pos[1]:self.box_pos[1] + self.box1.W, self.box_pos[2]:self.box_pos[2] + self.box1.H] = -1

        if((self.box_pos[2] + self.box1.H) < self.Bin.H):
            mask_space[self.box_pos[0]:self.box_pos[0] + self.box1.L, self.box_pos[1]:self.box_pos[1] + self.box1.W, self.box_pos[2] + self.box1.H] =1

        for a in range(self.Bin.H - 1):
            for i in range(self.Bin.L):
                for j in range(self.Bin.W):
                    if (mask_space[i][j][a] != -1) and (mask_space[i][j][a + 1] == -1):
                        mask_space[i, j, 0:a+1] = -1

        return mask_space 
    
    def calculate_e_pos(self):

        self.pos_ep1 = [self.box_pos[0], self.box_pos[1] + self.box1.W, self.box_pos[2], 0]
        self.pos_ep2 = [self.box_pos[0] + self.box1.L, self.box_pos[1], self.box_pos[2], 0]
        self.pos_ep3 = [self.box_pos[0], self.box_pos[1], self.box_pos[2] + self.box1.H, 0]

    # def e_pos_min(self):
    #     if((self.pos_ep1[1] == self.bef_ep1[1]) and (self.pos_ep1[2] == self.bef_ep1[2]) and (self.bef_ep1 != self.box_pos)):
    #         self.pos_ep1 = self.bef_ep1

    #     if((self.pos_ep2[0] == self.bef_ep2[0]) and (self.pos_ep2[2] == self.bef_ep2[2]) and (self.bef_ep2 != self.box_pos)):
    #         self.pos_ep2 = self.bef_ep2

    #     if((self.pos_ep3[0] == self.bef_ep3[0]) and (self.pos_ep3[1] == self.bef_ep3[1]) and (self.bef_ep3 != self.box_pos)):
    #         self.pos_ep3 = self.bef_ep3
    
    # (not use)
    def e_pos_min(self):

        temp1 = None
        temp2 = None
        if(len(self.eps) > 0):
            for i in range(len(self.eps)):

                if((self.pos_ep1[0] == self.eps[i][0]) and (self.pos_ep1[1] == self.eps[i][1]) and (self.pos_ep1[2] > self.eps[i][2])):
                    
                    self.pos_ep1 = self.eps[i]
                    self.eps.pop(i)
                    break

            for i in range(len(self.eps)):
                    if((self.pos_ep1[0] > self.eps[i][0]) and (self.pos_ep1[2] == self.eps[i][2])):
                        self.eps_stage.append(self.pos_ep1)
                        self.pos_ep1 = self.eps[i]
                        temp1 = i

            
            if temp1 != None:
                self.eps.pop(temp1)
                    
            for i in range(len(self.eps)):

                if((self.pos_ep2[0] == self.eps[i][0]) and (self.pos_ep2[1] == self.eps[i][1]) and (self.pos_ep2[2] > self.eps[i][2])):
                    self.pos_ep2 = self.eps[i]
                    self.eps.pop(i)

                    break

            for i in range(len(self.eps)):
                if(len(self.eps) > 0):
                    if((self.pos_ep2[1] > self.eps[i][1]) and (self.pos_ep2[2] == self.eps[i][2])):
                        self.eps_stage.append(self.pos_ep2)
                        self.pos_ep2 = self.eps[i]
                        temp2 = i


            if temp2 != None:
                self.eps.pop(temp2)
            
            # if((self.pos_ep3[0] == self.eps[i][0]) and (self.pos_ep3[1] == self.eps[i][1]) and (self.pos_ep3[2] > self.eps[i][2])):
            #     self.pos_ep3 = self.eps[i]
            #     self.eps.pop(i)
            #     break
        

    def decide_stack(self, mask_space, select_pos):
        if((select_pos[0] + self.box1.L <= self.Bin.L) and (select_pos[1] + self.box1.W <= self.Bin.W) and (select_pos[2] + self.box1.H <= self.Bin.H)):
            if((mask_space[select_pos[0]:select_pos[0]+self.box1.L, select_pos[1]:select_pos[1]+self.box1.W, select_pos[2]] == np.ones(shape = (self.box1.L, self.box1.W))).all()):
                if((mask_space[select_pos[0]:select_pos[0]+self.box1.L, select_pos[1]:select_pos[1]+self.box1.W, select_pos[2]:select_pos[2] + self.box1.H] != -1).all()):
                    return True

        return False

    def normal_eps(self, pos):
        flag = True
        # for i in range(len(self.eps)):
        #     if((pos[0] == self.eps[i][0]) and (pos[1] == self.eps[i][1]) and (pos[2] > self.eps[i][2])):
        #         flag = False
        #         break

            # elif((pos[1] == self.eps[i][1]) and (pos[2] == self.eps[i][2]) and (pos[0] > self.eps[i][0])):
            #     flag = False
            #     break

            # elif((pos[0] == self.eps[i][0]) and (pos[2] == self.eps[i][2]) and (pos[1] > self.eps[i][1])):
            #     flag = False
            #     break

        if(flag == True):
            self.eps.append(pos)

    def arrange_eps(self, eps):
        temp = []

        for i in range(len(eps)):
            if(eps[i][0] < self.Bin.L) and (eps[i][1] < self.Bin.W) and (eps[i][2] < self.Bin.H):
                if(self.mask_space[eps[i][0]][eps[i][1]][eps[i][2]] != 1):
                    temp.append(i)

        temp = list(set(temp))
        temp.sort(reverse=True)
        for i in range(len(temp)):            
            eps.pop(temp[i])
        return eps

    def calculate_score(self):
        self.score_space[self.box_pos[0]:self.box_pos[0] + self.box1.L, self.box_pos[1]:self.box_pos[1] + self.box1.W, self.box_pos[2]:self.box_pos[2] + self.box1.H] = -5

        if((self.box_pos[0] + self.box1.L) < self.Bin.L):
            self.score_space[self.box_pos[0] + self.box1.L, self.box_pos[1]:self.box_pos[1] + self.box1.W, self.box_pos[2]:self.box_pos[2] + self.box1.H] += 3

        if((self.box_pos[1] + self.box1.W) < self.Bin.W):
            self.score_space[self.box_pos[0]:self.box_pos[0] + self.box1.L, self.box_pos[1] + self.box1.W, self.box_pos[2]:self.box_pos[2] + self.box1.H] += 3

        if((self.box_pos[2] + self.box1.H) < self.Bin.H):
            self.score_space[self.box_pos[0]:self.box_pos[0] + self.box1.L, self.box_pos[1]:self.box_pos[1] + self.box1.W, self.box_pos[2] + self.box1.H] += 3

    def stack_score(self, score_space):
        return np.sum(score_space[self.box_pos[0]:self.box_pos[0] + self.box1.L, self.box_pos[1]:self.box_pos[1] + self.box1.W, self.box_pos[2]:self.box_pos[2] + self.box1.H])

    def bpos_to_pos(self):
        self.pos = [self.box_pos[0]*0.1 + self.origin_pos[0], self.box_pos[1]*0.1 + self.origin_pos[1], self.box_pos[2]*0.1 + self.origin_pos[2]]

    def select_other_eps(self):

        if self.select_3_flag == False:
            self.cur_action = 1
            self.select_3_flag = True
        self.count_action += 1
        if(self.cur_action < 2):
            self.cur_action += 1
        else:
            self.cur_action = 0
        
        self.select_action(self.cur_action)

    def calculate_eps_score(self):
        
        space_l = 0
        space_w = 0 
        rem_space1_l = 0
        rem_space1_w = 0
        rem_space2_l = 0
        rem_space2_w = 0
        waste_space1 = 0
        waste_space2 = 0
        eps_score = 0

        for i in range (len(self.eps)):
            space_l = 0
            space_w = 0 
            rem_space1_l = 0
            rem_space1_w = 0
            rem_space2_l = 0
            rem_space2_w = 0
            waste_space1 = 0
            waste_space2 = 0
            eps_score = 0

            if self.eps[i][2] == 0:
                # ---bin4------
                #eps_score = -8

                #----bin_2-----
                eps_score = -50

            else:
                #get space_l
                for j in range(self.Bin.L +1 - self.eps[i][0]):
                    if(self.eps[i][0] < self.Bin.L) and (self.eps[i][1] < self.Bin.W) and (self.eps[i][2] < self.Bin.H):
                        if(self.mask_space[self.eps[i][0] + j][self.eps[i][1]][self.eps[i][2]] != 1 ):
                            space_l = j
                            break
                            
                #get space_w
                for k in range(self.Bin.W +1 - self.eps[i][1]):
                    if(self.eps[i][0] < self.Bin.L) and (self.eps[i][1] < self.Bin.W) and (self.eps[i][2] < self.Bin.H):
                        if(self.mask_space[self.eps[i][0] + j-1][self.eps[i][1] + k][self.eps[i][2]] != 1 ):
                            space_w = k
                            break

                #get not real space_l & space_w
                # if(self.eps[i][0] < self.Bin.L) and (self.eps[i][1] < self.Bin.W) and (self.eps[i][2] < self.Bin.H):
                #     if not((self.mask_space[self.eps[i][0]: self.eps[i][0] + space_l, self.eps[i][1]:self.eps[i][1]+space_w, self.eps[i][2]] == 1).all()):

                #         for j in range(self.Bin.W +1 - self.eps[i][1]):
                #             if(self.eps[i][0] < self.Bin.L) and (self.eps[i][1] < self.Bin.W) and (self.eps[i][2] < self.Bin.H):
                #                 if(self.mask_space[self.eps[i][0]][self.eps[i][1] + j][self.eps[i][2]] != 1 ):
                #                     space_w = j
                #                     break

                #         for k in range(self.Bin.L +1 - self.eps[i][0]):
                #             if(self.eps[i][0] < self.Bin.L) and (self.eps[i][1] < self.Bin.W) and (self.eps[i][2] < self.Bin.H):
                #                 if(self.mask_space[self.eps[i][0] + k][self.eps[i][1] + j - 1][self.eps[i][2]] != 1 ):
                #                     space_l = k
                #                     break
                # if self.box1.L < space_l:
                #     eps_l = space_l - self.box1.L

                # else:
                #     eps_l = self.box1.L - space_l

                # if self.box1.W < space_w:
                #     eps_w = space_w - self.box1.Wself.box_list.append([self.box1.L self.box1.W self.box1.H])


            if self.box1.L <= space_l and self.box1.W <= space_w and self.eps[i][2] != 0:
                
                if space_l - self.box1.L >= space_w - self.box1.W:
                    rem_space1_l = space_l - self.box1.L
                    rem_space1_w = space_w
                    rem_space2_l = self.box1.L
                    rem_space2_w = space_w - self.box1.W
                
                else:
                    rem_space1_l = space_l - self.box1.L
                    rem_space1_w = self.box1.W
                    rem_space2_l = space_l
                    rem_space2_w = space_w - self.box1.W

                for j in range(len(self.box_list)):
                    if(self.box_list[j][0] <= rem_space1_l and self.box_list[j][1] <= rem_space1_w):
                        waste_space1 = 0
                        eps_score += -1
                        break

                    waste_space1 = rem_space1_l * rem_space1_w

                for j in range(len(self.box_list)):
                    if(self.box_list[j][0] <= rem_space2_l and self.box_list[j][1] <= rem_space2_w):
                        waste_space2 = 0
                        eps_score += -1
                        break

                    waste_space2 = rem_space2_l * rem_space2_w

                eps_score += (waste_space1 + waste_space2) * -5

            elif (self.box1.L > space_l or self.box1.W > space_w) and self.eps[i][2] != 0:
                eps_score = -100
            

            self.eps[i][3] = eps_score

        self.eps = list(set(tuple(t) for t in self.eps))
        self.eps = list(list(t) for t in self.eps)
        self.eps = sorted(self.eps, key=lambda x:x[3], reverse = True)         

    def del_fake_eps(self):
        temp = []
        for i in range(len(self.eps_stage)):
            if(self.eps_stage[i][0] < self.Bin.L) and (self.eps_stage[i][1] < self.Bin.W) and (self.eps_stage[i][2] < self.Bin.H) :

                if((self.eps_stage[i][0] == 0) or (self.eps_stage[i][1] == 0)):
                    self.eps.append(self.eps_stage[i])
                    temp.append(i)


                elif((self.mask_space[self.eps_stage[i][0] -1][self.eps_stage[i][1]][self.eps_stage[i][2]] == -1) and (self.mask_space[self.eps_stage[i][0]][self.eps_stage[i][1]-1][self.eps_stage[i][2]] == -1)):
                    self.eps.append(self.eps_stage[i])
                    temp.append(i)
                
                elif((self.mask_space[self.eps_stage[i][0] -1][self.eps_stage[i][1]][self.eps_stage[i][2]] == -1) and (self.mask_space[self.eps_stage[i][0]][self.eps_stage[i][1]][self.eps_stage[i][2] -1] == -1)):
                    self.eps.append(self.eps_stage[i])
                    temp.append(i)

                elif((self.mask_space[self.eps_stage[i][0]][self.eps_stage[i][1] -1][self.eps_stage[i][2]] == -1) and (self.mask_space[self.eps_stage[i][0]][self.eps_stage[i][1]][self.eps_stage[i][2] -1] == -1)):
                    self.eps.append(self.eps_stage[i])
                    temp.append(i)
                   
        
        temp = list(set(temp))
        temp.sort(reverse=True)
        for i in range(len(temp)):
            self.eps_stage.pop(temp[i])

    def init_score_space(self):
        unit_L = int(self.Bin.L / 5)
        unit_W = int(self.Bin.W / 5)
        self.score_space[0:unit_L,:,:] = 5
        self.score_space[unit_L:self.Bin.L, 0:unit_W,:] = 5
        self.score_space[unit_L:2*unit_L, unit_W:self.Bin.W,:] = 4
        self.score_space[2*unit_L:self.Bin.L, unit_W:2*unit_W,:] = 4
        self.score_space[2*unit_L:3*unit_L,2*unit_W:self.Bin.W,:] = 3
        self.score_space[3*unit_L:self.Bin.L,2*unit_W:3*unit_W,:] = 3
        self.score_space[3*unit_L:4*unit_L,3*unit_W:self.Bin.W,:] = 2
        self.score_space[4*unit_L:self.Bin.L,3*unit_W:4*unit_W,:] = 2
        self.score_space[4*unit_L:self.Bin.L,4*unit_W:self.Bin.W,:] = 1

    def init_eps_ground(self):
        for i in range (self.Bin.L):
            for j in range (self.Bin.W):
                self.eps_ground.append([i,j,0,0]) 
        self.eps_ground.sort(key=lambda x:x[1])
        self.eps_ground.sort(key=lambda x:x[0])

    def select_non_eps(self):
        for j in range(len(self.eps_stage)):
            self.success_stack = self.decide_stack(self.mask_space, self.eps_stage[j])

            if(self.success_stack):
                self.box_pos = self.eps_stage[j]
                self.eps_stage.pop(j)
                self.eps_stage.append(self.pos_ep1)
                self.eps_stage.append(self.pos_ep2)
                self.normal_eps(self.pos_ep3)
                break

        if (not self.success_stack):
            for k in range(len(self.eps_ground)):
                self.success_stack = self.decide_stack(self.mask_space, self.eps_ground[k])

                if(self.success_stack):
                    self.box_pos = self.eps_ground[k]
                    self.eps_ground.pop(k)
                    self.eps_stage.append(self.pos_ep1)
                    self.eps_stage.append(self.pos_ep2)
                    self.normal_eps(self.pos_ep3)
                    break

    def calculate_waste_bottom(self):
        # get waste bottom space
        count = 0
        for l in self.mask_space[:,:,0]:
            for v in l:
                if v == 1:
                    count+=1
        return count

    def calculate_waste_space(self):
        waste_space_ratio = -20
        space_l = 0
        space_w = 0
        space_l_ep2 = 0
        space_w_ep2 = 0 
        space_l_ep1 = 0 
        space_w_ep1 = 0 
        rem_space1_l = 0
        rem_space2_w = 0
        waste_space1 = 0
        waste_space2 = 0

        # if(self.box_pos[2] != 0):
        #     #get space_l
        #     for j in range(self.Bin.L - self.pos_ep2[0]):
        #         if(self.pos_ep2[0] < self.Bin.L) and (self.pos_ep2[1] < self.Bin.W) and (self.pos_ep2[2] < self.Bin.H):
        #             if(self.mask_space[self.pos_ep2[0] + j][self.pos_ep2[1]][self.pos_ep2[2]] == 1 ):
        #                 space_l = j

        #     #get space_w
        #     for k in range(self.Bin.W - self.pos_ep1[1]):
        #         if(self.pos_ep1[0] < self.Bin.L) and (self.pos_ep1[1] < self.Bin.W) and (self.pos_ep1[2] < self.Bin.H):
        #             if(self.mask_space[self.pos_ep1[0] + space_l -1][self.pos_ep1[1] + k][self.pos_ep1[2]] == 1 ):
        #                 space_w = k
            
        #     if rem_space1_l >= rem_space1_w:
        #             rem_space1_l = space_l + 1
        #             rem_space1_w = self.box1.W + space_w + 1
        #             rem_space2_l = self.box1.L
        #             rem_space2_w = space_w + 1
                
        #     else:
        #         rem_space1_l = space_l + 1
        #         rem_space1_w = self.box1.W
        #         rem_space2_l = space_l + 1 + self.box1.L
        #         rem_space2_w = space_w + 1

        #     for j in range(len(self.box_list)):
        #         if(self.box_list[j][0] <= rem_space1_l and self.box_list[j][1] <= rem_space1_w):
        #             waste_space1 = 0
        #             break

        #         waste_space1 = rem_space1_l * rem_space1_w

        #     for j in range(len(self.box_list)):
        #         if(self.box_list[j][0] <= rem_space2_l and self.box_list[j][1] <= rem_space2_w):
        #             waste_space2 = 0
        #             break

        #         waste_space2 = rem_space2_l * rem_space2_w
            
        if(self.box_pos[2] == 0):
            for a in range (self.pos_ep2[1]):
                if(self.pos_ep2[0] < self.Bin.L) and (self.pos_ep2[1] < self.Bin.W) and (self.pos_ep2[2] < self.Bin.H):
                    if(self.mask_space[self.pos_ep2[0]-1][self.pos_ep2[1] -a -1][self.pos_ep2[2]] != -1 ):
                        space_w_ep2 = a + 1
            
            for k in range (self.pos_ep2[0]):
                if(self.pos_ep2[0] < self.Bin.L) and (self.pos_ep2[1] < self.Bin.W) and (self.pos_ep2[2] < self.Bin.H):
                    if(self.mask_space[self.pos_ep2[0] - k -1][self.pos_ep2[1] - space_w_ep2 -1][self.pos_ep2[2]] != -1 ):
                        space_l_ep2 = k + 1
            
            waste_space1 = space_w_ep2 * space_l_ep2 

            for j in range (self.pos_ep1[0]):
                if(self.pos_ep1[0] < self.Bin.L) and (self.pos_ep1[1] < self.Bin.W) and (self.pos_ep1[2] < self.Bin.H):
                    if(self.mask_space[self.pos_ep1[0] -j -1][self.pos_ep1[1]-1][self.pos_ep1[2]] != -1 ):
                        space_w_ep1 = j + 1
            
            for k in range (self.pos_ep1[1]):
                if(self.pos_ep1[0] < self.Bin.L) and (self.pos_ep1[1] < self.Bin.W) and (self.pos_ep1[2] < self.Bin.H):
                    if(self.mask_space[self.pos_ep1[0] -space_w_ep1 -1][self.pos_ep1[1] -k -1][self.pos_ep1[2]] != -1 ):
                        space_l_ep1 = k + 1
            
            waste_space2 = space_w_ep1 * space_l_ep1

        waste_space = waste_space1 + waste_space2


        return waste_space * waste_space_ratio

    def decide_non_full_sup(self, mask_space, select_pos):
        box_l_center = 0
        box_w_center = 0

        box_l_center = self.odd_even(self.box1.L)
        box_w_center = self.odd_even(self.box1.W)

        center_pos = [select_pos[0] + box_l_center, select_pos[1] + box_w_center, select_pos[2]]

        if((select_pos[0] + self.box1.L <= self.Bin.L) and (select_pos[1] + self.box1.W <= self.Bin.W) and (select_pos[2] + self.box1.H <= self.Bin.H)):
            if((mask_space[select_pos[0]:center_pos[0], select_pos[1]:center_pos[1], select_pos[2]] == np.ones(shape = (box_l_center, box_w_center))).all()):
                if((mask_space[select_pos[0]:select_pos[0]+self.box1.L, select_pos[1]:select_pos[1]+self.box1.W, select_pos[2]:select_pos[2] + self.box1.H] != -1).all()):
                    return True
        
        return False

    def odd_even(self, num):
        if (num%2) == 0:
            return int(num/2) + 2
        else:
            return int(num/2) + 2
    

    def non_full_stack(self):
        for j in range(len(self.eps)):
            self.success_stack = self.decide_non_full_sup(self.mask_space, self.eps[j])
            if(self.success_stack):
                self.box_pos = self.eps[j]
                self.eps.pop(j)
                self.eps_stage.append(self.pos_ep1)
                self.eps_stage.append(self.pos_ep2)
                
                # self.normal_eps(self.pos_ep3)
                break
        
    def select_action(self, action):
        # if (self.count == 1) :
        #         action = action%3
                

        if (action == 0): 
            self.success_stack = self.decide_stack(self.mask_space, self.pos_ep1)
            if (self.success_stack):
                self.eps_stage.append(self.pos_ep2)
                # self.normal_eps(self.pos_ep3)
                self.box_pos = self.pos_ep1
        
        if (action == 1):
            self.success_stack = self.decide_stack(self.mask_space, self.pos_ep2)
            if (self.success_stack):
                self.box_pos = self.pos_ep2
                self.eps_stage.append(self.pos_ep1)
                # self.normal_eps(self.pos_ep3)

        # if (action == 2):
        #     self.success_stack = self.decide_stack(self.mask_space, self.pos_ep3)
        #     if (self.success_stack):
        #         self.box_pos = self.pos_ep3
        #         self.eps_stage.append(self.pos_ep1)
        #         self.eps_stage.append(self.pos_ep2)
        
        if (action == 2):
            for j in range(len(self.eps)):
                self.success_stack = self.decide_stack(self.mask_space, self.eps[j])
                if(self.success_stack):
                    self.box_pos = self.eps[j]
                    self.eps.pop(j)
                    self.eps_stage.append(self.pos_ep1)
                    self.eps_stage.append(self.pos_ep2)
                    # self.normal_eps(self.pos_ep3)
                    break

            # if((not self.success_stack) and (j == len(self.eps)-1)):
            #     for j in range(len(self.eps_stage)):
            #         self.success_stack = self.decide_stack(self.mask_space, self.eps_stage[j])

            #         if(self.success_stack):
            #             self.box_pos = self.eps_stage[j]
            #             self.eps_stage.pop(j)
            #             self.eps_stage.append(self.pos_ep1)
            #             self.eps_stage.append(self.pos_ep2)
            #             self.normal_eps(self.pos_ep3)
            #             break
                   
                    
                # if(j > len(self.eps)):
                #     break

        self.cur_action = action
