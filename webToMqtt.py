#!/usr/bin/env python3
from bottle import route, run, get, post, request
import os.path
import pickle
import paho.mqtt.publish as publish
arr = []
redirectList = {
    "broker":"port",
    "port":"protocol",
    "protocol":"username",
    "username":"password",
    "password":"topic",
    "topic":"cp_01"
}
customPages = {
    "cp_01": '<a href = "/listall">Done (View Configs)</a> </br> <a href = "/">Home</a>'
}
@route('/prompt/<ids>/<thing>')
def prompt(ids,thing):
    form = ""
    if thing in redirectList:
        form  += '<form action="/upload" autocomplete="off" method="post">' + thing + ': <input name="val"/><div style="visibility:hidden;">ID: <input name="id" value="'+ids+'"/>thing: <input name="thing" value="'+thing+'"/></div><input value="Submit" type="submit"/></form>'

    else:
        form = customPages[thing]
    return form
    
@route('/upload', method='POST')
def do_login():
    val = request.forms.get('val')
    thing = request.forms.get('thing')
    sysid = int(request.forms.get('id'))
    arr[sysid][thing]=val
    pickle.dump(arr, open( "save.p", "wb" ))
    return '<script>window.location.href = "/prompt/'+str(sysid)+'/'+redirectList[thing]+'"</script>'

@route('/')
def main(): 
    val = '''Welcome to my site. This is a simple service that recieves rest requests, and forwards them over mqtt.</br>
            It is great for integrating with IFTTT, or anything else which has no direct way of reaching your device without port forwarding or fancy networking.</br> 
            Note that while passwords are not displayed in the site, they are stored in plaintext on my server.</br>
            There are no access controls, very little validation and several other bad practices. Please beware. <br>
            How to use:
            <ol>
                <li>Go to <a href="/new">new</a> and enter the following:</li>
                <ul>
                    <li>Broker - The domain name. No ports or protocols</li>
                    <li>Port - This is typically 1883 for mqtt</li>
                    <li>Protocol - By this I mean transport. tcp or websockets. Probably tcp if you don't know. </li>
                    <li>Username - Setting the username to x-noauth will disable mqtt authorization in theory</li>
                    <li>Password</li>
                    <li>Topic - When the service recieves a request, which topic to post it to. Only supports one</li>
                </ul>
                <li>Visit <a href = "http://machine.clarkbains.com:3142/api/{your_id}">http://machine.clarkbains.com:3142/api/{your_id}</a> and substitute in your id you got from the first page</li>
                <li>Check your mqtt topic. (If you POST, it will send the post body, otherwise it will send a generic message)</li>
                <li>Configure your service to post to the url you just found</li>
                <li>Subscribe to the mqtt topic on your devices.</li>
            </ol>
            You may visit <a href="/listall">here</a> to get the id or edit a config
            '''
    return val
@route('/new')
def new(): 
    ret = 'Creating New Service. ID is %s. Click <a href = "/prompt/%s/broker">here</a> to specify broker to send to.' %(str(len(arr)), str(len(arr)))
    arr.append({"sysid":str(len(arr))})
    return ret
@route('/listall')
def listall():
    retval = "Brokers:<br>"
    for i in arr:
        print (i)
        if "sysid" in i and "broker" in i and "topic" in i:
            retval+= ("id: "+i["sysid"] + ", broker: " + i["broker"] + ", publish topic: " + i["topic"] + ' <a href = "/prompt/'+i["sysid"]+'/broker" >Edit</a>'+"<br>")
    return retval
@route('/save')
def save():
    pickle.dump(arr, open( "save.p", "wb" ))
    return "Saved"
@route('/dump')
def dump():
    return str(arr)
@route('/load')
def load():
    global arr
    arr = pickle.load( open( "save.p", "rb" ))
    return "Loaded"
@route('/print')
def printArr():
    print(arr)
    return "Printed"
@route('/cls')
def cls():
    global arr
    #arr = []
    return "Cleared"

@route("/api/<url:re:\d*>")
def apiGet(url):
    if (int(url)>=len(arr) or int(url)<0):
        return "Bad Number"
    client = arr[int(url)]
    cred = {"username":client["username"],"password":client["password"]}
    if client["username"] == "x-noauth":
        cred=None
    publish.single(client["topic"],"Post Data Goes Here",hostname=client["broker"],port=int(client["port"]),transport=client["protocol"],auth=cred)
    return "run_event"

@route("/api/<url:re:\d*>", method='POST')
def api(url):
    if (int(url)>=len(arr) or int(url)<0):
        return "Bad Number"
    body = request.body.getvalue().decode('utf-8')
    client = arr[int(url)]
    cred = {"username":client["username"],"password":client["password"]}
    publish.single(client["topic"],body,hostname=client["broker"],port=client["port"],transport=client["protocol"],auth=cred)
    return "run_event"

if not os.path.exists(r'./save.p'):
    arr = [{}]
    pickle.dump(arr, open( "save.p", "wb" ))
else:
    arr = pickle.load( open( "save.p", "rb" ))
run(host='0.0.0.0', port=3142)