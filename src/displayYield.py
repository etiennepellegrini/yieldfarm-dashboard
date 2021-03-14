import requests

dep = []
rew = []
resp = requests.get('https://farm.army/api/v0/farms/0xEB1D8714D430Df1ebAd5dD202010d6fA020f4F07').json()
for platform in resp["platforms"]:
    for farm in platform["farms"]:
        dep.append(farm["deposit"]["usd"])
        rew.append(sum([x["usd"] for x in farm["rewards"]]))
        perc = float(rew[-1]/dep[-1])*100.0
        print(f'Farm: {farm["farm"]["id"]:35} ({farm["deposit"]["symbol"]:10}): deposits: {dep[-1]:9.8} USD, reward: {rew[-1]:9.6} USD, ({perc:5.03} %)')

print(f"Total: Deposits: {sum(dep):10.8}, rewards: {sum(rew):10.8}, ROI: {sum(rew)/max(sum(dep),1)*100:5.03} %")
