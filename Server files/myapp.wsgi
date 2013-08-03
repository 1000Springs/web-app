import sys
activate_this = '/home/ubuntu/opt/local/webapp/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0,'home/ubuntu/opt/local/webapp/')
from hotspringsapp import app as application
