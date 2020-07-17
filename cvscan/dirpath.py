import os
from cvscan.configurations import get_env_var

CURRENT_DIR_PATH = os.getcwd()
RESUMEPATH = get_env_var("CVSCAN_RESUME_PATH", CURRENT_DIR_PATH)

PKGPATH = os.path.dirname(os.path.abspath(__file__))
