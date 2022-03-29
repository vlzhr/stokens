import requests
import pywaves as pw
from json import loads, dumps
from math import floor
from time import sleep

# claim rewards
ac = pw.Address() # initialize with a seed
ac.invokeScript("3P8w8NXZUtYdCA13tHbDY5sW4mC27ZFJgG3", "claimRewards", [], [], txFee=900000)
sleep(1)
usdnAmount = ac.balance("DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p")

# TODO: convert rewards to USDN

# get holders list
current_height = int(loads(requests.get("https://nodes.wavesnodes.com/blocks/height").text)["height"])
dic = loads((requests.get("https://nodes.wavesnodes.com/assets/8wUmN9Y15f3JR4KZfE81XLXpkdgwnqoBNG6NmocZpKQx/distribution/{}/limit/1000".format(str(current_height-1))).text))["items"]

# get total amount
snsbtAmount = sum(dic.values())
avgReward = str(round(usdnAmount / snsbtAmount * 10000) / 10000)

# prepare mass transfers list
mass_transfers = []
for address in dic:
    mass_transfers.append({
        "recipient": address,
        "amount": floor(dic[address] * usdnAmount / snsbtAmount)
    })

# send mass transfers
distNum = str(2)
totalSum = str(floor(usdnAmount / 10000) / 100)
attachment_text = "#{} sNSBT rewards distribution: total of ${}, {} USDN per sNSBT. Buy sNSBT on PuzzleSwap.org to get daily rewards!".format(distNum, totalSum, avgReward)
for step in range(round(len(mass_transfers) / 100) + 1):
    print(ac.massTransferAssets(mass_transfers[step*100:(step+1)*100], pw.Asset("DG2xFkPdDwKUoBkzGAhQtLpSGzfXLiCYPEzeKH2Ad24p"), attachment_text, baseFee=500000))
