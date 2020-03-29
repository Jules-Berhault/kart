# Kart

## Introduction
This repository is a school project leaded at Ensta Bretagne about the building of a car and his automating. The car is a one-tenth scale replica and was built with 3d printing, turning and milling. Here is a picture of the final result of his building.

*Insert the picture here*

## Building
This car was designed using Autodesk Inventor and the files are available in the cao folder.

*Insert the picture of the cao here*

## Automating
After the building of this car, we need to robotize it. In order to do that, we decided to use a Raspberry Pi 4 and some sensors.

| Sensors       | Used             | Dope-Level               |
| ------------- |:----------------:|:------------------------:|
| GNSS          |:x:               |:turtle::boom::dash::poop:|
| Inertial Unit |:x:               |:rainbow:                 |
| Pi camera     |:heavy_check_mark:|:unicorn:                 |

We decided to use **ROS** (**R**obot **O**perating **S**ystem), the well-known Middleware for mobile robotics. We created our own nodes to control this robot.

*Insert the node graph here*

## Simulation
A simulator is implemented in V-REP in order to check system behavior in simulation. This simulation is base interfaced with ROS via a LUA script which control the simulated car in the V-REP environment. It let us cerify our node without any changes because the low level nodes are replaced by the ROS-V-REP linker.

*Insert the picture of the Simulation*

## Authors

* **Jules Bherault** - 
* **Quentin Brateau** -  [Teusner](https://github.com/Teusner) :sunglasses:
* **Paul-Antoine Le Tolguenec** - 
* **Gwendal Priser** - [gwendalp](https://github.com/gwendalp)


## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details