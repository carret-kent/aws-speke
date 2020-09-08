# about
https://docs.aws.amazon.com/speke/latest/documentation/what-is-speke.html

Key provide operation of the AWS SPEKE.
Only supports `HLS AES 128` Encryption and input of single content key.

This code was created with reference to two repositories.  
Thanks so much.
- https://github.com/OdaDaisuke/aws-speke
- https://github.com/awslabs/speke-reference-server

# environ
- local: use `src/.env` files.
- Lambda: set lambda console.

| key | description |
| ---- | ---- |
| APP_ENV | `local`: use cache_driver_mock, `other`: use cache_driver_s3 |
| SYSTEM_ID | Use Validation. set request body same value. |
| DERIVED_DOMAIN_URL | Distributing from Cloud front, set the domain.<br>Distributing from S3, set the domain. |
| KEY_STORE_BUCKET | Store s3 bucket name. |
| KEY_STORE_BUCKET_PREFIX | s3 put object need prefix, set any prefix. |

# build
This build tool use Python3.6.
If you use windows pc. You must use cygwin bash and exec option `-w`, install zip comand.

```
sh build.sh
```

ref. [lambci github code](https://github.com/lambci/docker-lambda)

# local test
This test tool use Python3.6.

## init
Create your test.env file. 
Copy file and write env info.
If you use windows pc. You must use cygwin bash and exec option `-w`.
```
cp ./src/.env.local ./src/.env
sh pip.sh
```

## run
If you use windows pc. You must use cygwin bash and exec option `-w`.
```
sh test.sh
```
