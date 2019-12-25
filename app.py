from server import Server

# callable entry point for gunicorn
app = Server()


@app.route('/home')
def home(request, response):
    response.text = "Home page"


@app.route('/other')
def other(request, response):
    response.text = "Other page"
