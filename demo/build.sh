#!/bin/bash

g++ -g -std=gnu++0x demo.cpp -o demo -I../third-party/google-breakpad/src/ -L../third-party/obj-breakpad/src/client/linux/ -lbreakpad_client -lpthread

../third-party/obj-breakpad/src/tools/linux/dump_syms/dump_syms ./demo > demo.sym
