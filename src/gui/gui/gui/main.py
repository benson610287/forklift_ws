
import sys

from gui_interface.srv import Taskcmd
import rclpy
from rclpy.node import Node

from threading import Thread,Event
from gui.main_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets



from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(Taskcmd, 'taskcmd')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Taskcmd.Request()
        self.tasklist=[]
        self.res=Taskcmd.Response()
        self.bridge = CvBridge()
        self.camera_tmp=None
        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.camera_callback,
            10)



        self.all_thread_flag=True
        self.task1_thread=Thread(target=self.send_request1)
        self.task1_event=Event()
        self.task1_event.daemon = True 
        self.task1_thread.start()

        self.task2_thread=Thread(target=self.send_request2)
        self.task2_event=Event()
        self.task2_event.daemon = True 
        self.task2_thread.start()




        self.ros_thread = Thread(target=rclpy.spin, args=(self,))
        self.ros_thread.daemon = True 
        self.ros_thread.start()

        self.camera_thread = Thread(target=self.start_camera)
        self.camera_event=Event()
        self.camera_thread.daemon = True 
        self.camera_thread.start()

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.ui.task1.clicked.connect(self.task1)
        self.ui.task2.clicked.connect(self.task2)
        self.ui.task3.clicked.connect(self.task3)
        self.ui.task4.clicked.connect(self.task4)
        self.ui.task5.clicked.connect(self.task5)
        self.ui.task6.clicked.connect(self.task6)
        # self.ui.open_camera.clicked.connect(self.start_camera)
        self.ui.exit.clicked.connect(self.exit)

        MainWindow.show()
        sys.exit(app.exec_())
        

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




    def send_request2(self):
        while self.all_thread_flag:
            self.task2_event.wait()
            self.task2_event.clear()
            print("doing task2")
            self.req.task="task2"
            self.future = self.cli.call_async(self.req)
            self.future.add_done_callback(self.task2_response_callback)
            print("done task2")
        
    def task2_response_callback(self, future):
        try:
            self.res = future.result()
            print("task2 res=",self.res.state)
            if self.res.state==0:
                self.ui.tasklist.addItem("task2 activated")
            elif self.res.state==1:
                self.ui.tasklist.addItem("task2 deactivate")
            elif self.res.state==2:
                self.ui.tasklist.addItem("task2 already active")
            else:
                self.ui.tasklist.addItem("task2 fail")
        except Exception as e:
            print(f"[ERROR] 服務回應錯誤: {e}")

    def task2(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task2")
        self.task2_event.set()


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
    def task3(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task3")
        print("cc")
        self.req.task="task3"
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        res=self.future.result()
        print(res.state)
        if res.state==1:
            self.ui.tasklist.addItem("task3 complete")
        else:
            self.ui.tasklist.addItem("task3 fail")
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



    def start_camera(self):
        while self.all_thread_flag:
            self.camera_event.wait()
            self.camera_event.clear()
            print("doing camera")
            # self.req.task="task2"
            # self.future = self.cli.call_async(self.req)
            # self.future.add_done_callback(self.task2_response_callback)
            camera_tmp = cv2.resize(self.camera_tmp, (300, 200))   # 改變尺寸和視窗相同
            camera_tmp = cv2.cvtColor(camera_tmp, cv2.COLOR_BGR2RGB)  # 轉換成 RGB
            height, width, channel = camera_tmp.shape    # 讀取尺寸和 channel數量
            bytesPerline = channel * width          # 設定 bytesPerline ( 轉換使用 )
            # 轉換影像為 QImage，讓 PyQt5 可以讀取
            img = QtGui.QImage(camera_tmp, width, height, bytesPerline, QtGui.QImage.Format_RGB888)
            self.ui.out2.setPixmap(QtGui.QPixmap.fromImage(img))

            print("done cmaera")
    def camera_callback(self,msg):
        self.camera_tmp=self.bridge.imgmsg_to_cv2(msg,'bgr8')
        self.camera_event.set()




    def exit(self):
        # self.task1_thread.kill()
        # self.task2_thread.kill()
        # self.camera_thread.kill()
        # self.ros_thread.kill()
        self.all_thread_flag=False
        # rclpy.shutdown()
        self.task1_event.set()
        self.task2_event.set()
        self.camera_event.set()
        self.task1_thread.join()
        self.task2_thread.join()
        self.camera_thread.join()
        rclpy.shutdown()
        self.ros_thread.join()
        sys.exit()
    # def _setup_ui(self):
    #     print("Setting up UI")
        
    #     print("aa")
    #     self.destroy_node()
    # def ui_thread(self):
    #     self.ui_loop=Thread(target=self._setup_ui)
    #     self.ui_loop.daemon=True
    #     self.ui_loop.start()


    

def main(args=None):
    



    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()


    
    # response = minimal_client.send_request(int(1), int(2))
    # minimal_client.get_logger().info(
    #     'Result of add_two_ints: for %d + %d = %d' %
    #     (int(sys.argv[1]), int(sys.argv[2]), response.sum))

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()