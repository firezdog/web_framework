from server import Server

# callable entry point for gunicorn
app = Server()

@app.route('/home')
def home(req, res):
    res.text = "Home page"

@app.route('/other')
def other(req, res):
    res.text = "Other page"
    