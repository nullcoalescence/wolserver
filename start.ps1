# starts application in development env
# usage: ./start.ps1

$env:FLASK_APP = "server"
$env:FLASK_ENV = "development"

flask run