

from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
from zeep.cache import SqliteCache
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#Download CUCM AXL Toolkit (Application -> Plugin Menu) on local system and replace wsdl file path with below  
WSDL_URL = 'C:/Users/ipcafe/Downloads/axlsqltoolkit/schema/12.5/AXLAPI.wsdl'

#Replace CUCM IP Address,AXL Username and password in below variables 
CUCM_URL = 'https://192.168.1.1:8443/axl/'

USERNAME = 'axl'
PASSWD = 'password'


session = Session()
session.verify = False
session.auth = HTTPBasicAuth(USERNAME, PASSWD)

transport = Transport(session=session, timeout='none', cache=SqliteCache())

client = Client(WSDL_URL, transport=transport)
service=client
service = client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding", CUCM_URL)


firstName=input("Enter User's Firstname Name:\n").capitalize()
lastName=input("Enter Users's Last Name:\n").capitalize()
userId=input("Enter User ID:\n")
extension=input("extension:\n")

if(len(lastName) > 11):
    deviceName=firstName[0]+lastName[:11]
else:
     deviceName=firstName[0]+lastName

deviceName='CSF'+deviceName

phone_data = {   'name': deviceName,
				'description': lastName+" "+ firstName+ " (" +extension+ ")",
                'product':'Cisco Unified Client Services Framework',
                'class':'Phone',
                'protocol':'SIP',
                'protocolSide':'User',                
                'devicePoolName': {                
                #replace currect Device Pool with below value
                '_value_1': 'MainOffice'               
				},
                #replace currect media resource group Name with below value
				'mediaResourceListName': {                
                '_value_1': 'media'
				},
				'networkHoldMohAudioSourceId': '1',
				'userHoldMohAudioSourceId': '1',
                #replace currect security profile with below value
				'securityProfileName': {
                '_value_1': 'Cisco Unified Client Services Framework - Standard SIP Non-Secure Profile'
				},
				#replace currect SIP profile with below value
				'sipProfileName': {
 					'_value_1': 'Presence'
				},                
                'ownerUserName':userId,
                 #replace currect common phone config with below value
                'commonPhoneConfigName':'Standard Common Phone Profile',
                'locationName':'Hub_None',
                'useTrustedRelayPoint':'Default',
                'builtInBridgeStatus':'On',
                'packetCaptureMode':'None',
                'certificateOperation':'No Pending Operation',
                'deviceMobilityMode':'Default',
                'lines': {
                'line': [
                    {
                        'index': 1,
                        'label': lastName+' '+ firstName,
                        'display': firstName[0]+'.' +lastName,
                        'dirn': {
                            'pattern': extension,
							 #replace currect partition with below value
                            'routePartitionName': {
                                '_value_1': 'PT-Staff'
                            },                           
                        },                        
                        'ringSetting': 'Ring',
                        'consecutiveRingSetting': 'Use System Default',
                        'ringSettingIdlePickupAlert': None,
                        'ringSettingActivePickupAlert': None,
                        'displayAscii': userId,
                        'e164Mask': None,
                        'dialPlanWizardId': None,
                        'mwlPolicy': 'Use System Policy',
                        'maxNumCalls': 3,
                        'busyTrigger': 1,
                        'callInfoDisplay': {
                            'callerName': 'true',
                            'callerNumber': 'false',
                            'redirectedNumber': 'false',
                            'dialedNumber': 'true'
                        },
                        #replace currect recording profile with below value
                        'recordingProfileName': {
                            '_value_1': 'recroding1'
                        },
                        'monitoringCssName': {
                            '_value_1': None
                        },
                        'recordingFlag': 'Automatic Call Recording Enabled',
                        'recordingMediaSource': 'Phone Preferred',
                        'audibleMwi': 'Default',
                        'speedDial': None,
                        'partitionUsage': 'General',
                        'associatedEndusers': {
                            'enduser': [
                                {
                                    'userId': userId
                                }
                            ]
                        },
                        'missedCallLogging': 'true',
                        'recordingMediaSource': 'Phone Preferred',
                        'ctiid': None,                   
                    }
                ],
                'lineIdentifier': None
                },			
                'phoneTemplateName': {
                '_value_1': 'Standard Client Services Framework'
				},				 
				'presenceGroupName': {
                '_value_1': 'Standard Presence group'
				}			
                   
            }          


line_data={
                'pattern': extension,
                 #replace currect partition with below value
                'routePartitionName':'PT-staff',
                'usage': 'Device',
                'description': firstName+' ' +lastName,
                'alertingName':firstName[0]+' ' + lastName,
                'asciiAlertingName':firstName[0]+' '+lastName,
                #replace currect calling search space with below value
                'shareLineAppearanceCssName':'CSS-Staff'
                
            }


try:
    service.addLine(line_data)
except: 
    print("line Exists,Creating phone...")


try:
    service.addPhone(phone_data)
except:
    print("Error creating phone") 
    sys.exit(0)
else:
    print("Phone creation successfull...")
    


try:
    service.updateUser(userid = userId,                      
				associatedDevices= {
                'device': deviceName,                 
				},
				primaryExtension= {
                    'pattern': extension,
                     #replace currect partition with below value
                    'routePartitionName': 'PT-Staff'
              },                
                homeCluster= 'true',
                imAndPresenceEnable= 'true',
                #replace currect service profile with below value
                serviceProfile=  'Profile-Jabber',              
                ipccExtension= extension) 
except:
    print("Error associating phone to user")  
else:
    print("Phone associated to user successfuly")


