__author__ = 'ceremcem'

def make_unicode(input):
    if type(input) != unicode:
        input = input.decode('utf-8')
        return input
    else:
        return input
