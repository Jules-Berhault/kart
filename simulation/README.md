# Simulation

A simulator is implemented in V-REP in order to check system behavior in simulation. This simulation is base interfaced with ROS via a LUA script which control the simulated car in the V-REP environment. It let us cerify our node without any changes because the low level nodes are replaced by the ROS-V-REP linker.

[![video](https://github.com/gwendalp/kart/blob/master/doc/rapport/Images/track.gif)](https://www.youtube.com/watch?time_continue=10&v=_vIXo1TvG0w&feature=emb_logo "video")

Voici le lien vers la vidéo 🏁 :camera_flash: ⏯ : 

https://www.youtube.com/watch?time_continue=44&v=_vIXo1TvG0w&feature=emb_logo


## Downloads

Download the folder :

```bash
git clone https://github.com/gwendalp/kart.git
```
Download the vrep:

https://coppeliarobotics.com/downloads


## Start Simulation

* Launch **ROS** : ```roscore```
* Run ```./vrep.sh```
* Open the scene : track.ttt
* Launch Nodes :
```bash
rosrun kart camera_node.py
rosrun kart camera_controller.py
```

## Enjoy and progress

You can tune the gains in controller.py in order to increase the speed of the car.
Now, it should run in about 1'15'' per track ! 🕙 🛤

## Authors

* **Jules Berhault** - 
* **Quentin Brateau** -  [Teusner](https://github.com/Teusner) :sunglasses:
* **Paul-Antoine Le Tolguennec** - 
* **Gwendal Priser** - [gwendalp](https://github.com/gwendalp) :ocean:
* **Mamadou Dembele** -

## Sources

Benoit Zerr work : https://www.ensta-bretagne.fr/zerr/dokuwiki/doku.php?id=vrep:create-rc-car-robot

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details