
import sys
from interface.msg import ShelfState
# from interface.srv import Maincontroller
from gui_interface.srv import Taskcmd
import rclpy
from rclpy.node import Node

from threading import Thread,Event
from gui.main_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


from std_msgs.msg import Bool
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
        self.order=list()
        self.shelf_pose_camera_tmp=None
        self.pallet_monitor_camera_tmp=None
        self.docking_camera_tmp=None
        self.pallet_camera_tmp=None
        # image data
        self.subscription_shelf_pose = self.create_subscription(
            Image,
            '/camera/depth/state_image',
            self.shelf_pose_camera_callback,
            10)
        self.subscription_pallet_monitor = self.create_subscription(
            Image,
            'camera/color/image_raw',
            self.pallet_monitor_camera_callback,
            10)
        self.subscription_docking = self.create_subscription(
            Image,
            'camera/color/image_raw',
            self.docking_camera_callback,
            10)
        self.subscription_pallet = self.create_subscription(
            Image,
            'camera/Armcamera/color/image_raw',
            self.pallet_camera_callback,
            10)
        #call slam
        self.slam_pos_pub=self.create_publisher(Image, 'topic', 10)  #not done
        self.slam_status_sub=self.create_subscription(
            Bool,
            '/tmp',
            self.pallet_camera_callback,
            10)
        
        self.shelf_status_sub=self.create_subscription(
            ShelfState,
            '/shelf/state',
            self.pallet_camera_callback,
            10)


        self.all_thread_flag=True

        self.auto_thread=Thread(target=self.start_auto)
        self.auto_event=Event()
        self.auto_event.daemon = True 
        self.auto_thread.start()



        self.task1_thread=Thread(target=self.send_request1)
        self.task1_event=Event()
        self.task1_event.daemon = True 
        self.task1_thread.start()

        self.task2_start_thread=Thread(target=self.send_start_request2)
        self.task2_close_thread=Thread(target=self.send_close_request2)
        self.task2_start_event=Event()
        self.task2_close_event=Event()
        self.task2_start_event.daemon = True 
        self.task2_close_event.daemon = True 
        self.task2_start_thread.start()
        self.task2_close_thread.start()

        self.docking_thread = Thread(target=self.start_docking)
        self.docking_event=Event()
        self.docking_thread.daemon = True 
        self.docking_thread.start()


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

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.ui.task1.clicked.connect(self.task1)
        self.ui.task2_open.clicked.connect(self.task2_open)
        self.ui.task2_close.clicked.connect(self.task2_close)
        self.ui.task3.clicked.connect(self.docking)
        self.ui.task4.clicked.connect(self.task4)
        self.ui.task5.clicked.connect(self.task5)
        self.ui.task6.clicked.connect(self.task6)
        self.ui.open_camera.clicked.connect(self.auto)
        self.ui.exit.clicked.connect(self.exit)

        MainWindow.show()
        sys.exit(app.exec_())
        
    
    def start_auto(self):
        while self.all_thread_flag:
            self.auto_event.wait()
            self.auto_event.clear()
            print("doing auto")
            self.tasklist.put("task1")
            self.tasklist.put("task2")
            self.tasklist.put("docking")
            self.ui.tasklist.addItem("task1")
            self.ui.tasklist.addItem("task2")
            self.ui.tasklist.addItem("docking")
            self.res.state=0
            self.task1_event.set()
            while self.res.state==1:
                time.sleep(0.01)
            self.res.state=0
            self.task2_start_event.set()
            while self.res.state==1:
                time.sleep(0.01)
            self.res.state=0
            self.docking_event.set()
            while self.res.state==1:
                time.sleep(0.01)
            # self.req.task="task1"
            # self.future = self.cli.call_async(self.req)
            # self.future.add_done_callback(self.task1_response_callback)
            # print("done task1")
        

    def auto(self):
        self.ui.tasklist.clear()
        # self.ui.tasklist.addItem("task1")
        self.auto_event.set()




    def send_request1(self):
        while self.all_thread_flag:
            self.task1_event.wait()
            self.task1_event.clear()
            print("doing task1")
            self.req.task="task1"
            self.future = self.cli.call_async(self.req)
            self.future.add_done_callback(self.task1_response_callback)
            print("done task1")
        
    def task1_response_callback(self, future):
        try:
            self.res = future.result()
            print("task1 res=",self.res.state)
            if self.res.state==1:
                self.ui.tasklist.addItem("task1 complete")
            else:
                self.ui.tasklist.addItem("task1 fail")
        except Exception as e:
            print(f"[ERROR] 服務回應錯誤: {e}")

    def task1(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task1")
        self.task1_event.set()




    def send_start_request2(self):
        while self.all_thread_flag:
            self.task2_start_event.wait()
            self.task2_start_event.clear()
            print("starting task2")
            self.req.task="task2_start"
            self.future = self.cli.call_async(self.req)
            self.future.add_done_callback(self.task2_response_callback)
            print("start task2")

    def send_close_request2(self):
        while self.all_thread_flag:
            self.task2_close_event.wait()
            self.task2_close_event.clear()
            print("closing task2")
            self.req.task="task2_close"  #not yet
            self.future = self.cli.call_async(self.req)
            self.future.add_done_callback(self.task2_response_callback)
            print("close task2")
        
    def task2_response_callback(self, future):
        try:
            self.res = future.result()
            print("task2 res=",self.res.state)
            if self.res.state==0:
                self.ui.tasklist.addItem("task2 activated")
            elif self.res.state==1:
                self.ui.tasklist.addItem("task2 deactivate")
            elif self.res.state==2:
                self.ui.tasklist.addItem("task2 command error")
            else:
                self.ui.tasklist.addItem("task2 fail")
        except Exception as e:
            print(f"[ERROR] 服務回應錯誤: {e}")

    def task2_open(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task2_start")
        self.task2_start_event.set()

    def task2_close(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task2_close")
        self.task2_close_event.set()


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
    
    def start_docking(self):
        while self.all_thread_flag:
            self.docking_event.wait()
            self.docking_event.clear()
            print("doing task1")
            self.req.task="docking"
            self.future = self.cli.call_async(self.req)
            self.future.add_done_callback(self.docking_response_callback)
            print("done docking")
        
    def docking_response_callback(self, future):
        try:
            self.res = future.result()
            print("docking res=",self.res.state)
            if self.res.state==1:
                self.ui.tasklist.addItem("docking complete")
            else:
                self.ui.tasklist.addItem("docking fail")
        except Exception as e:
            print(f"[ERROR] 服務回應錯誤: {e}")

    def docking(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("docking")
        self.docking_event.set()




    def task4(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task4")
        print("dd")
        self.req.task="task4"
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        res=self.future.result()
        print(res.state)
        if res.state==1:
            self.ui.tasklist.addItem("task4 complete")
        else:
            self.ui.tasklist.addItem("task4 fail")
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
            print("doing camera")
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
            print("done camera")
    def shelf_pose_camera_callback(self,msg):
        self.shelf_pose_camera_tmp=self.bridge.imgmsg_to_cv2(msg,'bgr8')
        self.shelf_pose_camera_event.set()

    def start_pallet_monitor_camera(self):
        while self.all_thread_flag:
            self.pallet_monitor_camera_event.wait()
            self.pallet_monitor_camera_event.clear()
            print("doing pallet_monitor_camera")
            pallet_monitor_camera_tmp = cv2.resize(self.pallet_monitor_camera_tmp, (300, 200))   # 改變尺寸和視窗相同
            pallet_monitor_camera_tmp = cv2.cvtColor(pallet_monitor_camera_tmp, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
            height, width, channel = pallet_monitor_camera_tmp.shape    # 讀取尺寸和 channel數量
            bytesPerline = channel * width          # 設定 bytesPerline ( 轉換使用 )
            # 轉換影像為 QImage，讓 PyQt5 可以讀取
            img = QtGui.QImage(pallet_monitor_camera_tmp, width, height, bytesPerline, QtGui.QImage.Format_RGB888)
            self.ui.pallet_monitor_camera.setPixmap(QtGui.QPixmap.fromImage(img))
            print("done pallet_monitor_cmaera")
    def pallet_monitor_camera_callback(self,msg):
        self.pallet_monitor_camera_tmp=self.bridge.imgmsg_to_cv2(msg,'bgr8')
        self.pallet_monitor_camera_event.set()
    def start_docking_camera(self):
        while self.all_thread_flag:
            self.docking_camera_event.wait()
            self.docking_camera_event.clear()
            print("doing docking_camera")
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
            print("done docking_cmaera")
        
    def docking_camera_callback(self,msg):
        self.docking_camera_tmp=self.bridge.imgmsg_to_cv2(msg,'bgr8')
        self.docking_camera_event.set()

    def start_pallet_camera(self):
        while self.all_thread_flag:
            self.pallet_camera_event.wait()
            self.pallet_camera_event.clear()
            print("doing pallet_camera")
            pallet_camera_tmp = cv2.resize(self.pallet_camera_tmp, (300, 200))   # 改變尺寸和視窗相同
            pallet_camera_tmp = cv2.cvtColor(pallet_camera_tmp, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
            height, width, channel = pallet_camera_tmp.shape    # 讀取尺寸和 channel數量
            bytesPerline = channel * width          # 設定 bytesPerline ( 轉換使用 )
            # 轉換影像為 QImage，讓 PyQt5 可以讀取
            img = QtGui.QImage(pallet_camera_tmp, width, height, bytesPerline, QtGui.QImage.Format_RGB888)
            self.ui.pallet_camera.setPixmap(QtGui.QPixmap.fromImage(img))
            print("done pallet_camera")
    def pallet_camera_callback(self,msg):
        self.pallet_camera_tmp=self.bridge.imgmsg_to_cv2(msg,'bgr8')
        self.pallet_camera_event.set()















    def exit(self):
        self.all_thread_flag=False
        self.task1_event.set()
        self.task2_start_event.set()
        self.task2_close_event.set()
        self.camera_event.set()

        self.task1_thread.join()
        self.task2_start_thread.join()
        self.task2_close_thread.join()
        self.camera_thread.join()
        rclpy.shutdown()
        self.ros_thread.join()
        sys.exit()


    

def main(args=None):
    



    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()