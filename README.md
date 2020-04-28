# Kart

## Introduction
This repository is a school project leaded at Ensta Bretagne about the building of a car and his automating. The car is a one-tenth scale replica and was built with 3d printing, turning and milling. Here is a picture of the final result of his building.

<p align="center">
    <img src="https://github.com/gwendalp/kart/blob/master/doc/report/Images/Kart_overview_1.jpg"> <br>
    <em>Real Kart 🚙</em>
</p>

## Building
This car was designed using Autodesk Inventor and the files are available in the CAD folder.

<p align="center">
    <img src="https://github.com/gwendalp/kart/blob/master/doc/report/Images/plan_global.png"> <br>
    <em>CAD of the kart 🗺 </em>
</p>


## Automating
After the building of this car, we need to robotize it. In order to do that, we decided to use a Raspberry Pi 3B+ and some sensors.

| Sensors       | Used             | Dope-Level               |
| ------------- |:----------------:|:------------------------:|
| GNSS          |:x:               |:turtle::boom::dash::poop:|
| Inertial Unit |:x:               |:rainbow:                 |
| Pi camera     |:heavy_check_mark:|:unicorn:                 |

We decided to use **ROS** (**R**obot **O**perating **S**ystem), the well-known Middleware for mobile robotics. We created our own nodes to control this robot.

*Insert the node graph here*

## :barber: Tracker :barber:
Here is a tracker for each task we have to do.

| Task            |Responsible | Progression      | Note |
| ----------------|:----------:|:----------------:|:----:|
| PWM driver      |Quentin     |:heavy_check_mark:|      |
| Image Processing|Paul-Antoine|:heavy_check_mark:|      |
| Launch on Boot  |Quentin     |:heavy_check_mark:|      |
| PWM driver      |Quentin     |:heavy_check_mark:|      |
| CAO             |Jules       |:heavy_check_mark:|      |
| Electronic board|Quentin     |:x:               |Lack of electronic items|
| V-REP Simulator |Gwendal     |:heavy_check_mark:         |      |
| Report          |All         |:recycle:         |      |


## Simulation
A simulator is implemented in V-REP in order to check system behavior in simulation. This simulation is base interfaced with ROS via a LUA script which control the simulated car in the V-REP environment. It let us cerify our node without any changes because the low level nodes are replaced by the ROS-V-REP linker.

[![video](https://github.com/gwendalp/kart/blob/master/doc/report/Images/track.gif)](https://www.youtube.com/watch?time_continue=10&v=_vIXo1TvG0w&feature=emb_logo "video")

Here is the link toward the YouTube video 🏁 :camera_flash: ⏯ : 

https://www.youtube.com/watch?time_continue=44&v=_vIXo1TvG0w&feature=emb_logo



## Authors

* **Jules Berhault** - 
* **Quentin Brateau** -  [Teusner](https://github.com/Teusner) :sunglasses:
* **Paul-Antoine Le Tolguennec** - 
* **Gwendal Priser** - [gwendalp](https://github.com/gwendalp) :ocean:
* **Mamadou Dembele** -

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details
