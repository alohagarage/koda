#!/usr/bin/env python

import sys, os, json

from itertools import izip, tee

from pprint import pprint

from bs4 import BeautifulSoup as bsoup

from xml2json import xml2json

def fishing(proj_dir):
    # for when you have to find the xml files in hidden directories
    addendum = '.koda' if proj_dir.endswith('/') else '/.koda'
    file_list = os.listdir(proj_dir + addendum)
    return file_list


def file_list(dir):
    file_list = [dir + '/' + file for file in os.listdir(dir)]
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
        if track != '\n':
            if track.name:
                obj = {'id': track['id'], 'type': track.name}
                devices = []
                for device in track.find('devices').children:
                    if device != '\n':
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
        if child != '\n':
            if child.name:
                obj[child.name] = child.attrs
    return obj

def make_set_file(file_list):
    out = []
    for file in file_list:
        #print file
        f = open(file, 'r')
        xml = f.read()
        #print xml
        try:
            dict =json.loads(xml2json(xml, 0, 1))
            dict['@XMLFilename'] = file
            out.append(dict)
        except Exception as e:
            print e
    return out


def main():
    final_json = json.dumps(make_set_file(file_list(sys.argv[1])), indent=4)
    f = open('diff_log.json', 'w')
    f.write(final_json)
    return final_json

if __name__ == '__main__':
    print main()
