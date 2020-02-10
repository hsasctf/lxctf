#!/bin/bash
for num in {1..254} 
do
    sudo wg-quick down wg$num
done
