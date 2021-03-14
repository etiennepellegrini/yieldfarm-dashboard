import argparse
import requests


def displayYield(apiResponse, verbose=1):
    deps = []
    rews = []
    resp = apiResponse.json()
    for platform in resp["platforms"]:
        for farm in platform["farms"]:
            deps.append(farm["deposit"]["usd"])
            rews.append(sum([x["usd"] for x in farm["rewards"]]))
            perc = float(rews[-1]/deps[-1])*100.0
            if verbose > 1:
                print(f'Farm: {farm["farm"]["id"]:35} ({farm["deposit"]["symbol"]:10}): deposits: {deps[-1]:9.8} USD, reward: {rews[-1]:9.6} USD, ({perc:5.03} %)')

    dep = sum(deps)
    rew = sum(rews)
    tot = dep + rew
    perc = rew / dep * 100.0
    if verbose: print(f"{apiResponse.headers['Date']}: Value: {tot:>10.4f} USD    Deposits: {dep:>10.4f} USD    rewards: {rew:10.4f} USD    ROI: {perc:>6.4} %")


def getYield():
    return requests.get('https://farm.army/api/v0/farms/0xEB1D8714D430Df1ebAd5dD202010d6fA020f4F07')


if __name__ == '__main__':
    # Create and populate argument parser
    parser = argparse.ArgumentParser(prog='displayYield')
    parser.add_argument('-v', '--verbose', type=int, nargs='?',
                        help='Different levels of debug output. Default: 1'
                        ' (total only)', default=1, const=2,
                        dest='verbose')

    # Read and convert input arguments
    args = parser.parse_args()
    apiResponse = getYield()
    displayYield(apiResponse, args.verbose)
