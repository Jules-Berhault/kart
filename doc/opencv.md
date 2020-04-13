# OpenCv Installation Guide

In order to install opencv for python, use the following command.
To download the latest source from OpenCV's GitHub Repository.


```bash
$ git clone https://github.com/opencv/opencv.git
```

It will create a folder "opencv" in current directory. The cloning may take some time depending upon your internet connection.
Now open a terminal window and navigate to the downloaded "opencv" folder. Create a new "build" folder and navigate to it.

```bash
$ cd opencv
$ mkdir build
$ cd build
```

```bash
$ cmake ..
```

You should see these lines in your CMake output (they mean that Python is properly found):

```bash
--   Python 2:
--     Interpreter:                 /usr/bin/python2.7 (ver 2.7.6)
--     Libraries:                   /usr/lib/x86_64-linux-gnu/libpython2.7.so (ver 2.7.6)
--     numpy:                       /usr/lib/python2.7/dist-packages/numpy/core/include (ver 1.8.2)
--     packages path:               lib/python2.7/dist-packages
--
--   Python 3:
--     Interpreter:                 /usr/bin/python3.4 (ver 3.4.3)
--     Libraries:                   /usr/lib/x86_64-linux-gnu/libpython3.4m.so (ver 3.4.3)
--     numpy:                       /usr/lib/python3/dist-packages/numpy/core/include (ver 1.8.2)
--     packages path:               lib/python3.4/dist-packages
```

Now you build the files using "make" command and install it using "make install" command.

```bash
$ make
$ make install
```

Installation is over. All files are installed in "/usr/local/" folder. Open a terminal and try import "cv2".

```python
import cv2 as cv
print(cv.__version__)
```