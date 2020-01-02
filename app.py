from server import Server

# callable entry point for gunicorn
app = Server()


@app.route('/')
def root(request, response):
    response.text = 'Root route'


@app.route('/home/another')
def another(request, response):
    response.text = 'Another home'


@app.route('/home')
def home(request, response):
    response.text = 'Home page'
