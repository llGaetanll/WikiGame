# %%
import json
from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    return json.dumps({'name': 'alice',
                       'email': 'alice@outlook.com'})


app.run()
