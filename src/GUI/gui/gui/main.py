
import sys

from gui_interface.srv import Taskcmd
import rclpy
from rclpy.node import Node

from threading import Thread
from gui.main_ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets



class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(Taskcmd, 'taskcmd')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Taskcmd.Request()
        self.tasklist=[]

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
        self.ui.exit.clicked.connect(self.exit)
        MainWindow.show()
        sys.exit(app.exec_())
        

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    def task1(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task1")
        print("aa")
    
    def task2(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task2")
        print("bb")
    def task3(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task3")
        print("cc")
    def task4(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task4")
        print("dd")
    def task5(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task5")
        print("ee")
    def task6(self):
        self.ui.tasklist.clear()
        self.ui.tasklist.addItem("task6")
        print("ff")
    def exit(self):
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