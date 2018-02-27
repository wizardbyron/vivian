#!/usr/bin/env python
import csv
import argparse
import time
import sys
from multiprocessing import Pool
from requests.exceptions import TooManyRedirects, ConnectionError
import requests


def load_csv(file_path):
    csv_reader = csv.reader(open(file_path, encoding='utf-8'))
    cases = []
    for row in csv_reader:
        cases.append(row)
    return cases


def verify_url(origin_url, expect_url, auth, line_num):
    print('verifying {0} to {1}'.format(origin_url, expect_url))
    no_fault = True
    is_redirect = False
    err_msg = ""
    status_code = 200
    redirect_count = 0
    is_match = True
    dist_url = ""
    try:
        if auth:
            username = auth['username']
            password = auth['password']
            response = requests.get(origin_url, auth=(username, password))
        else:
            response = requests.get(origin_url)
        is_redirect = len(response.history) > 0
        if is_redirect:
            last_url = response.history[-1].headers['Location']
            if auth:
                username = auth['username']
                password = auth['password']
                last_auth_response = requests.get(last_url, auth=(username, password))
                last_status_code = last_auth_response.status_code
            else:
                last_status_code = requests.get(last_url).status_code
        dist_url = response.history[-1].headers['Location'] if is_redirect else origin_url
        redirect_count = len(response.history)
        status_code = last_status_code if is_redirect else response.status_code
    except TooManyRedirects as err:
        no_fault = False
        err_msg = err
    except ConnectionError as err:
        no_fault = False
        err_msg = err
    return {
        'line':line_num,
        'status_code': status_code,
        'origin_url': origin_url,
        'expect_url': expect_url,
        'dist_url': dist_url,
        'redirect_count': redirect_count,
        'is_match': dist_url == expect_url,
        'is_pass': status_code in range(200, 400) and is_match and no_fault,
        'auth': auth,
        'err_msg': err_msg
    }


def multi_thread_verify(cases, auth, thread_num):
    pass_count = 0
    fail_count = 0
    failed_cases = []
    start_time = time.time()
    pool = Pool(processes=thread_num)
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
    print('Failed cases:')
    print('============================================================')
    for result in results:
        if result.get()['is_match']:
            pass_count += 1
        else:
            fail_count += 1
            failed_cases.append(result.get())
            print('  line: {0}'.format(result.get()['line']))
            print('origin: {0}'.format(result.get()['origin_url']))
            print('  dist: {0}'.format(result.get()['dist_url']))
            print('expect: {0}'.format(result.get()['expect_url']))
            print('status: {0}'.format(result.get()['status_code']))
            print('redirect_count:{0}'.format(result.get()['redirect_count']))
            print('------------------------------------------------------------')

    end_time = time.time()
    print("{0}/{1} PASS in {2} seconds".format(pass_count, len(cases), end_time-start_time))
    return 0 if fail_count > 0 else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth", help="basic auth in \"<username>:<password>\" format")
    parser.add_argument("-f", "--file", help="full path of .csv file")
    parser.add_argument("-n", "--number", type=int, help="thread number")
    args = parser.parse_args()
    print('load test case from {0}'.format(args.file))
    cases = load_csv(args.file)
    thread_num = args.number if args.number else len(cases)
    auth = {}
    if args.auth:
        auth = {
            'username': args.auth.split(':')[0],
            'password': args.auth.split(':')[1]
        }
    print("{0} cases loaded running in {1} threads".format(len(cases),thread_num))
    exit_value = multi_thread_verify(cases, auth, thread_num)
    sys.exit(exit_value)


if __name__ == '__main__':
    main()
