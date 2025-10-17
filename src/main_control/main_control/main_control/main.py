from interface.srv import Maincontroller
from interface.msg import ShelfState
from gui_interface.srv import Taskcmd
import rclpy
from rclpy.node import Node

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import time

from std_msgs.msg import Float32MultiArray , Int32

from threading import Event


class controller(Node):

    def __init__(self):
        super().__init__('MainControl')
        client_group1=ReentrantCallbackGroup()
        server_group=client_group1
        


        self.srv = self.create_service(Taskcmd, 'taskcmd', self.aa, callback_group=server_group)

        self.pallet = self.create_client(Maincontroller, 'Pallet',callback_group=client_group1)
        # while not self.cli_pallet.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('pallet service not available, waiting again...')
        
        self.shelf_pose = self.create_client(Maincontroller, 'toggle_aruco_detection',callback_group=client_group1)
        # while not self.cli_shelf_pose.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('shelf_pose service not available, waiting again...')

        self.docking = self.create_client(Maincontroller, 'docking_status_server',callback_group=client_group1)  #docking
        # while not self.cli_docking.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('docking service not available, waiting again...')
        
        self.shelf_docking = self.create_client(Maincontroller, 'shelf_docking',callback_group=client_group1)
        # while not self.cli_4.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        
        self.aruco_parking = self.create_client(Maincontroller, 'parking', callback_group=client_group1)

        # self.cli_5 = self.create_client(Maincontroller, 'add_two_ints',callback_group=client_group1)
        # while not self.cli_5.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        self.slam_pub = self.create_publisher(Float32MultiArray, '/timda_nav_pose', 10)
        self.slam_status_sub=self.create_subscription(
            Int32, 
            '/timda_nav_success',
            self.slam_callback,
            10)



        self.check_client_list=[
            # self.pallet,
            # self.shelf_pose,
            # self.docking,
            # self.shelf_docking
            # self.aruco_parking
        ]

        for i in self.check_client_list:
            while not i.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(i.srv_name +' server not available, waiting again...')


        self.slam_event=Event()
        self.process_event=Event()
        # self.slam_flag=False
        self.home_flag=True
        self.slam_count=0
        self.pallet_mode='mix'
        self.req = Maincontroller.Request()
        self.slam_req = Float32MultiArray()
        self.res = Taskcmd.Response()
        # self.auto_test()

    def auto_test(self):
        tasklist=["slam1","parking","slam2","slam3","docking","shelf_docking","slam4"]
        while len(tasklist)>=1:
            current_task=tasklist.pop(0)
            if current_task=="slam1":
                self.get_logger().info(f"Calling slam{self.slam_count}...")
                if self.slam_count==0:
                    #parking
                    # self.slam_req.data = [0.8,-0.95,270.0]
                    # self.slam_pub.publish(self.slam_req)
                    self.slam_count+=1
                elif self.slam_count==1:
                    #goto docking
                    self.slam_req.data = [1.6,-1.26,0.0]
                    self.slam_pub.publish(self.slam_req)
                    self.slam_count+=1
                elif self.slam_count==2:
                    #pre docking
                    self.slam_req.data = [2.31,-2.05,180.0]
                    self.slam_pub.publish(self.slam_req)
                    self.slam_count+=1
                elif self.slam_count==3:
                    #home
                    # self.slam_req.data = [2.31,-2.05,180]
                    # self.slam_pub.publish(self.slam_req)
                    pass
                    self.slam_count=0
                    self.slam_event.set()

                
                self.slam_event.wait()
                self.slam_event.clear()
                self.slam_status_sub = self.create_subscription(
                    Int32,
                    '/timda_nav_success',
                    self.slam_callback,
                    10
                )
                res=self.slam_status
                self.get_logger().info(f"done slam{self.slam_count}, res = {res}")


            
            

            elif current_task=="parking":
                self.get_logger().info("Calling parking...")
                inner_req = Maincontroller.Request()
                inner_req.enable = True
                future=self.aruco_parking.call_async(inner_req)
                # while not future.done():
                #     time.sleep(0.01)
                input(f"{current_task} need input")
                try:
                    # inner_res = future.result()
                    # print("parking_inner_res.done=",inner_res.done)
                    # res=inner_res.done
                    res=1
                except Exception as e:
                    self.get_logger().error(f"parking Inner service failed: {e}")
                    res = -1


            elif current_task=="palleting":
                self.get_logger().info("Calling palleting...")
                inner_req = Maincontroller.Request()
                inner_req.enable = True
                future = self.pallet.call_async(inner_req)
                # while not future.done():
                #     time.sleep(0.01)
                input(f"{current_task} need input")
                try:
                    # inner_res = future.result()
                    # print("palleting_inner_res.done=",inner_res.done)
                    # res=inner_res.done
                    res=1
                except Exception as e:
                    self.get_logger().error(f"palleting Inner service failed: {e}")
                    res = -1
                
            elif current_task=="start_positioning":
                self.get_logger().info("starting positioning...")
                inner_req = Maincontroller.Request()
                inner_req.enable = True
                future = self.shelf_pose.call_async(inner_req)
                while not future.done():
                    time.sleep(0.01)
                try:
                    inner_res = future.result()
                    print("start_positioning.done=",inner_res.done)
                    res=inner_res.done
                except Exception as e:
                    self.get_logger().error(f"start_positioning Inner service failed: {e}")
                    res = -1


            elif current_task=="close_positioning":
                self.get_logger().info("closing positioning...")
                inner_req = Maincontroller.Request()
                inner_req.enable = False
                future = self.shelf_pose.call_async(inner_req)
                while not future.done():
                    time.sleep(0.01)
                try:
                    inner_res = future.result()
                    print("close_positioning.done=",inner_res.done)
                    res=inner_res.done
                except Exception as e:
                    self.get_logger().error(f"close_positioning Inner service failed: {e}")
                    res = -1


            elif current_task=="docking":
                self.get_logger().info("starting docking...")
                inner_req = Maincontroller.Request()
                inner_req.enable = True
                future = self.docking.call_async(inner_req)
                while not future.done():
                    time.sleep(0.01)
                try:
                    inner_res = future.result()
                    print("docking_inner_res.done=",inner_res.done)
                    res=inner_res.done
                except Exception as e:
                    self.get_logger().error(f"docking Inner service failed: {e}")
                    res = -1

            elif current_task=="shelf_docking":
                self.get_logger().info("starting shelf_docking...")
                inner_req = Maincontroller.Request()
                inner_req.enable = True
                future = self.shelf_docking.call_async(inner_req)
                while not future.done():
                    time.sleep(0.01)
                try:
                    inner_res = future.result()
                    print("shelf_docking_inner_res.done=",inner_res.done)
                    res=inner_res.done
                except Exception as e:
                    self.get_logger().error(f"shelf_docking Inner service failed: {e}")
                    res = -1

            elif current_task=="task5":
                print("a")
                # self.req.enable=True
                # self.future = self.cli_5.call_async(self.req)
                # rclpy.spin_until_future_complete(self, self.future)
                # res=self.future.result()
                # print(res.done)
                res=5
            elif current_task=="task6":
                print("a")
                # self.req.enable=True
                # self.future = self.cli_6.call_async(self.req)
                # rclpy.spin_until_future_complete(self, self.future)
                # res=self.future.result()
                # print(res.done)
                res=6
            return res
        
    def slam_callback(self,msg):
        self.destroy_subscription(self.slam_status_sub)
        self.slam_status=msg.data
        if msg.data==1:
            self.slam_event.set()
            self.get_logger().info('slam success')
        else:
            self.get_logger().error('slam fail')
            pass

    def aa(self,req,res):
        if req.task=="slam_parking":
            self.get_logger().info(f"Calling slam_parking...")
            #parking
            self.slam_req.data = [0.8,-0.95,270.0]
            self.slam_pub.publish(self.slam_req)
            self.slam_event.wait()
            self.slam_event.clear()
            self.slam_status_sub = self.create_subscription(
                Int32,
                '/timda_nav_success',
                self.slam_callback,
                10
            )
            self.res.state=self.slam_status
            self.get_logger().info(f"done slam{self.slam_count}, res = {self.res}")

        elif req.task=="slam_goto_docking":
            self.get_logger().info(f"Calling slam_goto_docking...")
            #goto docking
            self.slam_req.data = [1.6,-1.26,0.0]
            self.slam_pub.publish(self.slam_req)
            self.slam_event.wait()
            self.slam_event.clear()
            self.slam_status_sub = self.create_subscription(
                Int32,
                '/timda_nav_success',
                self.slam_callback,
                10
            )
            self.res.state=self.slam_status
            self.get_logger().info(f"done slam{self.slam_count}, res = {self.res}")


        elif req.task=="slam_pre_docking":
            self.get_logger().info(f"Calling slam_pre_docking...")
            #pre docking
            self.slam_req.data = [2.31,-2.05,180.0]
            self.slam_pub.publish(self.slam_req)
            self.slam_event.wait()
            self.slam_event.clear()
            self.slam_status_sub = self.create_subscription(
                Int32,
                '/timda_nav_success',
                self.slam_callback,
                10
            )
            self.res.state=self.slam_status
            self.get_logger().info(f"done slam{self.slam_count}, res = {self.res}")


        elif req.task=="slam_home":
            self.get_logger().info(f"Calling slam_home...")
            #home
            self.slam_req.data = [0.7,-0.3,0.0]
            self.slam_pub.publish(self.slam_req)
            self.slam_event.wait()
            self.slam_event.clear()
            self.slam_status_sub = self.create_subscription(
                Int32,
                '/timda_nav_success',
                self.slam_callback,
                10
            )
            self.res.state=self.slam_status
            self.get_logger().info(f"done slam{self.slam_count}, res = {self.res}")



        elif req.task=="parking":
            self.get_logger().info("Calling parking...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            self.future=self.aruco_parking.call_async(inner_req)
            # while not future.done():
            #     time.sleep(0.01)
            self.future.add_done_callback(self.client_callback)
            self.process_event.wait()
            self.process_event.clear()
            # input(f"{req.task} need input")
            # try:
            #     # inner_res = future.result()
            #     # print("parking_inner_res.done=",inner_res.done)
            #     # res.state=inner_res.done
            #     self.res.state=1
            # except Exception as e:
            #     self.get_logger().error(f"parking Inner service failed: {e}")
            #     self.res.state = -1


        elif req.task=="palleting":
            self.get_logger().info("Calling palleting...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            self.future = self.pallet.call_async(inner_req)
            # while not future.done():
            #     time.sleep(0.01)
            # input(f"{req.task} need input")
            self.future.add_done_callback(self.client_callback)
            self.process_event.wait()
            self.process_event.clear()
            # try:
            #     # inner_res = future.result()
            #     # print("palleting_inner_res.done=",inner_res.done)
            #     # res.state=inner_res.done
            #     self.res.state=1
            # except Exception as e:
            #     self.get_logger().error(f"palleting Inner service failed: {e}")
            #     self.res.state = -1
            
        elif req.task=="start_positioning":
            self.get_logger().info("starting positioning...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            self.future = self.shelf_pose.call_async(inner_req)
            # while not future.done():
            #     time.sleep(0.01)
            # input(f"{req.task} need input")
            self.future.add_done_callback(self.client_callback)
            self.process_event.wait()
            self.process_event.clear()
            # try:
            #     # inner_res = future.result()
            #     # print("start_positioning.done=",inner_res.done)
            #     # res.state=inner_res.done
            #     self.res.state=1
            # except Exception as e:
            #     self.get_logger().error(f"start_positioning Inner service failed: {e}")
            #     self.res.state = -1


        elif req.task=="close_positioning":
            self.get_logger().info("closing positioning...")
            inner_req = Maincontroller.Request()
            inner_req.enable = False
            self.future = self.shelf_pose.call_async(inner_req)
            # while not future.done():
            #     time.sleep(0.01)
            # input(f"{req.task} need input")
            self.future.add_done_callback(self.client_callback)
            self.process_event.wait()
            self.process_event.clear()
            # try:
            #     # inner_res = future.result()
            #     # print("close_positioning.done=",inner_res.done)
            #     # res.state=inner_res.done
            #     self.res.state=1
            # except Exception as e:
            #     self.get_logger().error(f"close_positioning Inner service failed: {e}")
            #     self.res.state = -1


        elif req.task=="docking":
            self.get_logger().info("starting docking...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            self.future = self.docking.call_async(inner_req)
            # while not future.done():
            #     time.sleep(0.01)
            # input(f"{req.task} need input")
            self.future.add_done_callback(self.client_callback)
            self.process_event.wait()
            self.process_event.clear()
            # try:
            #     # inner_res = future.result()
            #     # print("docking_inner_res.done=",inner_res.done)
            #     # res.state=inner_res.done
            #     self.res.state=1
            # except Exception as e:
            #     self.get_logger().error(f"docking Inner service failed: {e}")
            #     self.res.state = -1

        elif req.task=="shelf_docking":
            self.get_logger().info("starting shelf_docking...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            self.future = self.shelf_docking.call_async(inner_req)
            # while not future.done():
            #     time.sleep(0.01)
            # input(f"{req.task} need input")
            self.future.add_done_callback(self.client_callback)
            self.process_event.wait()
            self.process_event.clear()
            # try:
            #     # inner_res = future.result()
            #     # print("shelf_docking_inner_res.done=",inner_res.done)
            #     # res.state=inner_res.done
            #     self.res.state=1
            # except Exception as e:
            #     self.get_logger().error(f"shelf_docking Inner service failed: {e}")
            #     self.res.state = -1

        # elif req.task=="task5":
        #     print("a")
        #     # self.req.enable=True
        #     # self.future = self.cli_5.call_async(self.req)
        #     # rclpy.spin_until_future_complete(self, self.future)
        #     # res=self.future.result()
        #     # print(res.done)
        #     self.res.state=5
        # elif req.task=="task6":
        #     print("a")
        #     # self.req.enable=True
        #     # self.future = self.cli_6.call_async(self.req)
        #     # rclpy.spin_until_future_complete(self, self.future)
        #     # res=self.future.result()
        #     # print(res.done)
        #     self.res.state=6
        return self.res


    def client_callback(self, future):
        try:
            res = future.result()
            self.process_event.set()
            self.get_logger().info(f"move completed: {res.done}")
        except Exception as e:
            self.get_logger().error(f'move service call failed: {e}')






def main(args=None):
    rclpy.init(args=args)

    minimal_client = controller()
    executor=MultiThreadedExecutor()
    executor.add_node(minimal_client)
    minimal_client.get_logger().info('beginning')
    executor.spin()

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()