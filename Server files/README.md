How to get a flask web app running on mod_wsgi

----------APACHE CONFIG FILE
Add apache config file to /etc/apache2/sites-available
- no file extension required

<VirtualHost *:80>

 # ---- Configure VirtualHost Defaults ----

    ServerAdmin test@test.com

        DocumentRoot /home/ubuntu/opt/local/webapp/hotspringsapp

        <Directory />
                Options FollowSymLinks
                AllowOverride None
        </Directory>

        <Directory /home/ubuntu/opt/local/webapp/hotspringsapp/>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride None
                Order allow,deny
                allow from all
        </Directory>

        # ---- Configure WSGI Listener(s) ----

        WSGIDaemonProcess flaskapp user=www-data group=www-data threads=5
        WSGIScriptAlias / /home/ubuntu/opt/local/webapp/myapp.wsgi

        <Directory /home/ubuntu/public_html/http/flasktest1>
                WSGIProcessGroup flaskapp
                WSGIApplicationGroup %{GLOBAL}
                Order deny,allow
                Allow from all
        </Directory>

        # ---- Configure Logging ----

    ErrorLog /home/ubuntu/public_html/logs/error22.log
    LogLevel warn
    CustomLog /home/ubuntu/public_html/logs/access.log combined

</VirtualHost>

run sudo a2ensite <config filename> to add it to the sites-enabled folder
run sudo a2dissite <config filename> to disable the site

if another port is being used then the /etc/apache2/ports.conf file needs to be added

NameVirtualHost *:<port number>
Listen <port number>



--------------WSGI FILE

the wsgi file needs to be in the top level folder of the webapp

/webapp
	/hotspringsapp
	/insertdata
	manage.py
	<filename>.wsgi
	etc...

wsgi file should be as follows

####MYAPP.WSGI####
import sys
	/*	----this is if virtualenv is being used 
	 *	activate_this = '/home/ubuntu/opt/local/webapp/venv/bin/activate_this.py'
	 *	execfile(activate_this, dict(__file__=activate_this))
	 */
	 
sys.path.insert(0,'home/ubuntu/opt/local/webapp/')
from hotspringsapp import app as application
####END####
	
Check to see that 

Python <filename>.wsgi 

will load correctly - http://stackoverflow.com/questions/8943421/cannot-import-module


--------------Restarting Apache

After that is all done apache just needs to load the new config files in

sudo service apache2 reload

curl http://localhost:<port number> should return something