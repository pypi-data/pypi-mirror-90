import argparse
from main import *

default_instance_id = 'i-02e51d708e3e3b08b'
default_pem_file_path = "../AWS/PEM/fog_free.pem"
default_username = 'ec2-user'

def main():
    parser = argparse.ArgumentParser(prog='thundercloud', description='Run Python scripts on an EC2 instance!')
    parser.add_argument("-r", "--run", type=str, nargs=1, default=None, dest="run", required=True,
                        help="Runs a python file on the EC2 instance.")
    parser.add_argument("-i", "--instance", type=str, nargs=1, default=None, dest="instance",
                        help="Specifies the EC2 instance to be used.")
    
    args = parser.parse_args()

    if args.run:
        if args.instance:
            print("We currently don't provide support for other instances try again later!")
        else:
            print("Preparing to run your python script!")
            start_instance(default_instance_id)
            default_instance_ip = get_instance_ip(default_instance_id)
            client = start_ssh_session(default_pem_file_path, default_instance_ip, default_username)
            put_file(client, args.run[0], "test_program") # Will have to change this later
            output = command_stdout(client, "python test_program") # Will have to change this later
            print(output)
            stop_instance(default_instance_id)

if __name__ == "__main__": 
    # calling the main function 
    main() 
    



