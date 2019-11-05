#!/usr/bin/env bash

# run after services are deployed

lxc list -c n --format csv | xargs -i"{}" lxc stop {}
lxc list -c n --format csv | xargs -i"{}" lxc delete {}/backup
lxc list -c n --format csv | xargs -i"{}" lxc snapshot {} backup
lxc list -c n --format csv | xargs -i"{}" lxc start {}
