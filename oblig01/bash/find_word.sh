#!/usr/local/env bash

find $1 -type f | xargs grep -n --color=always $2 \
|| echo No files containing \"$2\" found.
