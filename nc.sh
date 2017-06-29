#!/bin/bash
#$1:ipaddr $2:port
nc -z -w 1 $1 $2 $3
