#!/bin/bash

./CloudflareST -n 100 -dn 10 -url 'https://speed.cloudflare.com/__down?bytes=50000000' -tl 200 -tll 10 -tlr 0.1 -sl 5 -p 0

python run.py

rm -f result.csv