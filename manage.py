# - this file is used for database migration
# - after deployed, after any change made to database models,
#   should run this file to map changes in models to the remote
#   databaseself.
# - useful operations:
#   python3 manage.py db init -> used to create the menu structure for migrations file, needed first time
#   python3 manage.py db migrate -> migrate changes
#   python3 manage.py db upgrade -> map to remote
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
