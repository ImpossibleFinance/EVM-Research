
import flask

from scripts.Functions import *

# Before: pip3 install -r requirements.txt

###############################################################
############################# App #############################
###############################################################

server = flask.Flask(__name__)
app = Dash(
    __name__, 
    server = server, 
    use_pages = True
)

app.layout = html.Div([])

if __name__ == '__main__':
    app.run_server(debug = True)