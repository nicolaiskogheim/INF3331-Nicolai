#!/usr/local/env bin

test $# -ne 2 && echo "${0##*/}: Expected two arguments path & size" && exit 1

path=$1
size=$2

files_to_delete=$(find $path -size +${size}k -print)

if [ -n "$files_to_delete" ]
then
  echo Deleting...
  echo "$files_to_delete"
  rm -- $files_to_delete
else
  echo No files of size $size kilobytes or larger found.
fi



exit 0

#######################
Alternate solution

if [ -n "$files_to_delete" ]
then
  echo Deleting...

  # List og slett slik..
  rm -v $files_to_delete | awk '{print $2}'

  # ..eller slik
  for file in ${files_to_delete[@]} ; do
    rm -- $file && echo $file
  done        # ^^------------- Går det åt skogen med rm, vil det
              #+                ikke stå at filen er slettet.
else
  echo No files of size $size kilobytes or larger found.
fi
