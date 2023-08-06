# main.py

import argparse

def main():

    parser = argparse.ArgumentParser(prog='SsyiWorking', usage='This is a demo, please follow SsyiWorking on wechat')

    parser.add_argument("name", default='SsyiWorking', help="This is a demo framework", action="store")

    args = parser.parse_args()

    if args.name:

        print("Hello, My name is Ssyi, Please search and follow below account from wechat:\n")

        print(args.name)

if __name__ == "__main__":

    main()
