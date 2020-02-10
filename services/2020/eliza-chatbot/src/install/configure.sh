#!/bin/sh
./prepare.sh 

# something to look
cd ~/eliza-chatbot/install/
cp ../www/always-look-on-the-bright-cyber.png ~/quicklisp/dists/quicklisp/software/hunchentoot-v1.2.38/www/
cp ../www/eliza.css  ~/quicklisp/dists/quicklisp/software/hunchentoot-v1.2.38/www/

# start the server
cd ~/eliza-chatbot/install/
nohup ./eliza-chatbot.lisp &
