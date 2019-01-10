#!/usr/bin/env python
import csv
import argparse
import time
import sys
from multiprocessing import Pool
from requests.exceptions import TooManyRedirects, ConnectionError
import requests
import urllib


def load_csv(file_path):
    csv_reader = csv.reader(open(file_path))
    cases = []
    for row in csv_reader:
        cases.append(row)
    return cases


def request(url, auth):
    if auth:
        username = auth['username']
        password = auth['password']
        response = requests.get(url, auth=(username, password))
    else:
        response = requests.get(url)
    return response


def is_ok_status(status_code):
    return status_code in range(200, 400)


def verify_url(origin_url, expect_url, auth, line_num):
    no_fault = True
    err_msg = ""
    status_code = ""
    redirect_count = 0
    actual_url = origin_url
    try:
        response = request(origin_url, auth)
        status_code = response.status_code
        redirect_count = len(response.history)
        if redirect_count > 0:
            actual_url = response.history[-1].headers['Location']
            status_code = request(actual_url, auth).status_code
    except TooManyRedirects as err:
        no_fault = False
        err_msg = err
    except ConnectionError as err:
        no_fault = False
        err_msg = err

    is_match = urllib.unquote(actual_url) == expect_url
    return {
        'line': line_num,
        'status_code': status_code,
        'origin_url': origin_url,
        'expect_url': expect_url,
        'actual_url': actual_url,
        'redirect_count': redirect_count,
        'is_match': is_match,
        'is_pass': (is_ok_status(status_code) and is_match and no_fault),
        'auth': auth,
        'err_msg': err_msg
    }


def running_in_pool(cases, auth, process_num):
    pool = Pool(processes=process_num)
    results = []
    line_num = 0
    for case in cases:
        line_num += 1
        origin = case[0].strip()
        expect = case[1].strip()
        result = pool.apply_async(verify_url, args=(origin, expect, auth, line_num))
        results.append(result)
    pool.close()
    pool.join()
    return results


def multi_process_verify(cases, auth, process_num):
    start_time = time.time()
    results = running_in_pool(cases, auth, process_num)
    end_time = time.time()
    case_count = len(cases)
    pass_count = len(filter(lambda r: r.get()['is_pass'], results))
    fail_count = case_count - pass_count
    print_cases_message(results, case_count, pass_count, end_time - start_time)
    return 1 if fail_count > 0 else 0


def print_cases_message(results, case_count, pass_count, time_cost):
    for result in results:
        status_code = result.get()['status_code']
        if is_ok_status(status_code):
            format_status = format_passed_message(status_code)
        else:
            format_status = format_failed_message(status_code)

        if result.get()['is_pass']:
            format_passed = format_passed_message('YES')
        else:
            format_passed = format_failed_message('NO')

        print('------------------------------------------------------------')
        print('          line: {0}'.format(result.get()['line']))
        print('        origin: {0}'.format(result.get()['origin_url']))
        print('        expect: {0}'.format(result.get()['expect_url']))
        print('        actual: {0}'.format(result.get()['actual_url']))
        print(' response code: {0}'.format(format_status))
        print('        passed: {0}'.format(format_passed))
        print('redirect count: {0}'.format(result.get()['redirect_count']))
        print('------------------------------------------------------------')
    print("{0}/{1} PASS in {2} seconds".format(pass_count, case_count, time_cost))


def format_failed_message(message):
    return '\033[0;31m{0}\033[0m'.format(message)


def format_passed_message(message):
    return '\033[0;32m{0}\033[0m'.format(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", help="basic auth in \"<username>:<password>\" format")
    parser.add_argument("-f", "--file", help="full path of .csv file")
    parser.add_argument("-n", "--number", type=int, help="process number")
    parser.add_argument("-v", "--version", action='version', version='%(prog)s 0.0.1dev3')
    args = parser.parse_args()
    print('load test case from {0}'.format(args.file))
    cases = load_csv(args.file)
    process_num = args.number if args.number else len(cases)
    auth = {}
    if args.auth:
        auth = {
            'username': args.auth.split(':')[0],
            'password': args.auth.split(':')[1]
        }
    print("{0} cases loaded running in {1} process".format(len(cases), round(process_num, 4)))
    exit_value = multi_process_verify(cases, auth, process_num)
    sys.exit(exit_value)


if __name__ == '__main__':
    main()
