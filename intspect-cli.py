import os
import argparse
import sys
import json
import logging

import integration


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

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if debug:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)

    integrator = integration.Integrator(csv_separator, euro, nobase)

    if os.path.isdir(path_name):
        for file in [f for f in os.listdir(path_name) if os.path.isfile(os.path.join(path_name, f))]:
            fullpath = os.path.join(path_name, file)
            results[fullpath] = integrator.integral_from_file(fullpath, start, end)
    else:
        results[path_name] = integrator.integral_from_file(path_name, start, end)

    if print_csv:
        for k in results:
            print(f'{k},{results[k]}')
    else:
        print(json.dumps(results))
    return results


if __name__ == "__main__":
    main(sys.argv[1:])
