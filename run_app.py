
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    from main import app

    httpd = make_server('localhost', 5555, app)
    httpd.serve_forever()
