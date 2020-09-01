# aws-speke

https://docs.aws.amazon.com/speke/latest/documentation/what-is-speke.html

Key provide operation of the AWS SPEKE.
Only supports HLS AES 128 Encryption and input of single content key.


# build
This build tool use Python3.6.
If you use windows pc. You must use cygwin bash and exec option `-w`, install zip comand.

```
sh build.sh
```

ref. [lambci github code](https://github.com/lambci/docker-lambda)

# test
This test tool use Python3.6.

## init
Create your test.env file. 
Copy file and write env info.
```
cp ./src/.env.test ./src/.env
```

## run
If you use windows pc. You must use cygwin bash and exec option `-w`.
```
sh test.sh
```
