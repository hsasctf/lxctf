#!/usr/bin/env bash

# run after testing the ctf (for testing the ctf on the production system, to return to a clean state after testing)

lxc list -c n --format csv | xargs -i"{}" lxc restore {} backup
