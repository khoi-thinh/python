#!/usr/bin/python3
# The script searches and removes overly permissive rules such as 0.0.0.0/0 in all Security Groups

import boto3
client = boto3.client('ec2')

def remove_unsecure_group_rules():
    for sg in client.describe_security_groups()['SecurityGroups']:
        group_id = sg['GroupId']
      
        for rule in sg['IpPermissions']:
            protocol = rule.get('IpProtocol')
            
            if protocol == '-1':
                for ip_range in rule.get('IpRanges', []):
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        client.revoke_security_group_ingress(GroupId=group_id, CidrIp='0.0.0.0/0', IpProtocol=protocol)
                for ip_range in rule.get('IpRangesv6', []):
                    if ip_range.get('CidrIpv6') == '::/0':
                        client.revoke_security_group_ingress(GroupId=group_id, IpPermissions=[
                                                    {
                                                        'IpProtocol': '-1',
                                                        'Ipv6Ranges': [
                                                                {
                                                                    'CidrIpv6': '::/0'
                                                                }
                                                            ],
                                                    }
                                                ])
            else:            
                from_port = rule.get('FromPort')
                to_port = rule.get('ToPort')
                # Remove 0.0.0.0/0 ipv4
                for ip_range in rule.get('IpRanges', []):
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        client.revoke_security_group_ingress(GroupId=group_id, CidrIp='0.0.0.0/0', IpProtocol=protocol,FromPort=from_port,ToPort=to_port)
                      
                # Remove ::/0 ipv6        
                for ipv6_range in rule.get('Ipv6Ranges', []):
                    if ipv6_range.get('CidrIpv6') == '::/0':
                        client.revoke_security_group_ingress(GroupId=group_id, IpPermissions=[
                            {
                                'FromPort': from_port,
                                'IpProtocol': protocol,
                                'Ipv6Ranges': [
                                        {
                                            'CidrIpv6': '::/0'
                                        }
                                    ],
                                'ToPort': to_port   
                            }
                        ])
                   
remove_unsecure_group_rules()  
