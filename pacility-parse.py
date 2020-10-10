from requests import get
import json

getParcility = get("https://api.parcility.co/db/repos/small")

jsonParcility = getParcility.json()

numRepos = len(jsonParcility["data"])

repoList = [None] * numRepos

numRepos -= 1
while numRepos >= 0:
    repoList[numRepos] = "deb " + jsonParcility["data"][numRepos]["url"] + " ./"

    print (numRepos, repoList[numRepos])
    numRepos -= 1

print ("" + jsonParcility["data"][631]["url"])

with open('sources.list', 'w') as f:
    for repo in repoList:
        f.write("%s\n" % repo)