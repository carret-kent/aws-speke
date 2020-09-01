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

docker run --rm -v "$ORIGIN/src":/var/task \
--env-file ./src/.env \
"lambci/lambda:python3.6" \
lambda_function.lambda_handler \
'{"body": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><cpix:CPIX xmlns:cpix=\"urn:dashif:org:cpix\" xmlns:pskc=\"urn:ietf:params:xml:ns:keyprov:pskc\" xmlns:speke=\"urn:aws:amazon:com:speke\" id=\"sample\"><cpix:ContentKeyList><cpix:ContentKey kid=\"00112233-4455-6677-8899-aabbccddeeff\"></cpix:ContentKey></cpix:ContentKeyList><cpix:DRMSystemList><cpix:DRMSystem kid=\"00112233-4455-6677-8899-aabbccddeeff\" systemId=\"81376844-f976-481e-a84e-cc25d39b0b33\"><cpix:PSSH /><cpix:ContentProtectionData /><cpix:URIExtXKey /><speke:KeyFormat /><speke:KeyFormatVersions /><speke:ProtectionHeader /></cpix:DRMSystem></cpix:DRMSystemList></cpix:CPIX>","isBase64Encoded": false}'


rm -rf "$ORIGIN/src/__pycache__"
