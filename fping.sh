#!/bin/bash
fping $1 2> /dev/null | awk '{print $3}'
