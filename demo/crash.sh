#!/bin/bash

curl -F minidump=@$1 -F product=Demo -F version=0.1 -F build=foobar -F user=dummy http://localhost:5000/submit