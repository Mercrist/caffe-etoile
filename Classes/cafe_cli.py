#!/usr/bin/python3
from argparse import ArgumentParser


description = "CLI tool used to interact with Caffè Étoilé."

def generate_parser():
    parser = ArgumentParser(description) 
    parser.add_argument("action", help="Main action to take.",choices=["menu","reservation","about"])

    
    return parser


if __name__ == "__main__":
    parser = generate_parser() 
    args = parser.parse_args() 

