# GVE DevNet Meraki Organization Merger
This prototype uses the Meraki APIs to copy the networks and devices from one organization to another. Once the devices are added to the networks in the new organization, they will be removed from the old organization. The wireless network settings of the networks in the old organization are also copied into the networks of the new organization.

## Contacts
* Danielle Stacy

## Solution Components
* Python 3.9
* Meraki APIs

## Prerequisites
- **API Key**: In order to use the Meraki API, you need to enable the API for your organization first. After enabling API access, you can generate an API key. Follow these instructions to enable API access and generate an API key:
1. Login to the Meraki dashboard
2. In the left-hand menu, navigate to `Organization > Settings > Dashboard API access`
3. Click on `Enable access to the Cisco Meraki Dashboard API`
4. Go to `My Profile > API access`
5. Under API access, click on `Generate API key`
6. Save the API key in a safe place. The API key will only be shown once for security purposes, so it is very important to take note of the key then. In case you lose the key, then you have to revoke the key and a generate a new key. Moreover, there is a limit of only two API keys per profile.
> For more information on how to generate an API key, please click [here](https://developer.cisco.com/meraki/api-v1/#!authorization/authorization). 

- **Organization Names**: This prototype is about copying over networks and their devices from one organizaton to another. In order to accomplish this, you need the names of the source organization (the organization from which the networks and devices are coming) and the destination organization (the organization to which the networks and devices will be moved). To find the names of these organizations, follow these instructions:
1. Login to the Meraki dashboard
2. In the left-hand menu, select the Organization dropdown menu. It should be the first item in the menu.
3. All of the organzations should now be listed in the left-hand menu. To view a summary of the organizations, select the <b>MSP Portal</b> option.
4. Note the names of the source organization and the destination organization. You will need these names in the Installation portion of this prototype.
> For more information on MSP Portal, please visit [this article](https://documentation.meraki.com/General_Administration/Inventory_and_Devices/Monitoring_and_Managing_Multiple_Organizations)

## Installation/Configuration
1. Clone this repository with `git clone https://github.com/gve-sw/gve_devnet_meraki_organization_merger`
2. Add Meraki API key, source organization name, destination organization name, and radius server information (if necessary) to environment variables:
```python
base_url = "https://api.meraki.com/api/v1/"
API_KEY = "API key goes here"
src_org_name = "source organization name goes here"
dest_org_name = "destination organization name goes here"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Cisco-Meraki-API-Key": API_KEY
}

need_radius = False #if RADIUS servers are needed, change this to True
#The RADIUS servers are added by SSID, so the radius_servers data structure is a dictionary
#The key is the name of the SSID that you are adding the RADIUS servers to and the value of the key is the list of RADIUS servers that should be added to the SSID
#If more SSIDs need RADIUS servers, add more items to the dictionary. The key should be the name of the additional SSID and the value should be the RADIUS servers with the same formatting
#Add RADIUS server credentials here, to add more radius servers, add more elements to the array
#If one of the keys is not needed, delete that line
#If no RADIUS servers are needed, delete this information
radius_servers = {
    "ssid_name": [
        {
            "openRoamingCertificateId": "id of the Openroaming Certificate attached to radius server",
            "port": "udp port the RADIUS server listens on for Access-requests",
            "caCertificate": "certificate used for authorization for the RADSEC Server",
            "host": "ip address of your RADIUS server",
            "secret": "RADIUS client shared secret",
            "radsecEnabled": False #Boolean value, change as needed
        }
    ]
}
```
3. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
4. Install the requirements with `pip3 install -r requirements.txt`

## Usage
The functions that this program uses are located in meraki_functions.py, and the source code is found in merge_organizations.py

To run the program, use the command:
```
$ python3 merge_organizations.py
```


# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

Source Organization before running the program
![/IMAGES/src_org_before.png](/IMAGES/src_org_before.png)

Source Organization Calgary Network SSIDs before running the program
![/IMAGES/src_org_ssids_before.png](/IMAGES/src_org_ssids_before.png)

Source Organization Calgary Network SSID Firewall before running the program
![/IMAGES/src_org_ssid_fw_before.png](/IMAGES/src_org_ssid_fw_before.png)

Destination Organization before running the program
![/IMAGES/dest_org_before.png](/IMAGES/dest_org_before.png)

Output from running the program
![/IMAGES/output.png](/IMAGES/output.png)

Source Organization after running the program
![/IMAGES/src_org_after.png](/IMAGES/src_org_after.png)

Destination Organization after running the program
![/IMAGES/dest_org_after.png](/IMAGES/dest_org_after.png)

Destination Organization Calgary Network SSIDs after running the program
![/IMAGES/dest_org_ssids_after.png](/IMAGES/dest_org_ssids_after.png)

Destination Organization Calgary Network SSID Firewall after running the program
![/IMAGES/dest_org_ssid_fw_after.png](/IMAGES/dest_org_ssid_fw_after.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
