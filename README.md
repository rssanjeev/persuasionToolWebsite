This is the Persuasion Tool Website developed for BITSLAB.

- nltk.txt
  Contains all of the libs needed by nltk.

- models
  Contains all machine learning models used by the website.

- app
  Contains .py files, .csv files, .db files and so on.
  - home.py handles the backend events with flask framework.
  - tool.py using machine learning libraries to calculate persuasion,
    it also has a "gettingFeatures" function used to get the specific
    features of given statement.
  - schema.sql defines the structure of the local database.
  - feedbacks.db store the content of the local database.
  - npersuasiveClassification.csv and persuasiveClassification.csv are
    data files saving training data set.

  - static
  	Contains all .css files for the website.
  - templates
    Contains all .html files for the website.

- config.py
  Contains the configuration for flask framework, however, it
  doesn't work on Heroku.

- Procfile
  A file needed by Heroku, tell Heroku how to start you app.

- requirements.txt
  A file needed by Heroku, contains all the python libs needed by
  this app. In this file, there are some redundant libs cause I
  didn't use a virtual environment, it's better to use the venv.

- Unfinished function
  The "export" function is unfinished cause the special design for
  dyno. Dyno is something like a sandbox or a virtual machine. In
  order to have better performance and liability, Heroku choose to
  use dyno to manage the resources. There's no conection between
  different dynos. Thus, it's hard to get data out from it. And, dyno
  has e ephemeral file system, when it restart, it will lose all dynamic
  data. And all the files will back to the status of the last deployed
  version.
