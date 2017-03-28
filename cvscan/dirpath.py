import os
from configurations import get_env_var

RESUMEPATH = os.path.expanduser("~") + '/cvscan'
RESUMEPATH = get_env_var("CVSCAN_RESUME_PATH", RESUMEPATH)

DATAPATH = os.path.join(os.path.expanduser("~") + '/.cvscan', 'data')
PKGPATH = os.path.dirname(os.path.abspath(__file__))
