#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import requests
import json
import math
import random
from requests.exceptions import ConnectionError


domoticz_server = "http://localhost"
domoticz_port = 8080
domoticz_device = 1
alert_range = 25  # in km
random_debug = 0 # 1 for enable

llatHome = xx.xxxxx
lngHome = xx.xxxx
# Try to get the data from domoticz
try:
    data = json.loads(
        requests.get(
            "%s:%d/json.htm?type=settings" %
            (domoticz_server, domoticz_port)).content)
    latHome = float(data['Location']['Latitude'])
    lngHome = float(data['Location']['Longitude'])
except:
    pass


class GripAlert:

    def __init__(self):
        self.link = "http://feeds.livep2000.nl/"
        if random_debug:
            self.push(random.randint(0, 4), "debug push")
        self.fetch()

    def push(self, level, text):
        try:
            requests.get(
                "%s:%d/json.htm?type=command&param=udevice&idx=%d&nvalue=%d&svalue=%s" %
                (domoticz_server, domoticz_port, domoticz_device, level, text))
        except ConnectionError:
            print "I wasn't able to contact the domoticz server, is it up?"

    def fetch(self):
        # fetch the data and push it
        z = requests.get(self.link)
        elements = ET.fromstring(z.content).getchildren()[0].getchildren()

        pushed = 0
        for element in elements[7:]:
            data = element.getchildren()
            try:
                title = data[0].text.replace("<br/>", "\n")
                description = data[3].text.replace("<br/>", "\n")
                lat = float(data[6].text)
                lng = float(data[7].text)
                if not (self.calculateDistance(latHome, lngHome, lat,
                        lng) <= alert_range):
                    continue

                level = 0
                if ("grip: 1" in title.lower()
                        or "grip: 1" in description.lower()):
                    level = 1
                elif ("grip: 2" in title.lower() or "grip: 2" in description.lower()):
                    level = 2
                elif ("grip: 3" in title.lower() or "grip: 3" in description.lower()):
                    level = 3
                elif ("grip: 4" in title.lower() or "grip: 4" in description.lower()):
                    level = 4

                if not level:
                    continue

                message = "%s\n%s" % (title, description)
                self.push(level, message)
                print "Pushed alert, GRIP Level: %d\nMessage: %s" % (level, message)

                pushed += 1
            except:
                pass

        if not pushed:
            print "No alerts were pushed"

    def calculateDistance(self, lat1, lng1, lat2, lng2):
        radius = 6371

        dLat = (lat2 - lat1) * math.pi / 180
        dLng = (lng2 - lng1) * math.pi / 180

        lat1 = lat1 * math.pi / 180
        lat2 = lat2 * math.pi / 180

        val = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLng / 2) * \
            math.sin(dLng / 2) * math.cos(lat1) * math.cos(lat2)
        ang = 2 * math.atan2(math.sqrt(val), math.sqrt(1 - val))
        return radius * ang


GripAlert()
