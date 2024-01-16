from requests import get
from json import loads, dumps

pools = loads(get("https://puzzle-js-back.herokuapp.com/api/v1/pools").text)
result = {"assets": {}, "pools": {}}
tokens = {"sNSBT": "8wUmN9Y15f3JR4KZfE81XLXpkdgwnqoBNG6NmocZpKQx"}

exceptions = {
    "3P5XtYc2UNoJPzffK5Ex1UdmqMCYuFqziAa": "3PAac3dNbhhX9qo4oxCxo4GY8SXYUHADVa9"
}

for token in tokens:
    decimals = 1e8 if token != "sNSBT" else 1e6
    tokenId = tokens[token]

    distr = loads(
        get("https://nodes.wavesnodes.com/assets/"+tokenId+"/distribution/3999969/limit/1000").text)[
        "items"]

    users = {n: distr[n] for n in distr}
    print(users)
    poolAddresses = [pool["contractAddress"] for pool in pools if tokenId in [asset["assetId"] for asset in pool["assets"]]]
    for address in poolAddresses:
        poolBalance = loads(get("https://nodes-puzzle.wavesnodes.com/addresses/balance/"+address).text)["balance"] if tokenId == "WAVES" else  loads(get("https://nodes-puzzle.wavesnodes.com/assets/balance/{}?id={}".format(address, tokenId)).text)["balances"][0]["balance"]
        data = loads(get("https://nodes-puzzle.wavesnodes.com/addresses/data/"+address).text)
        dic = {n["key"]: n["value"] for n in data}

        if not dic.get("global_indexStaked", 0) == 0:
            for n in dic:
                if "indexStaked" in n and not "global" in n:
                    users[n.split("_")[0]] = users.get(n.split("_")[0], 0) + int(poolBalance * dic[n] / dic["global_indexStaked"])

            print(address, poolAddresses.index(address) + 1)
        else:
            print("empty pool", address)

        result["pools"][address] = "PuzzleSwap"

    users = {exceptions.get(n, n): users[n] / decimals for n in users if not users[n] < decimals and not n in result["pools"]}
    result["assets"][token] = users

with open("result-160124.json", "w") as f:
    f.write(dumps(result, sort_keys=True, indent='\t', separators=(',', ': ')))

