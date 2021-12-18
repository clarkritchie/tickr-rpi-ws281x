#!/usr/bin/env python3
import time, json, random
import argparse
from singleton import Singleton

@Singleton
class Tickr:
    def sample_data(self):
        value = {
            "value": random.randint(50, 180)
        }
        # Dictionary to JSON Object using dumps() method, returns JSON
        return json.dumps(value)
    def __init__(self):
        print("TICKR constructor")

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            tickr = Tickr.instance() # Good. Being explicit is in line with the Python Zen
#             g = Foo.instance() # Returns already created instance
#             print(f is g)
            print(tickr.sample_data())
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")
        if args.clear:
            print("Clear stuff here")