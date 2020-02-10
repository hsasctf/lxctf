# enter a secret key for flask
SECRET_KEY = b'Y\x1d@j\xcbj\x8fhg\xd6\xeb\xbf"\x03P\x9c'

DEBUG=False

NAME_CTF = "HSAlbSigCTF"
AUTHORS = "Leo, Dominik, Anton, Peter"
YEAR = 2020
FOOTER_DESCRIPTION = """We are a team of students who develop a Capture the Flag for
                    Albstadt-Sigmaringen University."""

#ALLOWED_IP_RANGES = []
ALLOWED_IP_RANGES = ["127.0.0.0/8", "141.87.0.0/16",  "172.16.17.0/24", "10.38.1.0/24", "10.41.0.0/24", "10.40.0.0/24", "192.168.0.0/16"]


# set this for verification links to work (without trailing /)
URL_BASE = "141.87.8.20"

# enter a mailserver that is trusted by the spamfilter of your recipients :)
MAIL_SERVER = "mail.gmx.net"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "hsctf@gmx.net"
MAIL_PASSWORD = "hsctf2020_pdal"
MAIL_DEFAULT_SENDER = "hsctf@gmx.net" # trusted sender address
MAIL_REPLY_TO = "hsctf@gmx.net"  # the mailbox when someone hits reply
