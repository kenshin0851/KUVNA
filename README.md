# KUVNA
This project aims to understand the principles of a Vector Network Analyzer (VNA) by building a user interface (UI) with the Python packages included in the uvna kit. ]

To use the python modules to communicate with the transceiver board, first you must run the following
script with your python installation: %ProgramFiles%/Vayyar/VNAKit/python/install_vnakit.py
API is compatible with python versions: 2.7, 3.5, 3.6, & 3.7
Once you've run that, it should install two python packages: “vnakit” (to use API commands) and
“vnakit_ex “(to run and use Demos provided). Check if both these packages were installed in your
python package list.
Now you can run the Demos which are located at “%ProgramFiles%/Vayyar/VNAKit/python/demos”.
To connect to the UVNA-63 transceiver board, append the following code to the beginning of your own
python script:
 import vnakit
 vnakit.Init() 
