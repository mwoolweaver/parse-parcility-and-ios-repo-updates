import requests
from requests import get
import json
import re

def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

word = b'Origin:'

defaultRepos = ["https://apt.bingner.com", "http://apt.saurik.com", "http://apt.thebigboss.org", "https://apt.procurs.us", "https://repo.packix.com", "https://repo.dynastic.co", "https://repounclutter.coolstar.org", "https://repo.theodyssey.dev", "https://repo.chariz.com", "https://checkra.in/assets/mobilesubstrate", "https://repo.chimera.sh"]

reposWithIssues = ["https://booleanmagic.com/repo", "https://cydiamy.github.io/1.0.4", "https://chickenmatt5.github.io/repo", "https://iamjamieq.github.io/repo", "http://rcrepo.com", "https://bandarhl.github.io"]

numDefault = len(defaultRepos)
getParcility = get("https://api.parcility.co/db/repos/small")

jsonParcility = getParcility.json()

parcility = jsonParcility["data"]

numRepos = len(jsonParcility["data"])

# repoURLs = [None] * numRepos
repoList = [None] * numRepos
repoListURLs = [None] * numRepos

beforeCheck = [None] * numRepos

numAdded = 0

# print (parcility)
x = 0
for repo in parcility:
    bc = repo["url"].rstrip('/')
    beforeCheck[x] = bc.lstrip()
    x += 1

res = []
notRES = []
defaultIn = 0
numWithIssues = 0
for i in beforeCheck: 
    if i not in res:
        if i not in defaultRepos:
            if i not in reposWithIssues:
                res.append(i)
            else:
                numWithIssues += 1
        else:
            defaultIn += 1
    else:
        notRES.append(i)

maxRepo = len(res) - 1
noFind = []
found = []
releaseFiles = []
while maxRepo >= 0:

        checkPackurl = res[maxRepo] + "/Release"
        try:
            checkPack = get(checkPackurl, headers={"User-Agent":"Debian APT-HTTP/1.3 (2.1.10)"}, timeout=2)

        except requests.exceptions.ReadTimeout as er:
            print ("\n")
            print ("Not added.")
            print (maxRepo, res[maxRepo])
            print (er)
            print ("\n")
            noFind.append(res[maxRepo])
            maxRepo -= 1
            continue # start the while loop over and try again.

        except requests.exceptions.ConnectionError as err:
            print ("\n")
            print ("Not added.")
            print (maxRepo, res[maxRepo])
            print (err)
            print ("\n")
            noFind.append(res[maxRepo])
            maxRepo -= 1
            continue # start the while loop over and try again.

        if checkPack.status_code == 200:
            repoListURLs[maxRepo] = res[maxRepo]
            repoList[maxRepo] = "deb " + repoListURLs[maxRepo] + " ./"
            print (maxRepo, res[maxRepo], checkPack.status_code)
            found.append([res[maxRepo], checkPack.content])
            #releaseFiles.append(checkPack.content)
            maxRepo -= 1

        else:
            print ("\n")
            print ("Not added.")
            print (maxRepo, res[maxRepo], checkPack.status_code)
            print ("\n")
            noFind.append(res[maxRepo])
            maxRepo -= 1

checkDup = []
notDup = []
isDup = []
notValid = []
z = 0
for file in found:
    if file[1] not in checkDup:
        if word in file[1]:
            checkDup.append(file[1])
            notDup.append(file[0])
            z += 1
        else:
            notValid.append(file)
    else:
        isDup.append(file)

print ("\n")
print ("\n")
print ("\n")
print ("Found " + str(len(notRES)) + " duplicate URLs")
#for url in notRES:
    # print (url)

print ("\n")
print ("found " + str(len(isDup)) + " duplicate release files")
#for dup in isDup:
   # print (dup[0])

print ("\n")
print ("found " + str(len(notValid)) + " with not valid release files")
#for invalid in notValid:
#    print (invalid[0])

print ("\n")
print ("Failed to find " + str(len(noFind)))
#for notFound in noFind:
#    print (notFound)

print ("\n")
print ("Found " + str(numWithIssues) + " repos that cause issues.")

print("\n")
print ("Default repos found but will not add to list")
print (defaultIn)

print ("\n")
print ("Found " + str(len(notDup)) + " valid repos to be added to list.")

print ("\n")
print ("Number of repo on Parcility.co")
print (numRepos)


with open('just-urls-sources.list', 'w') as f:
    for url in notDup:
        if url != None:
            f.write("%s\n" % url)

with open('sources.list', 'w') as f:
    for repo in notDup:
        if repo != None:
            f.write("deb %s/ ./\n" % repo)
