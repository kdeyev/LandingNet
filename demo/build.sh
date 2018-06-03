#!/bin/bash

g++ -g -std=gnu++0x demo.cpp -o demo -I/usr/local/include/breakpad/ -L/usr/local/lib -lbreakpad_client -lpthread

dump_syms ./demo > demo.sym
