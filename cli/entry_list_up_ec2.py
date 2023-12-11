"""
Get input from option -p and call the function inside list_up_ec2 script (same directory) to output the result

Usage:
./entry_list_up_ec2.py -p windows
{'SuperWin': 'Windows'}

./entry_list_up_ec2.py -p Linux
{'aws-cloud9-terraform-1-3-e057eb8730054752bf43bc99d1ce88ac': 'Linux/UNIX', 'aws-cloud9-ide3-55bd06969e704acf9001b9cc25b5ebb7': 'Linux/UNIX', 'master-node': 'Linux/UNIX', 'node-01': 'Linux/UNIX'}

./entry_list_up_ec2.py -p
usage: entry_list_up_ec2.py [-h] [-p PLATFORM]
entry_list_up_ec2.py: error: argument -p/--platform: expected one argument

"""
#!/usr/bin/python3

import argparse
import list_up_ec2

platform_list = ['windows', 'linux']

def get_args():
    parser = argparse.ArgumentParser(description="List up all EC2 name based on input of OS platform",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-p','--platform',help="Platform name: windows or linux",default=None)
    
    args = parser.parse_args()
    
    return args
    
def main():
    args = get_args()
    platform = args.platform
    if platform is not None:
        platform = platform.lower()
        if platform in platform_list:
            print(list_up_ec2.list_ec2(platform))
        else:
            print("Please choose Linux or Windows")
    else:
        print("Please specify the option: -p or --platform")

if __name__ == '__main__':
    main()
