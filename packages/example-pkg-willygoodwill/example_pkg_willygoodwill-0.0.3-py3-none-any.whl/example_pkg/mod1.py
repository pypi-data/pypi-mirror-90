def load_data():
    print('Load info about module mod1')
    from example_pkg import alist
    print(f'this is from pakage init - {alist}')

class Products(object):
    def __init__(self):
        self.name = 'My package to parse data from Ikea'
    def __str__(self):
        return str(self.name)