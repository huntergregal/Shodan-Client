#/usr/bin/python
import shodan
import argparse
import sys

#Define Shodan variables
SHODAN_API_KEY = "API_KEY"
api = shodan.Shodan(SHODAN_API_KEY)

#Define argument options
parser = argparse.ArgumentParser(description="An API client for the Shodan framework.")
parser.add_argument('-k', '--keyword', nargs=1, default=False, help='a keyword to search')
parser.add_argument('-t', '--target', nargs=1, default=False, help='a target ip address to search')

parser.add_argument('-v', '--verbose', action='store_true', help='show more information')
args = parser.parse_args()
def keywordSearch(keyword):
    try:
        #Search Shodan
        results = api.search(keyword)

        #Show results
        print 'Results found: %s' % results['total']
        for result in results['matches']:
            print 'IP: %s' % result['ip_str']
            if args.verbose:
                print 'Hostname: %s' % result['hostnames']
                print 'OS: %s' % result['os']
                print 'Port: %s' % result['port']
                print 'Timestamp: %s' % result['timestamp']
            print result['data']
            print '----------'
        print "\n[+]Keyword search complete"
    except shodan.APIError, e:
        print 'Error: %s' % e

def targetSearch(target):
    try:
        #Lookup the target
        host = api.host(target)
        #Show results
        print """
            IP: %s
            Organization: %s
            Operating System: %s
        """ % (host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a'))
        if args.verbose:
            #Print all banners
            print """
                Port: %s
                Banner: %s
            """ % (item['port'], item['data'])

        print "\n[+]Target lookup complete"
    except shodan.APIError, e:
        print 'Error: %s' % e
if __name__ == "__main__":
    if args.keyword and args.target:
        print "Cannot search both a keyword and a target!"
        sys.exit()
    if args.keyword:
        #keyword funtion
        keywordSearch(args.keyword)
    if args.target:
        #target function
        targetSearch(args.target)
