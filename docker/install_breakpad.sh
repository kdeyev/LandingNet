#!/bin/bash

cd third-party
#svn co http://google-breakpad.googlecode.com/svn/trunk/ google-breakpad
git clone https://github.com/google/breakpad.git
git clone https://chromium.googlesource.com/linux-syscall-support breakpad/src/third_party/lss
mv breakpad google-breakpad
mkdir obj-breakpad/
cd obj-breakpad/ 
../google-breakpad/configure && make
cd ../


#hg clone http://hg.mozilla.org/users/tmielczarek_mozilla.com/minidump-stackwalk -b json
svn export https://github.com/mozilla-services/socorro.git/trunk/minidump-stackwalk
cd minidump-stackwalk
make
cp stackwalker ../../bin/
cd ../../

#wget -N --quiet 'https://index.taskcluster.net/v1/task/project.socorro.breakpad.v1.builds.linux64.latest/artifacts/public/breakpad.tar.gz'
#tar -zxf breakpad.tar.gz
#rm -rf stackwalk
#mv breakpad stackwalk