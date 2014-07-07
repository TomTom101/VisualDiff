#!/bin/bash

cp -R ~/VisualDiff/capture/Screens/ ~/VisualDiff/capture/Screens-B
rm ~/VisualDiff/capture/Screens/*
./capture.py -O ~/VisualDiff/capture/Screens -S http://www.integration.native-instruments.de/en/sitemap/ -L 3
./compare.py ~/VisualDiff/capture/Screens ~/VisualDiff/capture/Screens-B --output-path=~/VisualDiff/compare/mismatches
