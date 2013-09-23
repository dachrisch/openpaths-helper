#!/usr/bin/env python        

import json
from pprint import pprint
import sys, urllib2, oauth2, time, urllib

URL = "https://openpaths.cc/api/1" 

def build_auth_header(url, method, access, secret):
    params = {                                            
        'oauth_version': "1.0",
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': int(time.time()),
    }
    consumer = oauth2.Consumer(key=access, secret=secret)
    params['oauth_consumer_key'] = consumer.key 
    request = oauth2.Request(method=method, url=url, parameters=params)    
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    request.sign_request(signature_method, consumer, None)
    return request.to_header()

def get_params_from_commandline(arguments):

    if len(arguments) < 4:
        print 'usage: %s <location_history.json> <access> <secret>' % arguments[0]
        sys.exit(-1)

    return arguments[1:]

def format_numberE7(number):
    return float('%.6f' % (number / 1e7))

def transform_glatitude_to_openpaths(gdata):
    points = []
    for location in gdata['locations']:
        points.append({
            'lat' : format_numberE7(location['latitudeE7']),
            'lon' : format_numberE7(location['longitudeE7']),
            'alt' : 0.0,
            't' : int(location['timestampMs']) / 1e3,
            })
    return points

def upload_points_to_openpaths(points, access, secretc):
    success = 0
    failure = 0
    for point in points:
        try:
            request = urllib2.Request(URL)
            request.headers = build_auth_header(URL, 'POST', access, secret)
            param = {'points': json.dumps((point, ))}
            print('[%05d] uploading %s...' % (success + failure, param)),
            connection = urllib2.urlopen(request, urllib.urlencode(param))
            o_data = json.loads(''.join(connection.readlines()))
            success += 1
            print('OK %s' % str(o_data))
        except urllib2.HTTPError as e:
            failure += 1
            error_message = e.read()
            print error_message
            if '400: NOT AUTHORIZED' == error_message:
                raise e
    return (success, failure)

if __name__ == '__main__':
    (_file, access, secret) = get_params_from_commandline(sys.argv)
    print 'loading location data from [%s]...' % _file

    with open(_file) as data_file:
        data = json.load(data_file)


    points = transform_glatitude_to_openpaths(data)
    print '[%d] entries loaded.' % len(points)

    (success, failure) = upload_points_to_openpaths(points, access, secret)
    print 'done. (%d successfull, %d failed)' % (success, failure)
