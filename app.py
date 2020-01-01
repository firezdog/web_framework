from server import Server

# callable entry point for gunicorn
app = Server()

@app.route("/")
def root(request, response):
    response.text = "Root route"

@app.route('/home')
def home(request, response):
    response.text = "Home page"


@app.route('/other')
def other(request, response):
    response.text = "Other page"

@app.route('/hello/{name}')
def hello(request, response, name):
    response.text = f"Hello, {name}"