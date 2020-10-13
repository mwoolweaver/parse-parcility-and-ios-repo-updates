import requests
from requests import get
import json
import re

def contains_word(s, w):
    return (' ' + w + ' ') in (' ' + s + ' ')

word = b'Origin:'

defaultRepos = ["http://apt.modmyi.com", "http://apt.thebigboss.org/repofiles/cydia", "https://apt.bingner.com", "http://apt.saurik.com", "http://apt.thebigboss.org", "https://apt.procurs.us", "https://repo.packix.com", "https://repo.dynastic.co", "https://repounclutter.coolstar.org", "https://repo.theodyssey.dev", "https://repo.chariz.com", "https://checkra.in/assets/mobilesubstrate", "https://repo.chimera.sh"]

reposWithIssues = ["https://repo.sciency.us", "https://wizage.github.io/repo/", "https://iluwqaa.github.io/", "https://booleanmagic.com/repo", "https://cydiamy.github.io/1.0.4", "https://chickenmatt5.github.io/repo", "https://iamjamieq.github.io/repo", "http://rcrepo.com", "https://bandarhl.github.io", "https://xninja.xyz/apt", "https://apt.xninja.xyz"]

# Where we source our repo list from
getParcility = get("https://api.parcility.co/db/repos/small")
getIRU = get("https://api.ios-repo-updates.com/1.0/popular-repos/")

jsonParcility = getParcility.json()
jsonIRU = getIRU.json()

parcility = jsonParcility["data"]
IRU = jsonIRU

beforeCheck = []

for repoIRU in IRU:
    bc1 = repoIRU["url"].rstrip('/')
    beforeCheck.append(bc1.lstrip())

for repoParcility in parcility:
    bc2 = repoParcility["url"].rstrip('/')
    beforeCheck.append(bc2.lstrip())

res = []
notRES = []
defaultIn = []
numWithIssues = []

beforeCheck.sort()
for i in beforeCheck:
    if i not in res:
        if i not in defaultRepos:
            if i not in reposWithIssues:
                res.append(i)
            else:
                numWithIssues.append(i)
        else:
            defaultIn.append(i)
    else:
        notRES.append(i)

res.sort(reverse=True)
maxRepo = len(res) - 1
noFind = []
found = []
releaseFiles = []
while maxRepo >= 0:

        checkPackurl = res[maxRepo] + "/Release"
        try:
            checkPack = get(checkPackurl, headers={"User-Agent":"Debian APT-HTTP/1.3 (2.1.10)"}, timeout=2)

        except requests.exceptions.ReadTimeout as err:
            print ("\n")
            print ("Not added.")
            print (maxRepo, res[maxRepo])
            print (err)
            print ("\n")
            noFind.append([res[maxRepo], err])
            maxRepo -= 1
            continue # start the while loop over and try the next repo.

        except requests.exceptions.ConnectionError as err:
            print ("\n")
            print ("Not added.")
            print (maxRepo, res[maxRepo])
            print (err)
            print ("\n")
            noFind.append([res[maxRepo], err])
            maxRepo -= 1
            continue # start the while loop over and try the next repo.

        if checkPack.status_code == 200:
            print (maxRepo, res[maxRepo], checkPack.status_code)
            found.append([res[maxRepo], checkPack.content])
            maxRepo -= 1

        else:
            print ("\n")
            print ("Not added.")
            print (maxRepo, res[maxRepo], checkPack.status_code)
            print ("\n")
            noFind.append([res[maxRepo], checkPack.status_code])
            maxRepo -= 1

checkDup = []
notDup = []
isDup = []
notValid = []

for file in found:
    if file[1] not in checkDup:
        if word in file[1]:
            checkDup.append(file[1])
            notDup.append(file[0])
        else:
            notValid.append(file)
    else:
        isDup.append(file)

print ("\n")
print ("\n")
print ("\n")
print ("Found " + str(len(notRES)) + " duplicate URLs.")
#for url in notRES:
    # print (url)

print ("\n")
print ("Found " + str(len(isDup)) + " duplicate release files.")
#for dup in isDup:
   # print (dup[0])

print ("\n")
print ("Found " + str(len(notValid)) + " with invalid release files.")
#for invalid in notValid:
#    print (invalid[0])

print ("\n")
print ("Failed to find " + str(len(noFind)) + " repos.")
#for notFound in noFind:
#    print (notFound)

print ("\n")
print ("Found " + str(len(numWithIssues)) + " repos that could cause issues.")
#for withIssues in numWithIssues:
#    print (withIssues)

print("\n")
print ("Found " + str(len(defaultIn)) + " default repos found but will not add to list")
#for default in defaultIn:
#    print (default)

print ("\n")
print ("Found " + str(len(notDup)) + " valid repos to be added to list.")
#for ND in notDup:
#    print (ND)

print ("\n")
print ("The combined number of repos on Parcility.co & ios-repo-updates.com")
print (len(beforeCheck))


notDup.sort()
with open('just-urls-sources.list', 'w') as f:
    for url in notDup:
        if url != None:
            f.write("%s\n" % url)

with open('sources.list', 'w') as f:
    for repo in notDup:
        if repo != None:
            f.write("deb %s/ ./\n" % repo)
