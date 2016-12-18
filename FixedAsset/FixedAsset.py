import urllib

import json
import sys
import time

#local import
from password import *


class FixedAssets():
    def __init__(self):
        #self.fixedBinUrl = "http://services.arcgis.com/Fv0Tvc98QEDvQyjL/arcgis/rest/services/liveBins_wgs84/FeatureServer"
        #self.fixedBinUrl = "http://services.arcgis.com/Fv0Tvc98QEDvQyjL/arcgis/rest/services/LiveCollectionData_WFL/FeatureServer"
        self.fixedBinUrl = "http://services.arcgis.com/Fv0Tvc98QEDvQyjL/arcgis/rest/services/LiveStreetbinCollectionData/FeatureServer"
        
        
        #This is a bad feature and needs to be fixed asap
        self.numberOfAssets = 715 #713 is the numer of bins currently serviced






    def generateToken(self):
        """ PNCC generateToken for accessing AGOL content """
        
        self.parameters = urllib.urlencode({'username' : username,
                            'password' : password,
                            'client' : 'referer',
                            'referer': portalUrl,
                            'expiration': 60,
                            'f' : 'json'})
        self.parameters = self.parameters.encode('utf-8')
        
        try:
            print "starting urllib"
            urllib.urlopen(portalUrl + '/sharing/rest/generateToken?', self.parameters)
            self.response = urllib.urlopen(portalUrl + '/sharing/rest/generateToken?', self.parameters)
        except Exception as e:
            print(e)
            print "stopping system"
            sys.exit(0)
        self.responseJSON = json.loads(self.response.read())
        #print responseJSON
        
        self.token = self.responseJSON.get('token')
        print "Token response complete"
        print self.token
        return self.token
    

    def returnAllObjectId(self):

        self.url = self.fixedBinUrl + '/0/query'

        payload = {"Where": "1=1",
                   "f": "json",
                   "returnIdsOnly": "True",
                   "token": self.token
                   }

        payloadEncoded = urllib.urlencode(payload)
        result = urllib.urlopen(self.url, payloadEncoded).read()
        queryReturn = json.loads(result)
        #print ("This is the payload update the collection to Today return:")
        #print queryReturn

        numberOfAssets = queryReturn['objectIds']
        print numberOfAssets
        return numberOfAssets
    

    def queryFixedAssetsXY(self):
        """ PNCC queryAGOL content """
        self.url = self.fixedBinUrl + '/0/query'
        
        #"outFields" : stops it from defaulting to random attributes
        self.payload = {"Where" : "1=1",
                        "f" : "json",
                        "returnGeometry":"True",
                        "outFields": "objectID"
                        }
                        
        self.payloadEncoded = urllib.urlencode(self.payload)
        self.result = urllib.urlopen(self.url, self.payloadEncoded).read()
        self.queryReturn =  json.loads(self.result)
        #return a list to iterate through
        #print self.queryReturn
        return self.queryReturn['features']
        
    
    def doneFixedAsset(self,closeOIDList):
        
        updateList = []
        try:
            #print closeOIDList[0]
            for f in closeOIDList:
                oidRef = f['attributes']['OBJECTID']
                feat = {"attributes" : {"OBJECTID" : oidRef,"Done": "Yes"}}
                updateList.append(feat)
            payload = {"f": "json", "features": updateList}    
            payloadEncoded = urllib.urlencode(payload)
            result = urllib.urlopen(self.fixedBinUrl + '/0/updateFeatures', payloadEncoded).read()
            queryReturn =  json.loads(result)
        except:
            print "nothing close by"
            pass
    
    def prepDay(self,dayInt):
        
        url = self.fixedBinUrl + '/0/query'
        days = ["Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"]
        
        #UPDATE DAYINT IF YOU WANT AN UPDATE FOR TODAYS DAY    format(days[(int(dayInt))+1]),
        # -1 sets this up for today
        payload = {"Where" : "{}Collect='Yes'".format(days[(int(dayInt))-1]),
                        "f": "json",
                        "returnIdsOnly": "True",
                        "token": self.token
                        }
        print ("calcualation are based on day {} +1").format(dayInt)

        payloadEncoded = urllib.urlencode(payload)
        result = urllib.urlopen(url, payloadEncoded).read()
        queryReturn =  json.loads(result)
        print ("This is the payload update the collection to Today return:")
        print queryReturn
        
        featList = queryReturn['objectIds']
        print featList
        
       
        updateList = []
        
        for f in featList:
            #print f
            feat = {"attributes" : {"OBJECTID" : f, "CollectToday": "Yes"}}
            updateList.append(feat)
        print ("we're updating todays to do list")
        print len(updateList)
        # print len(featList)
        
        payload = {"f": "json", "features": updateList, "token": self.token}    
        payloadEncoded = urllib.urlencode(payload)
        result = urllib.urlopen(self.fixedBinUrl + '/0/updateFeatures', payloadEncoded).read()
        queryReturn =  json.loads(result)
        print ("final return values:")
        print queryReturn
        

    def resetFixedAsset(self, numberOfAssets):
        """ method to reset everything to neutral before applying logic """
        self.numberOfAssets
        self.url = self.fixedBinUrl + '/0/updateFeatures'
        self.updateList = []
        
        for i in self.numberOfAssets:
            self.feat = {"attributes" : {"OBJECTID" : i,"Done": "No", "CollectToday": "No"}}
            self.updateList.append(self.feat)
        
        #{"f": "json", "features": } is added to get a json return 
        self.payload = {"f": "json", "features": self.updateList, "token": self.token}
        self.payloadEncoded = urllib.urlencode(self.payload)
        self.result = urllib.urlopen(self.url,self.payloadEncoded).read()
        self.queryReturn = json.loads(self.result)
        print self.queryReturn
