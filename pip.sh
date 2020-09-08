#!/bin/bash

# If you use windows pc. You must use cygwin bash and exec option `-w`, install zip comand.

# Set ORIGIN
while getopts w OPT
do
  case $OPT in
     w) HAS_OPT_W="TRUE";;
     *) echo "invalid option" && exit 0;;
  esac
done
if [ "$HAS_OPT_W" = "TRUE" ]; then
  ORIGIN=`cygpath -wp $PWD`
else
  ORIGIN=`pwd`
fi

# delete
rm -rf "$ORIGIN/src/lib"

# install
docker run --rm -v "$ORIGIN/src":/var/task "lambci/lambda:build-python3.6" pip install -r requirements.txt -t ./lib

echo "pip install finished."
