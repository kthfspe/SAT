from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():

    return 'Hello World'

hello_world.__doc__ = "This is docstring testing"

if __name__ == '__main__':
    """ inits Spamfilter with training data
        
    :param training_dir: path of training directory with subdirectories
     '/ham' and '/spam'
    """
    # The server is run directly
    app.debug = True
    app.run()
# else: (If imported by another module)