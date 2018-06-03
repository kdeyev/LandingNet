#!/bin/bash

g++ -g -std=gnu++0x demo.cpp -o demo -I/usr/local/include/breakpad/ -L/usr/local/lib -lbreakpad_client -lpthread

../third-party/obj-breakpad/src/tools/linux/dump_syms/dump_syms ./demo > demo.sym
