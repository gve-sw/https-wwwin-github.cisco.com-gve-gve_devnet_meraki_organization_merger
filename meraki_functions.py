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
import requests
import json


def getOrgID(base_url, headers, org_name):
    orgs_endpoint = "organizations"
    response = json.loads(requests.get(base_url+orgs_endpoint, headers=headers).text)

    for org in response:
        if org["name"] == org_name:
            return org["id"]

    return None


def getOrgNetworks(base_url, headers, org_id):
    org_nets_endpoint = "organizations/{}/networks".format(org_id)
    response = requests.get(base_url+org_nets_endpoint, headers=headers)

    all_networks = json.loads(response.text)
    networks = []
    for net in all_networks:
        networks.append(net)

    return networks


def getAccessPoints(base_url, headers, net_id):
    net_devices_endpoint = "networks/{}/devices".format(net_id)
    response = requests.get(base_url+net_devices_endpoint, headers=headers)

    net_devices = json.loads(response.text)
    access_points = []

    for device in net_devices:
        if 'MR' in device['model']:
            access_points.append(device)

    return access_points


def removeDeviceFromNetwork(base_url, headers, serial, net_id):
    remove_device_endpoint = "networks/{}/devices/remove".format(net_id)
    body = {"serial": serial}
    response = requests.post(base_url+remove_device_endpoint, headers=headers, data=json.dumps(body))

    return response.status_code


def createOrgNetwork(base_url, headers, org_id, network):
    org_nets_endpoint = "organizations/{}/networks".format(org_id)
    body = {
        "name": network["name"],
        "timeZone": network["timeZone"],
        "tags": network["tags"],
        "notes": network["notes"],
        "productTypes": network["productTypes"]
        }
    response = requests.post(base_url+org_nets_endpoint, headers=headers, data=json.dumps(body))

    new_network = json.loads(response.text)

    return new_network


def claimDevicesToOrg(base_url, headers, org_id, devices):
    org_claim_endpoint = "organizations/{}/claim".format(org_id)
    body = {"serials": devices}
    response = requests.post(base_url+org_claim_endpoint, headers=headers, data=json.dumps(body))

    return response.status_code


def claimDevicesToNetwork(base_url, headers, net_id, devices):
    net_claim_endpoint = "networks/{}/devices/claim".format(net_id)
    body = {"serials": devices}
    response = requests.post(base_url+net_claim_endpoint, headers=headers, data=json.dumps(body))

    return response.status_code


def getSSIDs(base_url, headers, net_id):
    ssids_endpoint = "networks/{}/wireless/ssids".format(net_id)
    response = requests.get(base_url+ssids_endpoint, headers=headers)

    ssids = json.loads(response.text)

    return ssids


def editSSID(base_url, headers, net_id, ssid):
    ssid_endpoint = "networks/{}/wireless/ssids/{}".format(net_id, ssid["number"])

    response = requests.put(base_url+ssid_endpoint, headers=headers, data=json.dumps(ssid))

    return response.status_code


def getGroupPolicies(base_url, headers, net_id):
    group_policy_endpoint = "networks/{}/groupPolicies".format(net_id)

    response = requests.get(base_url+group_policy_endpoint, headers=headers)

    group_policies = json.loads(response.text)

    return group_policies


def getWirelessSSIDFirewall(base_url, headers, net_id, ssid_num):
    ssid_firewall_endpoint = "networks/{}/wireless/ssids/{}/firewall/l3FirewallRules".format(net_id, ssid_num)

    response = requests.get(base_url+ssid_firewall_endpoint, headers=headers)

    ssid_firewall = json.loads(response.text)

    return ssid_firewall


def editWirelessSSIDFirewall(base_url, headers, net_id, ssid_num, rules):
    ssid_firewall_endpoint = "networks/{}/wireless/ssids/{}/firewall/l3FirewallRules".format(net_id, ssid_num)

    response = requests.put(base_url+ssid_firewall_endpoint, headers=headers, data=json.dumps(rules))

    return response.status_code
