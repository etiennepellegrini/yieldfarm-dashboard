import argparse
import json
import jsonlines
import requests

import displayYield

# Go look here: https://www.dataquest.io/blog/python-api-tutorial/

def updateWallet(wallet, verbose):

    # GET all info from API
    address = wallet["address"]
    farms = requests.get(f'https://farm.army/api/v0/farms/{address}')
    balances = requests.get(
        f'https://farm.army/api/v0/balances/{address}'
    )

    # Create data dictionary
    data = {
        "wallet": wallet,
        "date": farms.headers["Date"],
        "farms": farms.json(),
        "balances": balances.json(),
    }

    # Write data as a new line
    with jsonlines.open(wallet["datafile"], "a") as writer:
        writer.write(data)

    # Display ROI
    if verbose:
        displayYield.displayYield(farms, verbose)


def loadConfig(args):
    configFile = args.config
    config = json.load(open(configFile, 'r'))
    config["wallets"] = json.load(open(config["wallet_list"]))
    config["verbose"] = args.verbose

    return config


def dataUpdate(config):
    for wallet in config["wallets"]:
        updateWallet(wallet, config["verbose"])


if __name__ == '__main__':
    # Create and populate argument parser
    parser = argparse.ArgumentParser(prog='dataUpdate')
    parser.add_argument('-c', '--config', type=str, nargs='?', help='Config'
                        ' json file. Default: "config.json"',
                        default='config.json')
    parser.add_argument('-v', '--verbose', type=int, nargs='?',
                        help='Different levels of debug output. Default: 0'
                        ' -1 for complete silence', default=0, const=1,
                        dest='verbose')

    # Read and convert input arguments
    args = parser.parse_args()
    config = loadConfig(args)
    dataUpdate(config)
