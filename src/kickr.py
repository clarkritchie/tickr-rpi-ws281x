#!/usr/bin/env python3
import time, json, random
import argparse
from singleton import Singleton

@Singleton
class Strand:
    def do_stuff(self, data):
        print(data)
    def __init__(self):
        print("Strand constructor")

@Singleton
class Tickr:
    def sample_data(self):
        value = {
            "value": random.randint(50, 180)
        }
        # Dictionary to JSON Object using dumps() method, returns JSON
        return value
    def __init__(self):
        print("TICKR constructor")

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-m', '--mac', help='clear the display on exit')
    args = parser.parse_args()
    
    print(f'MAC is {args.mac}')

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            tickr = Tickr.instance() # Good. Being explicit is in line with the Python Zen
            strand = Strand.instance()
            strand.do_stuff(tickr.sample_data())
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")
        if args.clear:
            print("Clear stuff here")