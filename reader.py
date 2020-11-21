import os
import csv
import argparse
import sys
import json


def main(argv):
    parser = argparse.ArgumentParser(description="Given csv files describing functions,"
                                                 " calculate their integrals over given intervals")
    parser.add_argument("path", metavar="PATH", type=str, nargs=1)
    parser.add_argument("start", metavar="START", type=float, nargs=1)
    parser.add_argument("end", metavar="END", type=float, nargs=1)
    parser.add_argument("--csv_separator", "-c", type=str, nargs=1, default=";")
    parser.add_argument("--european_number", "-e", "--euro", dest="euro", action="store_const", const=True, default=False)
    parser.add_argument("--zerobase", "-z", dest="nobase", action="store_const", const=True, default=False)
    parser.add_argument("--debug", "-d", dest="debug", action="store_const", const=True, default=False)
    args = parser.parse_args()

    results = {}
    start = args.start[0]
    end = args.end[0]
    path_name = args.path[0]
    euro = args.euro
    nobase = args.nobase
    debug = args.debug
    csv_separator = args.csv_separator[0]

    if os.path.isdir(path_name):
        for file in [f for f in os.listdir(path_name) if os.path.isfile(os.path.join(path_name, f))]:
            fullpath = os.path.join(path_name, file)
            results[fullpath] = integral_from_file(fullpath, start, end, csv_separator, euro, nobase, debug)
    else:
        results[path_name] = integral_from_file(path_name, start, end, csv_separator, euro, nobase, debug)

    print(json.dumps(results))
    return results


def integral_from_file(file, start, end, separator, euro, nobase, debug):
    dp = DebugPrinter(debug)
    idx_X = 0
    idx_Y = 1
    with open(file) as f:
        reader = csv.reader(f, delimiter=separator)
        vals = [[get_float(x[idx_X], euro), get_float(x[idx_Y], euro)] for x in reader if end >= get_float(x[idx_X], euro) >= start]
        dp.p(vals)
        if len(vals) == 0:
            return 0
        else:
            s = sum([x[idx_Y] for x in vals])
            base = baseline(vals[0][idx_Y], vals[-1][idx_Y], (vals[-1][idx_X] - vals[0][idx_X] + 1))
            if nobase:
                return s
            else:
                return s - base


def baseline(start_Y, end_Y, length_X):
    return (start_Y + end_Y) * length_X / 2.


def get_float(num_str, euro=False):
    n = num_str.replace(",", ".") if euro else num_str
    return float(n)


class DebugPrinter:
    def __init__(self, debug):
        self.debug = debug

    def p(self, v):
        if self.debug:
            print(v)


if __name__ == "__main__":
    main(sys.argv[1:])
