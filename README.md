# QGIS Plugin base

This QGIS plugin base is heavily based on a plugin that can be created with Plugin Builder plugin.

[Good source for PyQGIS examples](https://github.com/webgeodatavore/pyqgis-samples)
[QGIS Python API Documentation](https://www.qgis.org/pyqgis/master/)
[PyQt5 Reference Guide](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
[PyQt5 API Documentation](https://doc.bccnsoft.com/docs/PyQt5/)

## Setup

### Environment installation & setup

NOTE: There exists alternative ways to do this. However, following ways have been tested.

Download OSGeo4W network installer and choose Express Desktop install. It installs all necessary tools (GDAL, PyQt5, QtDesigner, Python etc.) for QGIS plugin development with QGIS itself. After this you can use OSGeo4W shell to access these tools. Other option is to use Python CLI opened from `C:\OSGeo4W64\bin\python-qgis.bat` script or set `C:\OSGeo4W64\apps\Python37` and `C:\OSGeo4W64\apps\Python37\Scripts` as path variables. Another way is to install all of the needed dependencies manually to existing python installation.

On your desired IDE set you Python interpreter according to the preferred python installation (development chapter contains insturctions how to se it inside VsCode).

#### Windows

For Windows environment run `compile.bat` to compile QT resources file into .py file to be used by Python plugin code. Additionally, indicate path to the QGIS install from current plugin path by running `o4w_env.bat`, `qt5_env.bat` & `py3_env.bat` scripts.

#### Linux

For Linux environment install python-qt5 package. Depending on your distribution change the following script `sudo apt-get install python-qt5`.

#### Max

For Mac environment install PyQt package with following command `brew install pyqt`.

#### External Python dependencies

Python pip packages can be installed using e.g. `python-qgis.bat -m pip install` or `C:\OSGeo4W64\apps\Python37\python.exe -m pip install`. The last command assumes that you have installed pip for this Python intepreter.

### Plugin installation

1. Git clone this repository into `C:\Users\%USERPROFILE%\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins` folder or `C:\OSGeo4W64\apps\qgis\python\plugins` (if there is a need for global place for plugins).
2. Optionally create symbolic link from `C:\OSGeo4W64\apps\qgis\python\plugins` path to user profile path (can be useful in production setting) by running following command prompt  command `mklink /D C:\Users\%USERPROFILE%\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\<plugin-folder-name> C:\OSGeo4W64\apps\qgis\python\plugins\<plugin-folder-name>`
3. Go to this folder and compile plugin resources with `pyrcc5 -o resources.py resources.qrc` (skip this step if compile.bat has been run already)
4. Restart QGIS in order to load profiles again (with plugin)
5. Add plugin `Plugins` -> `Manage and Install Plugins...` -> `Installed` and check the copied plugin

## Development

Main tools/applications for development are your IDE (Qt Creator, VsCode etc.) and Qt Designer. Additionally, Qt Linguist application exist for managing plugin translations.

### Qt Designer

This is a convenient tool for designing plugin ui. It straightly modifies opened .ui files. QDialog class provides access to named elements with the set name e.g. self.dlg.test_button. Additionally these elements can be connected for listening UI events.

### Plugin Reloader

Plugin reloader (QGIS Plugin) enables reloading (compiling) project code after code changes. It can be downloaded for QGIS plugins. Hot key for using it is `CTRL + F5`.

### Linting (vscode)

Project has pylint configuration file `.pylintrc`. This file contains rules that are used to detect informalities inside python code.

To generate empty .pylintrc configuration file run (this project already includes this):

`pylint --generate-rcfile | Out-File -Encoding utf8 .pylintrc`

In order to use pylint, install it for the used Python interpreter.

1. Check Python interpreter `CTRL + SHIFT + P -> Python: Select Interpreter`
2. Install pylint to selected interpreter -> `pip install pylint`
3. To be sure check that vscode settings file contains following lines:

```
CTRL + SHIFT + P -> Preferences: Open Settings (JSON)

"python.linting.enabled": true,
"python.linting.lintOnSave": true,
"python.linting.pylintEnabled": true,
```

4. Additionally, check the following settings:

```
CTRL + SHIFT + P -> Python: Select Linter -> pylint
CTRL + SHIFT + P -> Python: Enable Linting -> on
```

5. Check that pylint can be run manually:

```
CTRL + SHIFT + P -> Python: Run Linting
```

### Translations

This project contains example for creating translations in Finnish & English. 

Utilities folder contains translations.py file that has tr-method. This method can be used to map desired translation key to desired texts. .ui-files are automatically detected and generated from these keys.

Run following command to create Finnish and English translations for these keys. Everytime you create new translations key run this command, so they are created into .ts-files.

`./i18n/update-translations.sh`

Compile translations into .qm-files in order to QGIS to read them on plugin start. The correct language is automatically detected, since it is read from QSettings configuration class. Everytime you make changes to the translations you need to run this.

`./i18n/compile-translations.sh`

### Debugging

More IDE debugging options [here](https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins/ide_debugging.html). Modify `__init__.py` to set more debugging options

#### Visual Studio Code ([ptvsd](https://github.com/microsoft/ptvsd))

NOTE: Heavily based on this [gist](https://gist.github.com/veuncent/c4589af14af42941ac0b0310e8240d6c)

1. Select QGIS python as folder interpreter:
```
CTRL + SHIFT + P -> Python: Select intepreter -> C:\OSGeo4W64\apps\Python37\python.exe
```
2. Install ptvsd
```
pip install ptvsd==4.3.2
```
3. Set `QGIS_PLUGIN_USE_DEBUGGER` environment variable as `ptvsd`
4. Add debug configuration to launch.json-file
```
{
  "name": "Python: Remote Attach",
  "type": "python",
  "request": "attach",
  "port": 5678,
  "host": "localhost",
  "pathMappings": [
    {
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "${workspaceFolder}"
    }
  ]
}
```
5. Run this debug configuration from vscode and add desired breakpoints

### Dev environment database

1. Install [docker](https://docs.docker.com/docker-for-windows/install/).
2. Run `docker-compose.yaml` file inside dev-folder by running `docker-compose -f docker-compose.yaml up --build`
3. PostgreSQL (with PostGIS) is running on port 5432 and can be accessed from localhost.

Docker container is based on image ([kartoza/postgis](https://github.com/kartoza/docker-postgis)). Link contains more configuration options.

Inside docker-compose.yaml you can specify initial sql-scripts that are run on container start. Currently it runs `setup-db.sql` file that creates dummy table with one row of data.

```
Build container
$ docker-compose -f docker-compose.yaml build

Start container
$ docker-compose -f docker-compose.yaml up

Start and build container
$ docker-compose -f docker-compose.yaml up --build
```

Optionally there is a possibility to store the PostgreSQL data directory inside host machine. If the container PostgreSQL data volume is attached data will persist even if the container is removed.

```
Connect to database from container cli
$ psql -h localhost -U postgres
```

Some useful PostgreSQL commands:

```
Close connection
$ \q

List databases
$ \l

Connect to database
$ \c test_db

List tables inside database
$ \d

List schemas
$ \dn

List functions
$ \fn

List views
$ \dv
```

## Workspace file

Depending on project it is usually desired to save template workspace for project. This can be included with the project files with type .qgs. Other possiblity is to use zipped version .qgz, but it makes following workspace file changes in version control difficult.

## User profiles

`Settings` -> `User Profile` -> ...

By default user profile named `default` is used. All of its related data is stored under `C:\Users\%USERPROFILE%\AppData\Roaming\QGIS\QGIS3\profiles\default`.

Different profiles can be used to store e.g. different template workspaces, plugins.

## Database

### Database authentication

Database authentication can be done using QGIS internal authentication configuration. Every QGIS user has its own configuration file e.g. `db-auth` that plugin interacts with on start. Configuration file can be created from `Settings` -> `Options` -> `Authentication` -> `Add new authentication configuration`. Configuration has following parameters:

- Name -> Name of the configuration file. Used for loading auth config
- Id -> Id of the auth config. Used for accessing auth config
- Type -> Authentication type. Basic authentication is suggested for simple configuration (username, password)
- Username -> db username
- Password -> db password

After creation Master Password needs to be set for QGIS. This is for opening authentication configurations, therefore it is prompted on start of plugin. It can be reseted from `Utilities` -> `Reset master password`.

Generally speaking QGIS saves this auth configuration to users `qgis-auth.db` file. It can be found from users AppData path -> `C:\Users\%USERPROFILE%\AppData\Roaming\QGIS\QGIS3\profiles\default`. Due to this, it is convenient to seperate user data from project files.

### Database connection

Proided utility class DbConnection contains example methods for creating db connection with PostgreSQL database. Class variables `authConfigId` and `authConfigName` has to be set based on instuctions above. Additionally following environment variables needs to set for creating connection since authentication configuration only stores username and password.

- PGDATABASE -> db-name
- PGPORT -> db-port
- PGHOST -> db-host
- PGSSLMODE -> disable

If you are developing on Linux-environment check that Qt `QPSQL`-driver is installed by running following .py script:

```
from PyQt5.QtSql import QSqlDatabase
print(QSqlDatabase.isDriverAvailable('QPSQL))
```

If it is not installed. Install it by running following command

`$ sudo apt install libqt5sql5-psql`

### Database relations

Database relations can be set here.

`Project` -> `Properties...` -> `Relations`

This contains all relations between schema tables.

When setting relations between tables it enables displaying related tables inside attribute tables.

NOTE: QGIS might have some difficulties with creating many-to-many relations
