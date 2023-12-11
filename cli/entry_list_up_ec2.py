#Get input from option -p and call the function inside list_up_ec2 script (same directory) to output the result
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
