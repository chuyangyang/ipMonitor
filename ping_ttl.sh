#!/bin/bash
ping $1 -c 3 | grep 'min/avg/max/mdev'|awk '{print $4}'|awk -F '/' '{print $2}'
