import requests, getpass, simplejson, os.path
from os.path import expanduser

home = expanduser("~")
experimentalFunctions = ['networks']
nonexperimentalFunctions = ['servers']
rcfileName = '.ctl.io'

experimental = False

if experimental:
    apiVersion = 'v2-experimental'
else:
    apiVersion = 'v2'


apiUrlBase = 'https://api.ctl.io/'
apiUrl = apiUrlBase + apiVersion + '/'

def storeCreds(data):
    store_me = raw_input("Would you like me two Store Your Creds ? [y/n]")
    if store_me == 'y':
        # write file out
        rcfile = open(home + '/' + rcfileName, "w")
        rcfile.write(storage)
        rcfile.close()
        if os.path.isFile(home + '/' + rcfileName):
            print "Wrote Creds to File Successfully."
            return True
        else:
            print "Failed to Write Creds to File."
            return False

    else:
        print 'Will not store creds and will only use them for this session'
        return True

def login():
    username = raw_input("Username [%s]: " % getpass.getuser())
    if not username:
        username = getpass.getuser()

    password = getpass.getpass()

    body = {"username": username, "password": password}
    response = execApi('authentication/login',body)
    ## Store the Raw Response
    storage = response.text
    store = storeCreds(storage)
    if store:
        return storage
    else:
        raise SystemExit

def execApi(function, payload):
    options = {'content-type': 'application/json'}
    if function == 'authentication/login':
        response = requests.request("POST", apiUrl  + function, json=payload, headers=options)
    else:
        if httpMode == 'GET':
            response = requests.request("GET",apiUrl + function + '/' + account + '/' + datacenter, headers=options )
        elif httpMode == 'POST':
            response = requests.request("POST",apiUrl + function + '/' + account + '/' + datacenter, header=options )
    return response

def parseCreds(creds):
    data = simplejson.loads(creds)
    accountAlias = data["accountAlias"]
    bearerToken = data['bearerToken']
    return accountAlias, bearerToken



print "Welcome to CTL.io API CLI version 2"
print ""

if os.path.isfile(home + '/' + rcfileName):
    print "Using Stored Creds"
    data = open(home + '/' + rcfileName,'r')
    creds = data.read()
else:
    print "Creds wasn't stored, using interactive mode"
    creds = login()

accountAlias, bearerToken = parseCreds(creds)
