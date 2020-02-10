#!/bin/sh
curl -O https://beta.quicklisp.org/quicklisp.lisp
if [ -d /home/eliza-chatbot/quicklisp ] ;
then
    sbcl --script load-quicklisp.lisp
else
    echo "Installing quicklisp!"
    sbcl --script install.lisp
fi
