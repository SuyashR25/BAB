import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import sys

# =========================================================
# ⚙️ SETTINGS: UPDATE THIS IP ADDRESS
# Run 'cat /etc/resolv.conf' in WSL to find this IP
# =========================================================
WINDOWS_IP = '10.200.242.10'  # <--- REPLACE WITH YOUR IP
# =========================================================

class ScribeBotBridge(Node):
    def __init__(self):
        super().__init__('scribe_bot_bridge')
        self.get_logger().info('--- SCRIBE BOT BRIDGE STARTING ---')

        # 1. CONNECT TO COPPELIASIM
        try:
            self.get_logger().info(f'Connecting to Windows at {WINDOWS_IP}...')
            self.client = RemoteAPIClient(host=WINDOWS_IP, port=23000)
            self.sim = self.client.getObject('sim')
            self.get_logger().info('✅ ZMQ Connection Established.')
        except Exception as e:
            self.get_logger().error(f'❌ Connection Failed: {e}')
            self.get_logger().error('Did you check the IP? Is CoppeliaSim running?')
            sys.exit(1)

        # 2. TEST CONNECTION & GET SCRIPT HANDLE
        try:
            script_handle = self.sim.getObject('/Base') 
            script_id = self.sim.getScript(self.sim.scripttype_childscript, script_handle)
            response = self.sim.callScriptFunction('ping_from_ros', script_id)
            self.get_logger().info(f'✅ CoppeliaSim Responded: "{response}"')
        except Exception as e:
            self.get_logger().warn(f'⚠️ Could not ping script: {e}')

        # 3. GET JOINT HANDLES
        try:
            self.joint_x = self.sim.getObject("/Base/X_joint")
            self.joint_y = self.sim.getObject("/Base/X_joint/X_link/Y_joint")
            self.get_logger().info('✅ Joint Handles Found.')
        except Exception as e:
            self.get_logger().error(f'❌ Could not find joints: {e}')
            sys.exit(1)

        # 4. VARIABLES
        self.target_x = 0.0
        self.target_y = 0.0
        self.step = 0.005
        self.limit = 0.2

        # 5. SUBSCRIBE TO KEYBOARD
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        self.get_logger().info('Ready. 8/2 moves Y-Axis. 4/6 moves X-Axis.')

    def cmd_callback(self, msg):
        # ==================================================
        # 🎮 REMAPPING LOGIC (Numpad Style)
        # ==================================================

        # --- 8 and 2 (Up/Down) -> MOVE Y AXIS ---
        # 'i' sends +Linear X (Up/8) -> We map to Y+
        if msg.linear.x > 0: 
            self.target_y += self.step
        
        # ',' sends -Linear X (Down/2) -> We map to Y-
        if msg.linear.x < 0: 
            self.target_y -= self.step

        # --- 4 and 6 (Left/Right) -> MOVE X AXIS ---
        # 'l' sends -Angular Z (Right/6) -> We map to X+
        if msg.angular.z < 0: 
            self.target_x += self.step
            
        # 'j' sends +Angular Z (Left/4) -> We map to X-
        if msg.angular.z > 0: 
            self.target_x -= self.step

        # Apply Limits
        self.target_x = max(-self.limit, min(self.limit, self.target_x))
        self.target_y = max(-self.limit, min(self.limit, self.target_y))

        # Send to CoppeliaSim
        self.sim.setJointTargetPosition(self.joint_x, self.target_x)
        self.sim.setJointTargetPosition(self.joint_y, self.target_y)
        
        # Log occasionally
        # self.get_logger().info(f'X: {self.target_x:.3f}, Y: {self.target_y:.3f}')

def main():
    rclpy.init()
    node = ScribeBotBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
