
# Install Dependencies
`poetry install`
# Start poetry virtual env
`poetry shell`
# Export flask path env
`export FLASK_APP=app/webapp.py`
# Debug mode
`export FLASK_DEBUG=1`
# Create db

`flask shell`

`from app.webapp import app,db`

`from app.models import User,Models`

`app.app_context().push()`

`db.create_all()`

`exit()`
# Run app
`flask run`
