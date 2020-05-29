#!/usr/bin/env python3

import dash
import dash_auth

from configure.login import *

app = dash.Dash(__name__, url_base_pathname='/vbc-demo/launch/')
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server = app.server

app.config.suppress_callback_exceptions = True


auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
