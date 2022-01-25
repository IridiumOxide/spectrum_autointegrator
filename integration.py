import logging
import csv

idx_X = 0
idx_Y = 1


log = logging.getLogger("integration")


class Integrator:
    def __init__(self, separator, euro, nobase):
        self.separator = separator
        self.euro = euro
        self.nobase = nobase

    def integral_from_file(self, file, start, end):
        return integral_from_file(file, start, end, self.separator, self.euro, self.nobase)


def integral_from_file(file, start, end, separator, euro, nobase):
    with open(file) as f:
        reader = csv.reader(f, delimiter=separator)
        vals = [[get_float(x[idx_X], euro), get_float(x[idx_Y], euro)] for x in reader if end >= get_float(x[idx_X], euro) >= start]
        log.debug("vals               : %s", vals)
        log.debug("total vals         : %s", len(vals))
        if len(vals) == 0:
            return 0
        else:
            s = trapeze_integral(vals)
            base = min_min_baseline(vals)
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


def start_end_baseline(vals):
    base_end_X = vals[-1][idx_X]
    base_start_X = vals[0][idx_X]
    base_end_Y = vals[-1][idx_Y]
    base_start_Y = vals[0][idx_Y]
    log.debug("baseline start X   : %s", base_start_X)
    log.debug("baseline end X     : %s", base_end_X)
    log.debug("baseline start Y   : %s", base_start_Y)
    log.debug("baseline end Y     : %s", base_end_Y)
    return (base_start_Y + base_end_Y) * (base_end_X - base_start_X) / 2.


def min_min_baseline(vals):
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
    log.debug("baseline incline   : %s", baseline_a)
    log.debug("baseline intercept : %s", baseline_b)
    base_end_Y = baseline_a * base_end_X + baseline_b
    base_start_Y = baseline_a * base_start_X + baseline_b
    log.debug("baseline start X   : %s", base_start_X)
    log.debug("baseline end X     : %s", base_end_X)
    log.debug("baseline start Y   : %s", base_start_Y)
    log.debug("baseline end Y     : %s", base_end_Y)
    return (base_start_Y + base_end_Y) * (base_end_X - base_start_X) / 2.


def get_float(num_str, euro=False):
    n = num_str.replace(",", ".") if euro else num_str
    return float(n)
