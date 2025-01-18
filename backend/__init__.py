import os
from flask import Flask

template_folder_path = os.path.join(os.getcwd(), "templates")
static_folder_path = os.path.join(os.getcwd(), "static")
app = Flask(__name__, static_folder=static_folder_path, template_folder=template_folder_path)

import backend.routes