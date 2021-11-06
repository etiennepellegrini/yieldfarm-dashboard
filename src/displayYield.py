import argparse
import json
import requests


def displayYield(apiResponse, wallet=None, verbose=1):
    deps = []
    rews = []
    resp = apiResponse.json()
    for platform in resp["platforms"]:
        if verbose > 1:
            for farm in platform["farms"]:
                deps.append(farm["deposit"]["usd"])
                rews.append(sum([x.get("usd", 0.0) for x in farm.get("rewards", [{}])]))
                perc = float(rews[-1]/deps[-1])*100.0
                if verbose > 1:
                    print(f'Farm: {farm["farm"]["id"]:35} ({farm["deposit"].get("symbol", "no-symbol"):10}): deposits: {deps[-1]:12.6f} USD, reward: {rews[-1]:12.6f} USD, ({perc:6.4f} %)')
        else:
            deps.append(platform["usd"])
            rews.append(platform["rewards_total"])

    dep = sum(deps)
    rew = sum(rews)
    if wallet is not None:
        if wallet.get("harvested-rewards", None) is not None:
            harvested_reinvested = sum([ float(x["amount"]["usd"]) for x in wallet["harvested-rewards"]])
            rew = rew + harvested_reinvested
            dep = dep - harvested_reinvested
    tot = dep + rew
    if verbose > 1:
       perc = harvested_reinvested / tot * 100.0
       print(f'Harvested & reinvested:                                                             reward: {harvested_reinvested:12.6f} USD, ({perc:6.4f} %)')
    perc = rew / dep * 100.000
    if verbose: print(f"{apiResponse.headers['Date']}: Value: {tot:>12.6f} USD    Deposits: {dep:>12.6f} USD    rewards: {rew:12.6f} USD    ROI: {perc:>12.6f} %")


def getYield():
    return requests.get('https://farm.army/api/v0/farms/0xEB1D8714D430Df1ebAd5dD202010d6fA020f4F07')


def openWallet(walletID):
    config = json.load(open('config.json', 'r'))
    config["wallets"] = json.load(open(config["wallet_list"]))
    wallet = config["wallets"][walletID]
    return wallet


if __name__ == '__main__':
    # Create and populate argument parser
    parser = argparse.ArgumentParser(prog='displayYield')
    parser.add_argument('-v', '--verbose', type=int, nargs='?',
                        help='Different levels of debug output. Default: 1'
                        ' (total only)', default=1, const=2,
                        dest='verbose')
    parser.add_argument('-w', '--wallet', type=int, nargs='?', default=None,
                        const=0, dest='wallet')

    # Read and convert input arguments
    args = parser.parse_args()
    apiResponse = getYield()
    if args.wallet is not None:
      wallet = openWallet(args.wallet)
    else:
      wallet = None

    displayYield(apiResponse, wallet, args.verbose)
