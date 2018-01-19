__author__ = "kowalski"
import re
import numpy
import math
import subprocess
import warnings

LENGTH = 500

FPACL = "audio/fpcalc"

SPAN = 1200

STEP = 3


def calc_fp(input_file):
    chars = re.compile("[`!$^&*()=[\]{}\\\|;:'\",<>? ]")
    string_escaped = ""
    for char in input_file:
        if chars.search(char):
            string_escaped += '\\' + char
        else:
            string_escaped += char
    input_file = string_escaped

    fpcalc_out = subprocess.check_output(
        FPACL + " -raw -length " + str(LENGTH) + " " + input_file,
        stderr=subprocess.STDOUT, shell=True)
    fingerprint_index = fpcalc_out.find(b"FINGERPRINT=") + 12

    fingerprint = list(bytes(fpcalc_out[fingerprint_index:]).split(b','))
    return [int(x) for x in fingerprint]


def variance(lst):
    mean_x = numpy.mean(lst)
    mean_x_sqr = 0
    for x in lst:
        mean_x_sqr += x ** 2
    mean_x_sqr /= float(len(lst))
    return mean_x_sqr - mean_x ** 2


def cross_correlation(list_x, list_y, offset):

    if offset > 0:
        list_x = list_x[offset:]
        list_y = list_y[:len(list_x)]
    elif offset < 0:
        offset = -offset
        list_y = list_y[offset:]
        list_x = list_x[:len(list_y)]
    if len(list_x) != len(list_y):
        return -2

    mean_x = numpy.mean(list_x)
    mean_y = numpy.mean(list_y)

    covariance = 0
    for i in range(len(list_x)):
        covariance += (list_x[i] - mean_x) * (list_y[i] - mean_y)
    covariance /= float(len(list_x))

    return covariance / (math.sqrt(variance(list_x))
                         * math.sqrt(variance(list_y)))


def max_index(lst):
    maximum = 0
    max_value = lst[0]
    for i, value in enumerate(lst):
        if value > max_value:
            max_value = value
            maximum = i
    return maximum


def compare(first_fps, second_fps):
    warnings.simplefilter("ignore")
    try:
        corr_xy = []
        for offset in numpy.arange(-SPAN, SPAN + 1, STEP):
            corr_xy.append(cross_correlation(first_fps, second_fps, offset))
        corr_ab = corr_xy
    except ZeroDivisionError:
        return 0
    max_corr_index = max_index(corr_ab)
    return corr_ab[max_corr_index]
