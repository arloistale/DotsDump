#!/user/bin/python

from bs4 import BeautifulSoup, SoupStrainer

from collections import OrderedDict

import os, sys, argparse, urlparse
import csv

def validate_hash(hash):
    return len(hash) == 16

def grab_hash(url):
    query = urlparse.urlparse(url)

    hash = query.path.split('/')[4]

    if not validate_hash(hash):
        print 'Problem Hash: ', url
   
    return hash

def crunch(url, result):
    soup = BeautifulSoup(open(url), parse_only=SoupStrainer('a'))
    href = ''

    for link in soup:
        if not link.has_attr('href'):
            continue

        href = link['href']

        # avoid garbage links
        if href != '#' and href != 'javascript:;':
            result.add(grab_hash(href))

def write_result_to_csv(result):
    with open('result.csv', 'wb') as f:
        wr = csv.writer(f)
        
        for hash in result:
            wr.writerow([hash])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs='+')
    args = parser.parse_args()

    result = set()

    for url in args.url:
        crunch(url, result)

    write_result_to_csv(result)

    print 'Results written to result.csv'
    

if __name__ == "__main__":
    main()
