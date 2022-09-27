import os.path

def index():
    with open(os.path.join(os.path.curdir, 'templates', 'index.html'), 'r') as template:
        return template.read()


def blog():
    with open(os.path.join(os.path.curdir, 'templates', 'blog.html'), 'r') as template:
        return template.read()


