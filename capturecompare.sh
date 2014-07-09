#!/bin/bash

cp -R ~/VisualDiff/capture/Screens/www.integration.native-instruments.de/ ~/VisualDiff/capture/Screens-B
rm ~/VisualDiff/capture/Screens/*
vd-capture -O ~/VisualDiff/capture/Screens -S http://www.integration.native-instruments.de/en/sitemap/ -L 5
vd-compare ~/VisualDiff/capture/Screens/www.integration.native-instruments.de ~/VisualDiff/capture/Screens-B --output-path=~/VisualDiff/compare/mismatches
