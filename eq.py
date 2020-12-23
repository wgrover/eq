#!/usr/bin/env python3

import json
import urllib.request
import time
import curses

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main(stdscr):
    curses.curs_set(False)
    curses.halfdelay(50)  # units are tenths of a second, so 50 = 5 seconds
    curses.noecho()
    (ymax, xmax) = stdscr.getmaxyx()
    while True:
        stdscr.clear()
        for x in range(xmax):
            stdscr.addch(0, x, ' ', curses.A_REVERSE)
        stdscr.addstr(0,0," Mag  Time    Location", curses.A_REVERSE)
        stdscr.addstr(9,9,str(time.time()), curses.color_pair(1))
        url = urllib.request.urlopen("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_day.geojson")
        data = json.loads(url.read().decode())
        stdscr.addstr(0,xmax-36,
                      time.strftime("Updated %a %b %d %Y %I:%M:%S %p", time.localtime()),
                      curses.A_REVERSE)
        line = 0
        for feature in data["features"]:
            if line>ymax-2:
                break
            p = feature["properties"]
            mag = p["mag"]
            min = (time.time() - p["time"] / 1000) / 60
            place = p["place"]
            if place.endswith(" CA"):
                stdscr.addstr(line+1, 1, f"{mag:.1f}")
                if min<60:
                    stdscr.addstr(line+1, 6, f"{round(min)} min")
                else:
                    stdscr.addstr(line+1, 6, f"{min/60:.1f} h")
                stdscr.addstr(line+1, 14, f"{place}")
                line += 1
        char = stdscr.getch()
        if char != curses.ERR:
            exit()
        else:
            stdscr.refresh()
curses.wrapper(main)
