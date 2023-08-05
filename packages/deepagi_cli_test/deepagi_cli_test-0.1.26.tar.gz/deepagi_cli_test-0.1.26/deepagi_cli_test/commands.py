#!/usr/bin/env python
import argparse
import sys
import os
import glob
from shutil import ignore_patterns, move, copy2, copystat, copyfile, copytree
import deepagi_cli_test

SUB_COMMANDS = [
    "initialize",
    "deploy"
]

def entry():
    def renameOptions():
    for grp in parser._action_groups:
        if grp.title == 'positional arguments':
            grp.title = 'Commands Available'
        if grp.title == 'optional arguments':
            grp.title = 'Other Commands'
            
    print('inside')
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    for cmd in SUB_COMMANDS:
        add_parser(cmd, subparsers)
    renameOptions()
    
    if len(sys.argv) > 1 :
        args = parser.parse_args(sys.argv[1:])
        try:
            args.func(args)
        except AttributeError:
            print("Too few arguments input, please view the help below")
            print('\nDEEPAGI CLI Available Commands\n')
            parser.print_help()
            print('\nRun deepagi-cli-test <command> -h to see more info about the specific command')
        
    else :

        print("Too few arguments input, please view the help below")
        print('\nDEEPAGI CLI Available Commands\n')
        
        parser.print_help()
        print('\nRun deepagi-cli-test <command> -h to see more info about the specific command')





def initialize(args):
    print("Initializing Project..")
    print("Project Name : %s" % args.projectname)
    if os.path.isdir(args.projectname) == False :
#         os.mkdir(args.projectname)
        copytree(os.path.join(os.path.dirname(deepagi_cli_test.__file__) , 'templates' ),os.path.join(os.getcwd(),args.projectname))
        os.chdir(args.projectname)
        
        for f in glob.glob("*.templates"):
            with open(f, "r") as inputfile:
                newText = inputfile.read().replace('projectname', args.projectname)
            os.remove(f)
            f = f.replace('.templates','')
            with open(f, "w") as outputfile:
                outputfile.write(newText)
        print('Enjoy with your new project!')
    else:
        print('Project already exists')


def deploy(args):
    print("Deploying the Project..")
    print("inputfile: %s" % args.projectname)
    print("outputfile: %s" % args.destination)


def add_parser(subcmd, subparsers):
    if subcmd == "initialize":
        parser = subparsers.add_parser("initialize", help='Initialize the project')
        parser.add_argument("projectname", metavar="projectname", help='The name of the project')
        parser.set_defaults(func=initialize)
    elif subcmd == "deploy":
        parser = subparsers.add_parser("deploy" , help='Deploy the project')
        parser.add_argument("projectname", metavar="projectname", help='The name of the project')
        parser.add_argument("destination", metavar="destination" , help='The destination server for deployment')
        

        parser.set_defaults(func=deploy)

