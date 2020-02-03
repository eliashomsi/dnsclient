#!/usr/bin/python3.8
import argparse
from dns_client import DNSClient
import sys, os
from contextlib import contextmanager

def __main__():
    results = dict()
    try:
        results = parseArgs()
    except BaseException as e:
        print(f"ERROR\tIncorrect input syntax: Please check arguments and try again")
        return

    try:
        results.address = results.address[1:]
        client = DNSClient(results)
        client.makeRequest()
    except BaseException as e:
        print(e)

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store', dest='timeout', help='Timeout value', type=int, default=5)
    parser.add_argument('-r', action='store', dest='maxRetries', help='max retries', type=int, default=3)
    parser.add_argument('-p', action='store', dest='port', help='port number to make request', type=int, default=53)

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-mx', action="store_true", default=False, dest='mx', help="MX query type")
    group.add_argument('-ns', action="store_true", default=False, dest='ns', help="NS query type")

    parser.add_argument(action="store", dest="address", help="name to resolve")
    parser.add_argument(action="store", dest="name", help="name to resolve")

    args = dict()
    with redirect_stdout_stderr(os.devnull):
        args = parser.parse_args()
    return args

@contextmanager
def redirect_stdout_stderr(stream):
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = stream
    sys.stderr = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

if __name__ == "__main__":
    __main__()