#!/usr/bin/env bash

# run after testing the ctf

lxc list -c n --format csv | xargs -i"{}" lxc restore {} backup
