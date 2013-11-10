#!/usr/bin/env python

import sys, os

from itertools import izip, tee

from bs4 import BeautifulSoup as bsoup

def fishing(proj_dir):
    # for when you have to find the xml files in hidden directories
    addendum = '.koda' if proj_dir.endswith('/') else '/.koda'
    file_list = os.listdir(proj_dir + addendum)
    return file_list

def file_list(dir):
    file_list = os.listdir(dir)
    return file_list

def comparison_tuples(list):
    # separate into tuples
    a, b = tee(list)
    next(b, None)
    return izip(a, b)

def open_xml(tuple):
    # open a tuple into a python-friendly form
    path = 'xml/'
    xml_a = bsoup(open(path + tuple[0], 'r').read())
    xml_b = bsoup(open(path + tuple[1], 'r').read())
    return xml_a, xml_b


def main():
    tuple =  [t for t in comparison_tuples(file_list(sys.argv[1]))][0]
    return open_xml(tuple)

if __name__ == '__main__':
    print main()
