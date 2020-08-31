#!/bin/bash

# If you use windows pc. You must use cygwin bash and exec option `-w`.

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

# build
rm $ORIGIN/dist.zip

cp -rf ./src ./tmp
docker run --rm -v "$ORIGIN/tmp":/var/task lambci/lambda:build-python3.6 pip install -r requirements.txt -t .
docker run --rm -v "$ORIGIN":/var/task lambci/lambda:build-python3.6 zip -r dist ./tmp/

rm -rf $ORIGIN/tmp

echo "build finished."