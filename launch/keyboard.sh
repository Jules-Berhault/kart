roslaunch kart keyboard.launch &
sleep 2
rosrun kart teleop_twist_keyboard.py _speed:=1.0 _turn:=0.23
