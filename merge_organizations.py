#!/usr/bin/env python3
"""Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied."""
from meraki_functions import *
from env import *
import sys


#the SSIDs in Meraki come with default rules that do not need to be copied with the network - the default_rules variable is those rules
default_rules = [
    {
        'comment': 'Wireless clients accessing LAN',
        'destCidr': 'Local LAN',
        'destPort': 'Any',
        'ipVer': 'ipv4',
        'policy': 'deny',
        'protocol': 'Any'
    },
    {
        'comment': 'Default rule',
        'destCidr': 'Any',
        'destPort': 'Any',
        'ipVer': 'ipv4',
        'policy': 'allow',
        'protocol': 'Any'
    },
    {
        'comment': 'Wireless clients accessing LAN',
        'destCidr': 'Local LAN',
        'destPort': 'Any',
        'ipVer': 'ipv4',
        'policy': 'allow',
        'protocol': 'Any'
    }
]

src_org_id = getOrgID(base_url, headers, src_org_name)
if src_org_id is None:
    print("No organization found with name {}.".format(src_org_name))
    sys.exit(1)

dest_org_id = getOrgID(base_url, headers, dest_org_name)
if src_org_id is None:
    print("No organization found with that name {}.".format(dest_org_name))
    sys.exit(1)

networks = getOrgNetworks(base_url, headers, src_org_id)
if not networks:
    print("No networks exist in organization {}".format(src_org_name))
    sys.exit(1)

all_devices = [] #this list will hold all the device information for every AP in the src organization
old_networks = {} #this dictionary will map the src network ids to their names
new_networks = {} #this dictionary will map the dest network names to their ids, the dest network names will be the same as the src network names
networks_to_ssids = {} #map the new network ids to the SSIDs that it will have
network_ssids_to_firewalls = {} #map the new network ids to the SSID nums and their ssid firewall rules

'''we are getting the ssid information, network devices, and ssid firewall
information from the src organization and then creating new networks in the
dest organization that will have the same settings as the networks in the src
organization'''
for network in networks:
    ssids = getSSIDs(base_url, headers, network["id"])

    network_aps = getAccessPoints(base_url, headers, network["id"])

    old_networks[network["id"]] = network["name"]
    all_devices += network_aps

    new_network = createOrgNetwork(base_url, headers, dest_org_id, network)
    new_networks[new_network["name"]] = new_network["id"]
    networks_to_ssids[new_network["id"]] = ssids

    if ssids and isinstance(ssids, list):
        for ssid in ssids:
            firewall_rules = getWirelessSSIDFirewall(base_url, headers, network["id"], ssid["number"])
            rules = [rule for rule in firewall_rules["rules"] if rule not in default_rules] #we only want firewall rules that are different from the default_rules
            if rules: #there are firewall rules that are different from the default_rules
                if new_network["id"] in network_ssids_to_firewalls.keys(): #program has already added this network id to the dictionary, so we just have to add the ssid num and rules
                    network_ssids_to_firewalls[new_network["id"]][ssid["number"]] = {"rules": rules}
                else: #program has not yet added this network id to the dictionary, so we have to create a new key and assign it a dictionary with the ssid num and rules as its value
                    network_ssids_to_firewalls[new_network["id"]] = {
                        ssid["number"]: {"rules": rules}
                    }

'''edit the ssid settings of the new network with the ssid settings from the
source network'''
for network, ssids in networks_to_ssids.items():
    for ssid in ssids:
        if 'encryptionMode' in ssid.keys() and ssid['authMode'] != 'psk':
            del ssid['encryptionMode']

        if 'radiusFailoverPolicy' in ssid.keys() and ssid['radiusFailoverPolicy'] == None:
            del ssid['radiusFailoverPolicy']

        if 'radiusLoadBalancingPolicy' in ssid.keys() and ssid['radiusLoadBalancingPolicy'] == None:
            del ssid['radiusLoadBalancingPolicy']

        if need_radius and ssid["authMode"] == "8021x-radius":
            ssid_name = ssid["name"]
            ssid_servers = radius_servers[ssid_name]
            ssid["radiusServers"] = ssid_servers

        edit_ssid_status = editSSID(base_url, headers, network, ssid)
        if edit_ssid_status != 200:
            print("There was an issue editing the SSID {} of network {}".format(ssid["number"], network))
            sys.exit(1)

'''edit the firewall rules of the ssids in the new network with the firewall
rules from the source network'''
for network, ssid_firewalls in network_ssids_to_firewalls.items():
    for ssid, rules in ssid_firewalls.items():
        firewall_status = editWirelessSSIDFirewall(base_url, headers, network, ssid, rules)
        if firewall_status != 200:
            print("There was an issue editing the SSID firewall of the SSID {} of network {}".format(ssid["number"], network))
            sys.exit(1)

serials = [] #this list will have all the serial numbers of the devices removed from the source network

'''remove the device from the src organization network that it was in and then
add the serial number of the device to the list'''
for device in all_devices:
    remove_status = removeDeviceFromNetwork(base_url, headers, device["serial"], device["networkId"])
    if remove_status != 204:
        print("There was an issue removing the device {} from the network {}".format(device["serial"], device["networkId"]))
        sys.exit(1)

    print("Device {} removed from network {}".format(device["serial"], device["networkId"]))

    serials.append(device["serial"])

claim_status = claimDevicesToOrg(base_url, headers, dest_org_id, serials) #claim those devices that we removed from the src organization network to the dest organization
if claim_status != 200:
    print("There was an issue claiming the devices {} to the organization with ID {}".format(serials, dest_org_id))
    sys.exit(1)

print("Claimed the devices {} to the organization {}".format(serials, dest_org_id))

network_devices = {} #this dictionary will map the new network ids to the devices that should be added to that network

'''find which new networks the devices need to be claimed to based on the src
network they were previously assigned to'''
for device in all_devices:
    network_name = old_networks[device["networkId"]]
    new_net_id = new_networks[network_name]

    if new_net_id not in network_devices:
        network_devices[new_net_id] = [device["serial"]]
    else:
        network_devices[new_net_id].append(device["serial"])

'''assign the devices to the new networks that were created in the dest
organization according to the networks that were a part of in the src
organization'''
for net_id in network_devices:
    claim_status = claimDevicesToNetwork(base_url, headers, net_id, network_devices[net_id])
    if claim_status != 200:
        print("There was an issue claiming the devices {} to the network {}".format(network_devices[net_id], net_id))
        sys.exit(1)

    print("Claimed devices {} to the network {}".format(network_devices[net_id], net_id))
