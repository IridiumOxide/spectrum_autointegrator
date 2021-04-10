import os
import csv
import argparse
import sys
import json


idx_X = 0
idx_Y = 1


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
    parser.add_argument("--print_csv", "-p", dest="print_csv", action="store_const", const=True, default=False)
    args = parser.parse_args()

    results = {}
    start = args.start[0]
    end = args.end[0]
    path_name = args.path[0]
    euro = args.euro
    nobase = args.nobase
    debug = args.debug
    print_csv = args.print_csv
    csv_separator = args.csv_separator[0]

    if os.path.isdir(path_name):
        for file in [f for f in os.listdir(path_name) if os.path.isfile(os.path.join(path_name, f))]:
            fullpath = os.path.join(path_name, file)
            results[fullpath] = integral_from_file(fullpath, start, end, csv_separator, euro, nobase, debug)
    else:
        results[path_name] = integral_from_file(path_name, start, end, csv_separator, euro, nobase, debug)

    if print_csv:
        for k in results:
            print(f'{k},{results[k]}')
    else:
        print(json.dumps(results))
    return results


def integral_from_file(file, start, end, separator, euro, nobase, debug):
    dp = DebugPrinter(debug)
    with open(file) as f:
        reader = csv.reader(f, delimiter=separator)
        vals = [[get_float(x[idx_X], euro), get_float(x[idx_Y], euro)] for x in reader if end >= get_float(x[idx_X], euro) >= start]
        dp.p(vals)
        dp.p(len(vals))
        if len(vals) == 0:
            return 0
        else:
            s = trapeze_integral(vals)
            base = min_min_baseline(vals, debug)
            if nobase:
                return s
            else:
                return s - base


# just rectangles with X = 1 and Y = point's Y
def rect_integral(vals):
    sum([x[idx_Y] for x in vals])


# makes no sense for single value
def trapeze_integral(vals):
    i = 1
    totalsum = 0.0
    while i < len(vals):
        trap_a = vals[i][idx_Y]
        trap_b = vals[i-1][idx_Y]
        trap_h = abs(vals[i][idx_X] - vals[i-1][idx_X])
        trap_s = (trap_a + trap_b) * trap_h / 2.0
        totalsum += trap_s
        i += 1
    return totalsum


def start_end_baseline(vals, debug):
    dp = DebugPrinter(debug)
    base_end_X = vals[-1][idx_X]
    base_start_X = vals[0][idx_X]
    base_end_Y = vals[-1][idx_Y]
    base_start_Y = vals[0][idx_Y]
    dp.p(base_start_X, "baseline start X")
    dp.p(base_end_X, "baseline end X  ")
    dp.p(base_start_Y, "baseline start Y")
    dp.p(base_end_Y, "baseline end Y  ")
    return (base_start_Y + base_end_Y) * (base_end_X - base_start_X) / 2.


def min_min_baseline(vals, debug):
    dp = DebugPrinter(debug)
    n = len(vals)
    firstq_idx = int(n/4)
    firstq = vals[:firstq_idx]
    lastq_idx = int(3*n/4)
    lastq = vals[lastq_idx:]
    firstq_min_val = 1000000000.
    lastq_min_val = 1000000000.
    firstq_min_pos = 0.
    lastq_min_pos = 0.
    for kv in firstq:
        if kv[idx_Y] < firstq_min_val:
            firstq_min_val = kv[idx_Y]
            firstq_min_pos = kv[idx_X]
    for kv in lastq:
        if kv[idx_Y] < lastq_min_val:
            lastq_min_val = kv[idx_Y]
            lastq_min_pos = kv[idx_X]

    base_end_X = vals[-1][idx_X]
    base_start_X = vals[0][idx_X]

    baseline_a = (firstq_min_val - lastq_min_val)/(firstq_min_pos - lastq_min_pos)
    baseline_b = firstq_min_val - baseline_a * firstq_min_pos
    dp.p(baseline_a, "baseline incline")
    dp.p(baseline_b, "baseline intercept")
    base_end_Y = baseline_a * base_end_X + baseline_b
    base_start_Y = baseline_a * base_start_X + baseline_b
    dp.p(base_start_X, "baseline start X")
    dp.p(base_end_X, "baseline end X  ")
    dp.p(base_start_Y, "baseline start Y")
    dp.p(base_end_Y, "baseline end Y  ")
    return (base_start_Y + base_end_Y) * (base_end_X - base_start_X) / 2.


def get_float(num_str, euro=False):
    n = num_str.replace(",", ".") if euro else num_str
    return float(n)


class DebugPrinter:
    def __init__(self, debug):
        self.debug = debug

    def p(self, v, desc=""):
        if self.debug:
            if len(desc) == 0:
                print(v)
            else:
                print(desc + ": " + str(v))


if __name__ == "__main__":
    main(sys.argv[1:])
