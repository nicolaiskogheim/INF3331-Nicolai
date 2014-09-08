#!/usr/local/env bash

find file_tree -type f | xargs grep -n --color=always $1 \
|| echo No files containing \"$1\" found.
