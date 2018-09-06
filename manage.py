# from app import create_app
import os
from app import *
from app.models import *
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
#
# if __name__ == '__main__':
#     manager.run()

if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    # manager.run(host='0.0.0.0', port=port)
    manager.run()
