import os.path
import subprocess
import rospy
from std_msgs.msg import Float64

password_for_sudo = '07071999'

def get_root_privilleges():
    if started_as_root():
        init()
    else:
        current_script = os.path.realpath(__file__)
        os.system('echo %s|sudo -S python %s' % (password_for_sudo, current_script))

def started_as_root():
    if subprocess.check_output('whoami').strip() == 'root':
        return True
    return False        

def init():
    # Setting up the two pwm ports
    with open("/sys/class/pwm/pwmchip0/export", 'w') as f:
        f.write("0")  
    with open("/sys/class/pwm/pwmchip0/export", 'w') as f:
        f.write("1")
    
    # Setting up the period
    with open("/sys/class/pwm/pwmchip0/pwm0/period", 'w') as f:
        f.write("20000000")
    with open("/sys/class/pwm/pwmchip0/pwm1/period", 'w') as f:
        f.write("20000000")
    
    # Setting up the duty cycle
    with open("/sys/class/pwm/pwmchip0/pwm0/duty_cycle", 'w') as f:
        f.write("1500000")
    with open("/sys/class/pwm/pwmchip0/pwm1/duty_cycle", 'w') as f:
        f.write("1500000")
        
    # Enabling the pwm output
    with open("/sys/class/pwm/pwmchip0/pwm0/enable", 'w') as f:
        f.write("1")
    with open("/sys/class/pwm/pwmchip0/pwm1/enable", 'w') as f:
        f.write("1")

def u1_callback(data):
    u1 = 500000 * data.data + 1500000
    
def u2_callback(data):
    u2 = 500000 * data.data + 1500000

if __name__ == '__main__':
    # Checcking if we have the root privileges
    get_root_privilleges()
    
    # Cammand variables
    u1, u2 = 1500000, 1500000
    
    # ROS
    rospy.init_node('driver_node')
    rospy.Subscriber("u1", Float64, u1_callback)
    rospy.Subscriber("u2", Float64, u2_callback)
    
    r = rospy.Rate(20) # 20hz
    
    while not rospy.is_shutdown():
        # Setting up the duty cycle
        with open("/sys/class/pwm/pwmchip0/pwm0/duty_cycle", 'w') as f:
            f.write(u1)
        with open("/sys/class/pwm/pwmchip0/pwm1/duty_cycle", 'w') as f:
            f.write(u2)
            
        # Sleeping
        r.sleep()