# util labrary to work with portal, like:
# http://server.arcgis.com/en/portal/latest/administer/linux/example-transfer-item-ownership.htm

import urllib, json, ssl
from urllib2 import Request, urlopen

NOSSL  = True

def generateToken(username, password, portalUrl):
    """Retrieves a token to be used with API requests."""
    context = ssl._create_unverified_context() if NOSSL else None
    params = urllib.urlencode({'username' : username,
            'password' : password, 'client' : 'referer',
            'referer': portalUrl, 'expiration': 60, 'f' : 'json'})
    resp = urlopen(portalUrl + '/sharing/rest/generateToken?', params, context=context)
    jsonResponse = json.load(resp)
    if 'token' in jsonResponse:
        return jsonResponse['token']
    elif 'error' in jsonResponse:
        errMsg =  jsonResponse['error']['message']
        for detail in jsonResponse['error']['details']:
            errMsg += "\n"+ detail
        raise Exception( errMsg )

def getGroupContent( groupname, token, portalUrl):
    "Returns a list of all data for the specified group."
    context = ssl._create_unverified_context() if NOSSL else None
    groupID = getGroupID(groupname, token, portalUrl)
    if groupID:
       params =  urllib.urlencode({'token': token, 'f': 'json'})
       request = portalUrl + '/sharing/rest/content/groups/'+ groupID + '?'+ params
       userContent = json.load( urllib.urlopen(request, context=context) )
       return userContent
    else: 
       raise Exception("group with name: "+ groupname +" could not be found")

def getUserContent(username, folder, token, portalUrl):
    """Returns a list of all data for the specified user."""
    context = ssl._create_unverified_context() if NOSSL else None
    params =  urllib.urlencode({'token': token, 'f': 'json'})
    request = portalUrl + '/sharing/rest/content/users/' + username +'/'+ folder +'?'+ params
    userContent = json.load( urllib.urlopen(request, context=context) )
    return userContent

def getItemInfo(itemId, token, portalUrl):
    """Returns general information about the item."""
    context = ssl._create_unverified_context() if NOSSL else None
    params = urllib.urlencode({'token' : token,'f' : 'json'})
    request = portalUrl +'/sharing/rest/content/items/'+ itemId +'?'+ params
    itemInfo = json.load( urlopen(request, context=context) )
    return itemInfo

def additem(user, token, portalUrl, url, title, summary="", description="",
                  dtype="Map Service", tags="web", author="Stad Antwerpen", bbox="4.2482, 51.1470, 4.4976, 51.377"):
    """POST a new item to the portal:
        <PORTAL>/arcgis/portalhelp/apidocs/rest/index.html?groupsearch.html#/Add_Item/02t600000022000000/"""
    context = ssl._create_unverified_context() if NOSSL else None
    requestUrl = portalUrl +'/sharing/rest/content/users/'+ user +'/addItem'
    params = urllib.urlencode({
        'token' : token, 'f': 'json',
        'extent': ", ".join(bbox) if type(bbox) == list else bbox,
        'URL': url, 
        'title': title.encode('utf-8'),
        'snippet': summary[:250].encode('utf-8').strip(),
        'description': description.encode('utf-8').strip(),
        'type': dtype,
        'tags': tags.encode('utf-8').strip(),
        'accessInformation': author.encode('utf-8').strip(),
        "access": "public"
    }).encode()

    request = Request(requestUrl, params)
    item = json.load( urlopen(request, context=context) )
    return item

def updateItem(user, token, portalUrl, itemID, url=None, title=None, summary=None,
               description=None, tags=None, author=None, bbox=None):
    """modify a existing item:
       <PORTAL>/portalhelp/apidocs/rest/index.html?groupsearch.html#/Update_Item/02t60000000z000000/"""
    context = ssl._create_unverified_context() if NOSSL else None
    data = {'token' : token,'f' : 'json', "access": "public"}
    if url: data["URL"] = url
    if title: data["title"] = title.encode('utf-8').strip()
    if summary: data["snippet"] = summary[:250].encode('utf-8').strip(),
    if description: data["description"] = description.encode('utf-8').strip()
    if tags: data["tags"] = tags.encode('utf-8').strip()
    if author: data["accessInformation"] = author.encode('utf-8').strip()
    if bbox: data["extent"] = ", ".join(bbox) if type(bbox) == list else bbox

    requestUrl = portalUrl +'/sharing/rest/content/users/'+ user +'/items/' + itemID + "/update"
    request = Request(requestUrl, urllib.urlencode(data).encode())
    item = json.load( urlopen(request, context=context) )
    return item

def getGroupID(groupName, token, portalUrl):
    """Get the unique ID of a group by name"""
    context = ssl._create_unverified_context() if NOSSL else None
    params = urllib.urlencode({'token' : token, 'f' : 'json',
                                    'q': groupName.encode('utf-8').strip() }).encode()
    request = portalUrl +'/sharing/rest/community/groups' +'?'+ params
    query = json.load( urlopen(request, context=context) )

    if "results" in query.keys() and len( query["results"] ):
        return query["results"][0]["id"]


def shareItem(itemId, token, portalUrl, everyone=True, organistion=True, groups=[]):
    """share a item"""
    context = ssl._create_unverified_context() if NOSSL else None
    public = 'true' if everyone else 'false'
    org = 'true' if organistion else 'false'
    
    if len(groups) : 
       sgroups = ",".join(groups).encode('utf-8').strip()
       params = urllib.urlencode({'token' : token, 'f': 'json', 'org': org, 'everyone': public, 'groups': sgroups }).encode()
    else:
       params = urllib.urlencode({'token' : token, 'f': 'json', 'org': org, 'everyone': public }).encode()

    requestUrl = portalUrl +'/sharing/rest/content/items/'+ itemId + '/share'
    request = Request(requestUrl, params)
    item = json.load( urlopen(request, context=context) )
    return item

def deleteItem(itemId, token, portalUrl, userid):
    """delete a item"""
    context = ssl._create_unverified_context() if NOSSL else None
    params = urllib.urlencode({'token' : token, 'f' : 'json'}).encode()
    requestUrl = portalUrl +'/sharing/rest/content/users/' + userid + '/items/' + itemId + '/delete'
    response = urlopen(requestUrl, params, context=context)
    item = json.load( response )
    return item