# **pyrealsense2**
## ***Built from source***

> sudo apt-get update && sudo apt-get upgrade

> sudo apt-get install python3 python3-dev

> cd librealsense

> mkdir build

> cd build

> cmake ../ -DBUILD_EXAMPLES=true -DBUILD_WITH_OPENMP=false -DHWM_OVER_XU=false -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=/usr/bin/python3 -DFORCE_RSUSB_BACKEND=true

> make -j4

> sudo make install

## ***After built from source***
1.  Open new terminal
2.  Enter:
    > export PYTHONPATH=$PYTHONPATH:/usr/local/lib
3.  cd to the python file
4.  Execute python file -> change "filename" to your file name
    > python3 filename.py