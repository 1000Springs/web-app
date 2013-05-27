from flask.ext.script import Manager, Shell, Server

from hotspringsapp import app

manager = Manager(app)
manager.add_command("runserver", Server())
manager.add_command("shell", Shell())
manager.run()