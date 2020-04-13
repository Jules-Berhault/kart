import pyproj
from geometry_msgs.msg import PointStamped, PoseStamped, TwistStamped,Twist,Quaternion
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
from tf.transformations import quaternion_from_euler
import rospy
from numpy.linalg import inv
from numpy import *
from matplotlib.pyplot import scatter, show
freq=25

lat=0
lon=0

# Define a projection with Proj4 notation, in this case an France grid 
isn2004=pyproj.CRS("+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs") 
  
# Define some common projections using EPSG codes 
wgs84=pyproj.CRS("EPSG:4326") # LatLon with WGS84 datum used by GPS units and Google Earth

def gpsCallback(msg):
    lat=msg.latitude
    lon=msg.longitude

rospy.init_node('observer_node', anonymous=True)

""" creation subscriber """
gps_xy = rospy.Publisher('projection node',PointStamped, queue_size=10)
vel_suscriber = rospy.Subscriber('Fix', NavSatFix, gpsCallback)

mess=PointStamped()
rate = rospy.Rate(freq) # 25hz

while not rospy.is_shutdown():
	x,y=pyproj.transform(wgs84, isn2004, lat, lon)
	mess.point.x=x
	mess.point.y=y
	mess.point.z=0
	gps_xy.publish(mess)
