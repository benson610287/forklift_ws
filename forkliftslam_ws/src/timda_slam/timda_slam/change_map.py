import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from std_msgs.msg import Int32
from nav2_msgs.srv import LoadMap
from ament_index_python.packages import get_package_share_directory
import os

class MapSwitcherNode(Node):
    def __init__(self):
        super().__init__('map_switcher_node')
        
        # 使用 ReentrantCallbackGroup 允許 callback 中呼叫服務而不死鎖
        self.callback_group = ReentrantCallbackGroup()
        
        # 預存地圖清單 - 根據數字對應的地圖檔案路徑
        self.predefined_maps = {
            1: os.path.join(get_package_share_directory('timda_slam'), 'maps', 'map.yaml'),
            2: os.path.join(get_package_share_directory('timda_slam'), 'maps', 'map2.yaml'),
            3: os.path.join(get_package_share_directory('timda_slam'), 'maps', 'map3.yaml'),
            # 可以根據需要添加更多地圖
        }
        
        # 創建 subscriber，監聽 /change_map topic (改為接收整數)
        self.subscription = self.create_subscription(
            Int32,
            '/change_map',
            self.change_map_callback,
            10,
            callback_group=self.callback_group
        )
        
        # 創建 service client 來呼叫 /map_server/load_map
        self.client = self.create_client(LoadMap, '/map_server/load_map')
         
        # 設定一個計時器來檢查服務是否可用
        self.service_ready = False
        self.check_service_timer = self.create_timer(1.0, self.check_service_available)
        
        self.get_logger().info('MapSwitcherNode initialized. Checking for map service...')
        self.print_available_maps()

    def print_available_maps(self):
        """顯示可用的預存地圖"""
        self.get_logger().info('Available predefined maps:')
        for map_num, map_path in self.predefined_maps.items():
            exists = "✓" if os.path.exists(map_path) else "✗"
            self.get_logger().info(f'  Map {map_num}: {map_path} {exists}')

    def check_service_available(self):
        """定期檢查地圖服務是否可用"""
        if not self.service_ready:
            if self.client.wait_for_service(timeout_sec=0.1):
                self.service_ready = True
                self.check_service_timer.destroy()
                self.get_logger().info('Map service is available. Node ready to switch maps.')
            else:
                self.get_logger().info('Waiting for /map_server/load_map service...')

    def change_map_callback(self, msg):
        map_number = msg.data
        self.get_logger().info(f'Received request to switch to map number: {map_number}')
        
        # 檢查服務是否可用
        if not self.service_ready:
            self.get_logger().warn('Map service not available yet. Request ignored.')
            return
        
        # 檢查地圖編號是否存在
        if map_number not in self.predefined_maps:
            self.get_logger().error(f'Map number {map_number} not found in predefined maps. Available maps: {list(self.predefined_maps.keys())}')
            return
        
        map_path = self.predefined_maps[map_number]
        
        # 檢查地圖檔案是否存在
        if not os.path.exists(map_path):
            self.get_logger().error(f'Map file does not exist: {map_path}')
            return
        
        self.get_logger().info(f'Switching to map: {map_path}')
        
        # 準備請求
        request = LoadMap.Request()
        request.map_url = map_path  # 使用預存的地圖路徑
        
        # 非同步呼叫服務並設定 callback
        future = self.client.call_async(request)
        future.add_done_callback(lambda fut: self.service_response_callback(fut, map_number))

    def service_response_callback(self, future, map_number):
        """處理地圖載入服務的回應"""
        try:
            response = future.result()
            if response.result == 0:  # SUCCESS (基於 nav2_msgs 的回應代碼)
                self.get_logger().info(f'Successfully switched to map {map_number}!')
            else:
                self.get_logger().error(f'Failed to switch to map {map_number}, error code: {response.result}')
        except Exception as e:
            self.get_logger().error(f'Service call failed for map {map_number}: {e}')

def main(args=None):
    rclpy.init(args=args)
    
    node = MapSwitcherNode()
    
    # 使用 MultiThreadedExecutor 避免死鎖
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()