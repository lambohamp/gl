#!/bin/bash

# vars
path_to_echofile=/tmp/test.txt
path_to_pem=/test.pem
user=ubuntu
ip=0.0.0.0

# the script echoes the value of $MY_SECRET variable taken from Azure Key Vault secret to a file and then copies that file to a remote machine

echo $MY_SECRET >> $path_to_echofile && scp -i $path_to_pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $path_to_echofile $user@$ip:~
