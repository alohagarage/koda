#!/usr/bin/env python

import sys, os

from itertools import izip, tee

from pprint import pprint

from bs4 import BeautifulSoup as bsoup

def fishing(proj_dir):
    # for when you have to find the xml files in hidden directories
    addendum = '.koda' if proj_dir.endswith('/') else '/.koda'
    file_list = os.listdir(proj_dir + addendum)
    return file_list

def file_list(dir):
    file_list = os.listdir(dir)
    print file_list
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

def get_devices(soup):
    out = []
    for track in soup.find('tracks').children:
        # good test to see if it is a valid node
        if track.name:
            obj = {'id': track['id'], 'type': track.name}
            devices = []
            for device in track.find('devices').children:
                if device.name:
                    devices.append(make_device_object(device))
            obj['devices'] = devices
            out.append(obj)
    return out

def make_device_object(device):
    obj = {}
    obj['name'] = device.name
    obj['id'] = device['id']
    for child in device.children:
        if child.name:
            obj[child.name] = child.attrs
    print obj
    return obj


def main():
    tuple =  [t for t in comparison_tuples(file_list(sys.argv[1]))][-1]
    return get_devices(open_xml(tuple)[0])

if __name__ == '__main__':
    pprint(main())
