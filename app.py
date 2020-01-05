from server import Server

# callable entry point for gunicorn
app = Server()


@app.route('/')
def root(request, response):
    response.text = 'root'


@app.route('/name')
def name(request, response):
    response.text = 'enter your name'


@app.route('/name/in/depth')
def depth(request, response):
    response.text = 'going deep'


@app.route('/name/in')
def ok(request, response):
    response.text = 'this should be ok'


# @app.route('/name')
# def new_name(request, response):
#     response.text = 'this should not'


@app.route('/name/{first}')
def hello(request, response, first):
    response.text = f'hello, {first}'


@app.route('/name/{first}/{last}')
def full_name(request, response, first, last):
    response.text = f'hello, {first} {last}'


