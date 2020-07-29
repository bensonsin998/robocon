# **pyrealsense2**
## ***Build from source***
### ****Python 2.x****

* > sudo apt-get update && sudo apt-get upgrade

* > sudo apt-get install python python-dev

* > git clone https://github.com/JetsonHacksNano/installSwapfile.git

* > cd installSwapfile

* > ./installSwapfile.sh

* > cd../

* > git clone https://github.com/JetsonHacksNano/installlibrealsense.git

* > cd installLibrealsense

* > ./installLibrealsense.sh

* > ./buildLibrealsense.sh

* > cd ../

* > cd librealsense

* > If there is not "build" folder,
    >> mkdir build
  > cd build

* > export PATH=/usr/local/cuda/bin:$PATH

* > cmake ../ -DBUILD_EXAMPLES=true -DBUILD_WITH_OPENMP=false -DHWM_OVER_XU=false -DFORCE_RSUSB_BACKEND=true -DBUILD_WITH_CUDA=true -DBUILD_PYTHON_BINDINGS=bool:true -DPYTHON_EXECUTABLE=/usr/bin/python

* > make -jx

  > x = the core that Jetson support
    <br> Recommand: x >= 4
    <br> To check the core number, use command
    >> nproc

* > sudo make install

* > cd ../

* > sudo nano .bashrc

* Add the following command to the end of .bashrc
  > export PYTHONPATH=$PYTHONPATH:/usr/local/lib


## ***After built from source***
1.  Open new terminal
2.  Enter:
    > export PYTHONPATH=$PYTHONPATH:/usr/local/lib
3.  cd to the python file
4.  Execute python file -> change "filename" to your file name
    > python3 filename.py
