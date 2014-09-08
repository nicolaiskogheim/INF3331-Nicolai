#!/usr/local/env bash

E_BADARGS=85


usage(){
  echo -e "Usage: bash ./`basename $0` folder days"
  }

if [ $# -ne 2 ]
then
  usage
  exit $E_BADARGS
fi

folder=$1
days=$2

find $folder -type f -mtime -${days}d | du -h | sort -h | egrep -v "\.(\/$1)?$"
