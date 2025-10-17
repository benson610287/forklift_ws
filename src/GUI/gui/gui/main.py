
import sys
from interface.msg import ShelfState
# from interface.srv import Maincontroller
from gui_interface.srv import Taskcmd
import rclpy
from rclpy.node import Node

from threading import Thread,Event
from gui.main_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


from std_msgs.msg import Int32,Float32MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2,time,queue



class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(Taskcmd, 'taskcmd')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Taskcmd.Request()
        self.tasklist=queue.Queue()
        self.res=Taskcmd.Response()
        self.bridge = CvBridge()
        # self.order=list()
        self.shelf_pose_camera_tmp=None
        self.pallet_monitor_camera_tmp=None
        self.docking_camera_tmp=None
        self.pallet_camera_tmp=None
        # image data
        
        # #call slam
        # self.slam_pos_pub=self.create_publisher(Float32MultiArray, '/timda_nav_pose', 10)  #not done
        # self.slam_status_sub=self.create_subscription(
        #     Int32, 
        #     '/timda_nav_success',
        #     self.slam_callback,
        #     10)





        
        # self.shelf_status_sub=self.create_subscription(
        #     ShelfState,
        #     '/shelf/state',
        #     self.pallet_camera_callback,
        #     10)

        



        self.future=None

    
        self.current_task=None
        self.all_thread_flag=True

        self.auto_thread=Thread(target=self.send_auto)
        self.auto_event=Event()
        self.auto_thread.daemon = True 
        self.auto_thread.start()

        self.parking_thread=Thread(target=self.send_parking)
        self.parking_event=Event()
        self.parking_thread.daemon = True 
        self.parking_thread.start()

        self.slam_thread=Thread(target=self.send_slam)
        self.slam_event=Event()
        self.slam_thread.daemon = True 
        self.slam_thread.start()

        self.palleting_thread=Thread(target=self.send_palleting)
        self.palleting_event=Event()
        self.palleting_thread.daemon = True 
        self.palleting_thread.start()

        self.task2_start_thread=Thread(target=self.send_start_positioning)
        self.task2_close_thread=Thread(target=self.send_close_positioning)
        self.task2_start_event=Event()
        self.task2_close_event=Event()
        self.task2_start_thread.daemon = True 
        self.task2_close_thread.daemon = True 
        self.task2_start_thread.start()
        self.task2_close_thread.start()

        self.docking_thread = Thread(target=self.send_start_docking)
        self.docking_event=Event()
        self.docking_thread.daemon = True 
        self.docking_thread.start()

        self.shelf_docking_thread = Thread(target=self.send_shelf_docking)
        self.shelf_docking_event=Event()
        self.shelf_docking_thread.daemon = True 
        self.shelf_docking_thread.start()








        self.ros_thread = Thread(target=rclpy.spin, args=(self,))
        self.ros_thread.daemon = True 
        self.ros_thread.start()

        self.shelf_pose_camera_thread = Thread(target=self.start_shelf_pose_camera)
        self.shelf_pose_camera_event=Event()
        self.shelf_pose_camera_thread.daemon = True 
        self.shelf_pose_camera_thread.start()

        self.pallet_monitor_camera_thread = Thread(target=self.start_pallet_monitor_camera)
        self.pallet_monitor_camera_event=Event()
        self.pallet_monitor_camera_thread.daemon = True 
        self.pallet_monitor_camera_thread.start()

        self.docking_camera_thread = Thread(target=self.start_docking_camera)
        self.docking_camera_event=Event()
        self.docking_camera_thread.daemon = True 
        self.docking_camera_thread.start()

        self.pallet_camera_thread = Thread(target=self.start_pallet_camera)
        self.pallet_camera_event=Event()
        self.pallet_camera_thread.daemon = True 
        self.pallet_camera_thread.start()



        self.slam_success = 888


        self.app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.ui.task1.clicked.connect(self.palleting)
        self.ui.task2_open.clicked.connect(self.positioning_open)
        self.ui.task2_close.clicked.connect(self.positioning_close)
        self.ui.task3.clicked.connect(self.docking)
        self.ui.task4.clicked.connect(self.shelf_docking)
        self.ui.task5.clicked.connect(self.task5)
        self.ui.task6.clicked.connect(self.task6)
        self.ui.open_camera.clicked.connect(self.auto)
        self.ui.exit.clicked.connect(self.exit)


        
        self.test_event=Event()
        self.ss_event=Event()

        self.subscription_shelf_pose = self.create_subscription(
            Image,
            '/camera/depth/state_image',
            self.shelf_pose_camera_callback,
            10)
        

        # self.subscription_pallet_monitor = self.create_subscription(
        #     Image,
        #     'camera/color/azure_image',
        #     self.pallet_monitor_camera_callback,
        #     10)
        
        self.subscription_docking = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.pallet_monitor_camera_callback,
            10)
        self.subscription_pallet = self.create_subscription(
            Image,
            'camera/Armcamera/color/image_raw',
            self.docking_camera_callback,
            10)



        MainWindow.show()
        sys.exit(self.app.exec_())
        # sys.exit(0)
        
    
    def send_auto(self):
        while self.all_thread_flag:
            self.auto_event.wait()
            self.auto_event.clear()
            if not self.all_thread_flag:
                break
            print("doing auto")
            print()
            self.tasklist.put("slam")
            self.tasklist.put("parking")
            self.tasklist.put("palleting")
            self.tasklist.put("slam")
            self.tasklist.put("slam")
            self.tasklist.put("docking")
            self.tasklist.put("start_positioning")
            self.tasklist.put("shelf_docking")
            self.tasklist.put("close_positioning")
            self.tasklist.put("slam")
            # self.ui.tasklist.addItem("palleting")
            # self.ui.tasklist.addItem("positioning")
            # self.ui.tasklist.addItem("docking")
            # self.ui.tasklist.addItem("shelf_docking")
            while True:
                self.current_task=self.tasklist.get()
                print("doing " + self.current_task)
                self.res.state=0
                if self.current_task=="slam":
                    self.slam_event.set()
                    # while self.res.state!=1:
                    #     time.sleep(0.01)
                    self.test_event.wait()
                    self.test_event.clear()

                elif self.current_task=="parking":
                    self.parking_event.set()
                    # while self.res.state!=1:
                    #     time.sleep(0.01)
                    self.test_event.wait()
                    self.test_event.clear()
                elif self.current_task=="palleting":
                    self.palleting_event.set()
                    # while self.res.state!=1:
                    #     time.sleep(0.01)
                    self.test_event.wait()
                    self.test_event.clear()
                elif self.current_task=="docking":
                    self.docking_event.set()
                    # while self.res.state!=1:
                    #     time.sleep(0.01)
                    self.test_event.wait()
                    self.test_event.clear()
                elif self.current_task=="start_positioning":
                    self.task2_start_event.set()
                    # while self.res.state!=1:
                    #     time.sleep(0.01)
                    self.test_event.wait()
                    self.test_event.clear()
                elif self.current_task=="shelf_docking":
                    self.shelf_docking_event.set()
                    # while self.res.state!=1:
                    #     time.sleep(0.01)
                    self.test_event.wait()
                    self.test_event.clear()
                elif self.current_task=="close_positioning":
                    self.task2_close_event.set()
                    # while self.res.state!=1:
                    #     time.sleep(0.01)
                    self.test_event.wait()
                    self.test_event.clear()



                if self.tasklist.empty():
                    break



                







            # self.res.state=0
            # self.palleting_event.set()
            # while self.res.state!=1:
            #     time.sleep(0.01)
            # self.res.state=3
            # self.task2_start_event.set()
            # while self.res.state!=0:  #Activate
            #     if self.res.state==2:  #same mode
            #         break
            #     else:
            #         time.sleep(0.01)
            # self.res.state=0
            # self.docking_event.set()
            # while self.res.state!=1:
            #     time.sleep(0.01)
            # self.res.state=0
            # self.shelf_docking_event.set()
            # while self.res.state!=1:
            #     time.sleep(0.01)
            # self.res.state=0
            # self.task2_close_event.set()
            # while self.res.state!=1:  # Deactivate
            #     if self.res.state==2: #same mode
            #         break
            #     else:
            #         time.sleep(0.01)



        

    def auto(self):
        self.ui.tasklist.clear()
        # self.ui.tasklist.addItem("task1")
        self.auto_event.set()




    def send_palleting(self):
        # while self.all_thread_flag:
        #     self.palleting_event.wait()
        #     self.palleting_event.clear()
        #     if not self.all_thread_flag:
        #         break
        #     # self.current_task=self.tasklist.get()
        #     print("doing " + self.current_task)
        #     self.ui.tasklist.addItem(self.current_task)
        #     self.req.task=self.current_task
        #     self.future = self.cli.call_async(self.req)
        #     self.future.add_done_callback(self.palleting_response_callback)
        #     print("done " + self.current_task)
        #     print()
        while self.all_thread_flag:
            if not self.all_thread_flag:
                break
            if self.current_task == "palleting":
                print("doing " + self.current_task)
                self.ui.tasklist.addItem("doing " + self.current_task)
                self.req.task=self.current_task
                self.future = self.cli.call_async(self.req)
                input(f"{self.current_task} need input")
                self.palleting_response_callback(self.future)
                print("done pallet")
                print()
            else:
                pass
    def palleting_response_callback(self, future):
        # try:
        #     self.res = future.result()
        #     print("pallet res=",self.res.state)
        #     if self.res.state==1:
        #         self.ui.tasklist.addItem(self.current_task+" complete")
        #     else:
        #         self.ui.tasklist.addItem(self.current_task+" fail")
        # except Exception as e:
        #     print(f"[ERROR] 服務回應錯誤: {e}")
        print("----------------+++++++++++++++++++========================yuuurgsdfgfdshfdsfsddfsgfd")
        self.test_event.set()
        self.ui.tasklist.addItem(self.current_task+" complete")
        self.current_task=None

    def palleting(self):
        self.ui.tasklist.clear()
        self.tasklist.put("palleting")
        self.palleting_event.set()




    def send_start_positioning(self):
        # while self.all_thread_flag:
        #     self.task2_start_event.wait()
        #     self.task2_start_event.clear()
        #     if not self.all_thread_flag:
        #         break
        #     # self.current_task=self.tasklist.get()
        #     print("doing " + self.current_task)
        #     self.ui.tasklist.addItem(self.current_task)
        #     self.req.task=self.current_task
        #     self.future = self.cli.call_async(self.req)
        #     self.future.add_done_callback(self.task2_response_callback)
        #     print("done " + self.current_task)
        #     print()

        while self.all_thread_flag:
            if not self.all_thread_flag:
                break
            if self.current_task == "start_positioning":
                print("doing " + self.current_task)
                self.ui.tasklist.addItem("doing " + self.current_task)
                self.req.task=self.current_task
                self.future = self.cli.call_async(self.req)
                input(f"{self.current_task} need input")
                self.task2_response_callback(self.future)
                print("done start_positioning")
                print()
            else:
                pass


    def send_close_positioning(self):
        # while self.all_thread_flag:
        #     self.task2_close_event.wait()
        #     self.task2_close_event.clear()
        #     if not self.all_thread_flag:
        #         break
        #     # self.current_task=self.tasklist.get()
        #     print("doing " + self.current_task)
        #     self.ui.tasklist.addItem(self.current_task)
        #     self.req.task=self.current_task 
        #     self.future = self.cli.call_async(self.req)
        #     self.future.add_done_callback(self.task2_response_callback)
        #     print("done " + self.current_task)
        #     print()
        while self.all_thread_flag:
            if not self.all_thread_flag:
                break
            if self.current_task == "close_positioning":
                print("doing " + self.current_task)
                self.ui.tasklist.addItem("doing " + self.current_task)
                self.req.task=self.current_task
                self.future = self.cli.call_async(self.req)
                input(f"{self.current_task} need input")
                self.task2_response_callback(self.future)
                print("done close_positioning")
                print()
            else:
                pass
    def task2_response_callback(self, future):
        # try:
        #     self.res = future.result()
        #     print("positioning res=",self.res.state)
        #     if self.res.state==0:
        #         self.ui.tasklist.addItem(self.current_task + " complete")   #open
        #     elif self.res.state==1:
        #         self.ui.tasklist.addItem(self.current_task + " complete")   #close
        #     elif self.res.state==2:
        #         self.ui.tasklist.addItem(self.current_task + " command error")
        #     else:
        #         self.ui.tasklist.addItem(self.current_task + " fail")
        # except Exception as e:
        #     print(f"[ERROR] 服務回應錯誤: {e}")
        print("----------------+++++++++++++++++++========================yuuurgsdfgfdshfdsfsddfsgfd")
        self.test_event.set()
        self.ui.tasklist.addItem(self.current_task+" complete")
        self.current_task=None

    def positioning_open(self):
        self.ui.tasklist.clear()
        self.tasklist.put("start_positioning")
        self.task2_start_event.set()

    def positioning_close(self):
        self.ui.tasklist.clear()
        self.tasklist.put("close_positioning")
        self.task2_close_event.set()


    def send_parking(self):
        # while self.all_thread_flag:
        #     self.parking_event.wait()
        #     self.parking_event.clear()
        #     if not self.all_thread_flag:
        #         break
        #     # self.current_task=self.tasklist.get()
        #     print("doing " + self.current_task)
        #     self.ui.tasklist.addItem(self.current_task)
        #     self.req.task=self.current_task
        #     self.future = self.cli.call_async(self.req)
        #     self.future.add_done_callback(self.parking_response_callback)
        #     print("done " + self.current_task)
        #     print()
        while self.all_thread_flag:
            if not self.all_thread_flag:
                break
            if self.current_task == "parking":
                print("doing " + self.current_task)
                self.ui.tasklist.addItem("doing " + self.current_task)
                self.req.task=self.current_task
                self.future = self.cli.call_async(self.req)
                input(f"{self.current_task} need input")
                self.parking_response_callback(self.future)
                print("done parking")
                print()
            else:
                pass

    def parking_response_callback(self, future):
        # try:
        #     self.res = future.result()
        #     print("parking res=",self.res.state)
        #     if self.res.state==1:
        #         self.ui.tasklist.addItem(self.current_task+" complete")
        #     else:
        #         self.ui.tasklist.addItem(self.current_task+" fail")
        # except Exception as e:
        #     print(f"[ERROR] 服務回應錯誤: {e}")
        print("----------------+++++++++++++++++++========================yuuurgsdfgfdshfdsfsddfsgfd")
        self.test_event.set()
        self.ui.tasklist.addItem(self.current_task+" complete")
        self.current_task=None

    def palleting(self):
        self.ui.tasklist.clear()
        self.tasklist.put("parking")
        self.palleting_event.set()

    def send_slam(self):
        while self.all_thread_flag:
            if not self.all_thread_flag:
                break
            if self.current_task == "slam":
                print("doing " + self.current_task)
                self.ui.tasklist.addItem("doing " + self.current_task)
                self.req.task=self.current_task
                self.future = self.cli.call_async(self.req)
                input(f"{self.current_task} need input")
                self.slam_response_callback(self.future)
                print("done slam")
                print()
            else:
                pass

    def slam_response_callback(self, future):
        print("----------------+++++++++++++++++++========================yuuurgsdfgfdshfdsfsddfsgfd")
        self.test_event.set()
        self.ui.tasklist.addItem(self.current_task+" complete")
        self.current_task=None

    def slam(self):
        self.ui.tasklist.clear()
        self.tasklist.put("slam")
        self.slam_event.set()


    # def send_slam(self):
    #     while self.all_thread_flag:
    #         # self.slam_event.wait()
    #         # self.slam_event.clear()
    #         if not self.all_thread_flag:
    #             break
    #         # self.current_task=self.tasklist.get()
    #         if self.current_task == "slam":
    #             print("doing " + self.current_task)
    #             self.ui.tasklist.addItem("doing " + self.current_task)
    #             self.req.task=self.current_task
    #             self.future = self.cli.call_async(self.req)
    #             # self.future.add_done_callback(self.slam_response_callback)
    #             input()
    #             self.slam_response_callback(self.future)
                
                

    #             print("done slam")
    #             print()
    #         else:
    #             pass

    # def slam_response_callback(self, future):
    #     print("----------------+++++++++++++++++++========================yuuurgsdfgfdshfdsfsddfsgfd")
    #     # try:
    #     #     res = future.result()
    #     #     print("slam res=",res.state)
    #     #     if res.state==1:
    #     #         self.test_event.set()
    #     #         self.ui.tasklist.addItem(self.current_task+" complete")
    #     #     else:
    #     #         self.ui.tasklist.addItem(self.current_task+" fail")
    #     # except Exception as e:
    #     #     print(f"[ERROR] 服務回應錯誤: {e}")
    #     self.test_event.set()
    #     self.ui.tasklist.addItem(self.current_task+" complete")
    #     # self.ui.tasklist.addItem(self.current_task+" fail")
    #     self.current_task=None

    # def slam(self):
    #     self.ui.tasklist.clear()
    #     self.tasklist.put("slam")
    #     self.slam_event.set()





    # def task2(self):
    #     self.ui.tasklist.clear()
    #     self.ui.tasklist.addItem("task2")
    #     print("bb")
    #     self.req.task="task2"
    #     self.future = self.cli.call_async(self.req)
    #     rclpy.spin_until_future_complete(self, self.future)
    #     res=self.future.result()
    #     print(res.state)
    #     if res.state==1:
    #         self.ui.tasklist.addItem("task2 complete")
    #     else:
    #         self.ui.tasklist.addItem("task2 fail")
    # def task3(self):
    #     self.ui.tasklist.clear()
    #     self.ui.tasklist.addItem("task3")
    #     print("cc")
    #     self.req.task="task3"
    #     self.future = self.cli.call_async(self.req)
    #     rclpy.spin_until_future_complete(self, self.future)
    #     res=self.future.result()
    #     print(res.state)
    #     if res.state==1:
    #         self.ui.tasklist.addItem("task3 complete")
    #     else:
    #         self.ui.tasklist.addItem("task3 fail")
    
    def send_start_docking(self):
        # while self.all_thread_flag:
        #     self.docking_event.wait()
        #     self.docking_event.clear()
        #     if not self.all_thread_flag:
        #         break
        #     # self.current_task=self.tasklist.get()
        #     print("doing " + self.current_task)
        #     self.ui.tasklist.addItem(self.current_task)
        #     self.req.task=self.current_task
        #     self.future = self.cli.call_async(self.req)
        #     self.future.add_done_callback(self.docking_response_callback)
        #     print("done " + self.current_task)
        #     print()
        while self.all_thread_flag:
            if not self.all_thread_flag:
                break
            if self.current_task == "docking":
                print("doing " + self.current_task)
                self.ui.tasklist.addItem("doing " + self.current_task)
                self.req.task=self.current_task
                self.future = self.cli.call_async(self.req)
                input(f"{self.current_task} need input")
                self.docking_response_callback(self.future)
                print("done docking")
                print()
            else:
                pass
    def docking_response_callback(self, future):
        # try:
        #     self.res = future.result()
        #     print("docking res=",self.res.state)
        #     if self.res.state==1:
        #         self.ui.tasklist.addItem(self.current_task + " complete")
        #     else:
        #         self.ui.tasklist.addItem(self.current_task + " fail")
        # except Exception as e:
        #     print(f"[ERROR] 服務回應錯誤: {e}")
        print("----------------+++++++++++++++++++========================yuuurgsdfgfdshfdsfsddfsgfd")
        self.test_event.set()
        self.ui.tasklist.addItem(self.current_task+" complete")
        self.current_task=None

    def docking(self):
        self.ui.tasklist.clear()
        self.tasklist.put("docking")
        self.docking_event.set()




    def send_shelf_docking(self):
        # while self.all_thread_flag:
        #     self.shelf_docking_event.wait()
        #     self.shelf_docking_event.clear()
        #     if not self.all_thread_flag:
        #         break
        #     # self.current_task=self.tasklist.get()
        #     print("doing " + self.current_task)
        #     self.ui.tasklist.addItem(self.current_task)
        #     self.req.task=self.current_task
        #     self.future = self.cli.call_async(self.req)
        #     self.future.add_done_callback(self.docking_response_callback)
        #     print("done " + self.current_task)
        #     print()
        while self.all_thread_flag:
            if not self.all_thread_flag:
                break
            if self.current_task == "shelf_docking":
                print("doing " + self.current_task)
                self.ui.tasklist.addItem("doing " + self.current_task)
                self.req.task=self.current_task
                self.future = self.cli.call_async(self.req)
                input(f"{self.current_task} need input")
                self.docking_response_callback(self.future)
                print("done shelf_docking")
                print()
            else:
                pass
    def shelf_docking_response_callback(self, future):
        # try:
        #     self.res = future.result()
        #     print("shelf_docking res=",self.res.state)
        #     if self.res.state==1:
        #         self.ui.tasklist.addItem(self.current_task + " complete")
        #     else:
        #         self.ui.tasklist.addItem(self.current_task + " fail")
        # except Exception as e:
        #     print(f"[ERROR] 服務回應錯誤: {e}")
        print("----------------+++++++++++++++++++========================yuuurgsdfgfdshfdsfsddfsgfd")
        self.test_event.set()
        self.ui.tasklist.addItem(self.current_task+" complete")
        self.current_task=None

    def shelf_docking(self):
        self.ui.tasklist.clear()
        self.tasklist.put("shelf_docking")
        self.shelf_docking_event.set()







    def task5(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task5")
        print("ee")
        self.req.task="task5"
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        res=self.future.result()
        print(res.state)
        if res.state==1:
            self.ui.tasklist.addItem("task5 complete")
        else:
            self.ui.tasklist.addItem("task5 fail")
    def task6(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task6")
        print("ff")
        self.req.task="task6"
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        res=self.future.result()
        print(res.state)
        if res.state==1:
            self.ui.tasklist.addItem("task6 complete")
        else:
            self.ui.tasklist.addItem("task6 fail")



    def start_shelf_pose_camera(self):
        while self.all_thread_flag:
            self.shelf_pose_camera_event.wait()
            self.shelf_pose_camera_event.clear()
            if not self.all_thread_flag:
                break
            # print("doing camera")
            # self.req.task="task2"
            # self.future = self.cli.call_async(self.req)
            # self.future.add_done_callback(self.task2_response_callback)
            shelf_pose_camera_tmp = cv2.resize(self.shelf_pose_camera_tmp, (300, 200))   # 改變尺寸和視窗相同
            shelf_pose_camera_tmp = cv2.cvtColor(shelf_pose_camera_tmp, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
            height, width, channel = shelf_pose_camera_tmp.shape    # 讀取尺寸和 channel數量
            bytesPerline = channel * width          # 設定 bytesPerline ( 轉換使用 )
            # 轉換影像為 QImage，讓 PyQt5 可以讀取
            img = QtGui.QImage(shelf_pose_camera_tmp, width, height, bytesPerline, QtGui.QImage.Format_RGB888)
            self.ui.shelf_pose_camera.setPixmap(QtGui.QPixmap.fromImage(img))
            # print("done camera")
    def shelf_pose_camera_callback(self,msg):
        self.shelf_pose_camera_tmp=self.bridge.imgmsg_to_cv2(msg,'passthrough')
        self.shelf_pose_camera_event.set()

    def start_pallet_monitor_camera(self):
        while self.all_thread_flag:
            self.pallet_monitor_camera_event.wait()
            self.pallet_monitor_camera_event.clear()
            if not self.all_thread_flag:
                break
            # print("doing pallet_monitor_camera")
            pallet_monitor_camera_tmp = cv2.resize(self.pallet_monitor_camera_tmp, (300, 200))   # 改變尺寸和視窗相同
            pallet_monitor_camera_tmp = cv2.cvtColor(pallet_monitor_camera_tmp, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
            height, width, channel = pallet_monitor_camera_tmp.shape    # 讀取尺寸和 channel數量
            bytesPerline = channel * width          # 設定 bytesPerline ( 轉換使用 )
            # 轉換影像為 QImage，讓 PyQt5 可以讀取
            img = QtGui.QImage(pallet_monitor_camera_tmp, width, height, bytesPerline, QtGui.QImage.Format_RGB888)
            self.ui.pallet_monitor_camera.setPixmap(QtGui.QPixmap.fromImage(img))
            # print("done pallet_monitor_cmaera")
    def pallet_monitor_camera_callback(self,msg):
        self.pallet_monitor_camera_tmp=self.bridge.imgmsg_to_cv2(msg,'bgr8')
        self.pallet_monitor_camera_event.set()


    def start_docking_camera(self):
        while self.all_thread_flag:
            self.docking_camera_event.wait()
            self.docking_camera_event.clear()
            if not self.all_thread_flag:
                break
            # print("doing docking_camera")
            # self.req.task="task2"
            # self.future = self.cli.call_async(self.req)
            # self.future.add_done_callback(self.task2_response_callback)
            docking_camera_tmp = cv2.resize(self.docking_camera_tmp, (300, 200))   # 改變尺寸和視窗相同
            docking_camera_tmp = cv2.cvtColor(docking_camera_tmp, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
            height, width, channel = docking_camera_tmp.shape    # 讀取尺寸和 channel數量
            bytesPerline = channel * width          # 設定 bytesPerline ( 轉換使用 )
            # 轉換影像為 QImage，讓 PyQt5 可以讀取
            img = QtGui.QImage(docking_camera_tmp, width, height, bytesPerline, QtGui.QImage.Format_RGB888)
            self.ui.docking_camera.setPixmap(QtGui.QPixmap.fromImage(img))
            # print("done docking_cmaera")
        
    def docking_camera_callback(self,msg):
        self.docking_camera_tmp=self.bridge.imgmsg_to_cv2(msg,'bgr8')
        self.docking_camera_event.set()

    def start_pallet_camera(self):
        while self.all_thread_flag:
            self.pallet_camera_event.wait()
            self.pallet_camera_event.clear()
            if not self.all_thread_flag:
                break
            # print("doing pallet_camera")
            pallet_camera_tmp = cv2.resize(self.pallet_camera_tmp, (300, 200))   # 改變尺寸和視窗相同
            pallet_camera_tmp = cv2.cvtColor(pallet_camera_tmp, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
            height, width, channel = pallet_camera_tmp.shape    # 讀取尺寸和 channel數量
            bytesPerline = channel * width          # 設定 bytesPerline ( 轉換使用 )
            # 轉換影像為 QImage，讓 PyQt5 可以讀取
            img = QtGui.QImage(pallet_camera_tmp, width, height, bytesPerline, QtGui.QImage.Format_RGB888)
            self.ui.pallet_camera.setPixmap(QtGui.QPixmap.fromImage(img))
            # print("done pallet_camera")
    def pallet_camera_callback(self,msg):
        self.pallet_camera_tmp=self.bridge.imgmsg_to_cv2(msg,'bgr8')
        self.pallet_camera_event.set()



    









    def exit(self):
        self.all_thread_flag = False

        # 釋放所有事件
        events = [
            self.palleting_event, self.task2_start_event, self.task2_close_event,
            self.docking_event, self.shelf_docking_event,
            self.shelf_pose_camera_event, self.pallet_monitor_camera_event,
            self.docking_camera_event, self.pallet_camera_event,self.auto_event
        ]
        for e in events:
            e.set()

        # 結束所有子執行緒（加 timeout 避免阻塞）
        threads = [
            self.palleting_thread, self.task2_start_thread, self.task2_close_thread,
            self.docking_thread, self.shelf_docking_thread, self.shelf_pose_camera_thread,
            self.pallet_monitor_camera_thread, self.docking_camera_thread, self.pallet_camera_thread,self.auto_thread
        ]
        for t in threads:
            t.join(timeout=2)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        # 關閉 ROS
        self.destroy_node()
        rclpy.shutdown()
        self.ros_thread.join(timeout=2)
        print("===============================================================")
        # 關閉 PyQt 視窗與事件迴圈
        self.app.quit()
        # self.app.exec_()
        print("________________________________________________________________")
        # 最後退出程式
        sys.exit(0)

def main(args=None):
    



    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    # minimal_client.destroy_node()
    # rclpy.shutdown()


if __name__ == '__main__':
    main()