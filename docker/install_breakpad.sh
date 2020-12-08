#!/bin/bash

# yum -y install git svn hg;
# yum -y install gcc gcc-c++ make;

cd third-party
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
export PATH=$PATH:/breakpad/third-party/depot_tools/
fetch breakpad
# git clone https://github.com/google/breakpad.git
# cd breakpad
cd src
cp -rf /breakpad/third-party/core_handler.cc /breakpad/third-party/src/src/tools/linux/core_handler/core_handler.cc
./configure && make && make install
cd ../
cd minidump-stackwalk
make
mkdir ../../bin/
cp stackwalker ../../bin/
cd ../../


