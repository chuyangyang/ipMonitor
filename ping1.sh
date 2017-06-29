#!/bin/sh
ping -c 10  $1 |grep 'loss'|awk -F ' ' '{print $6}'
