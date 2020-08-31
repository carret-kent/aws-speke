# aws-speke

https://docs.aws.amazon.com/speke/latest/documentation/what-is-speke.html

Key provide operation of the AWS SPEKE.
Only supports HLS AES 128 Encryption and input of single content key.


# build
```
git submodule init
git submodule update
cp ./lambci/python3.6/build/Dockerfile Dockerfile
echo 'CMD ["/bin/bash"]' >> ./Dockerfile
docker-compose build
```