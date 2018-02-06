#!/bin/bash

yum -y install python python-pip; 
yum -y install gcc gcc-c++ make postgresql-devel python-devel;
#yum clean all
pip install -r requirements.txt
