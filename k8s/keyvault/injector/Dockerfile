FROM ubuntu:latest
# install ca-certificates package required by Injector and openssh-client for the sh script
RUN apt-get update && apt install -y ca-certificates openssh-client
# copy private key so the sh script can access a remote machine
COPY test.pem /
# copy the script itself
COPY test.sh /usr/local/bin/
# start the script
ENTRYPOINT ["test.sh"]
CMD []
