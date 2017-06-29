#!/bin/sh
ping -c 1 -w 3 $1 |grep 'loss'|awk -F ' ' '{print $6}'
