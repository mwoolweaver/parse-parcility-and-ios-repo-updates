import requests
from requests import get
import json
import re

# The repos we don't count/need 
defaultRepos = ["http://cydia.zodttd.com/repo/cydia", "http://apt.modmyi.com", "http://apt.thebigboss.org/repofiles/cydia", "https://apt.bingner.com", "http://apt.saurik.com", "http://apt.thebigboss.org", "https://apt.procurs.us", "https://repo.packix.com", "https://repo.dynastic.co", "https://repounclutter.coolstar.org", "https://repo.theodyssey.dev", "https://repo.chariz.com", "https://checkra.in/assets/mobilesubstrate", "https://repo.chimera.sh"]

reposWithIssues = ["https://repo.sciency.us", "https://wizage.github.io/repo/", "https://iluwqaa.github.io/", "https://booleanmagic.com/repo", "https://cydiamy.github.io/1.0.4", "https://chickenmatt5.github.io/repo", "https://iamjamieq.github.io/repo", "http://rcrepo.com", "https://bandarhl.github.io", "https://xninja.xyz/apt", "https://apt.xninja.xyz", "https://coolstar.org/publicrepo"]

# Where we source our repo list from
getParcility = get("https://api.parcility.co/db/repos/small")
getIRU = get("https://api.ios-repo-updates.com/1.0/popular-repos/")

jsonParcility = getParcility.json()
jsonIRU = getIRU.json()

parcility = jsonParcility["data"]
IRU = jsonIRU

listBeforeCheck = []

listIRU = []
listIRUDUP = []

for repoIRU in IRU:
    lbc1 = repoIRU["url"].rstrip('/')
    lbc1strip = lbc1.lstrip()
    if lbc1strip not in listBeforeCheck:
        listBeforeCheck.append(lbc1strip)
        listIRU.append(lbc1strip)
    else:
        listIRUDUP.append(lbc1strip)

listIRU.sort()
listBeforeCheck.sort()

listParcility = []
listParcilityDUP = []
for repoParcility in parcility:
    lbc2 = repoParcility["url"].rstrip('/')
    lbc2strip = lbc2.lstrip()
    if lbc2strip not in listBeforeCheck:
        listBeforeCheck.append(lbc2strip)
        listParcility.append(lbc2strip)
    else:
        listParcilityDUP.append(lbc2strip)

listParcility.sort()
listBeforeCheck.sort()

listAfterCheck = []
listAfterCheckDUP = []
defaultInLBC = []
WithIssuesInLBC = []

for i in listBeforeCheck:
    if i not in listAfterCheck:
        if i not in defaultRepos:
            if i not in reposWithIssues:
                listAfterCheck.append(i)
            else:
                WithIssuesInLBC.append(i)
        else:
            defaultInLBC.append(i)
    else:
        listAfterCheckDUP.append(i)

noFind = []

releaseFilesLAC = []

listAfterCheck.sort()
for repo in listAfterCheck:

    checkPackurl = repo + "/Release"

    try:
        checkPack = get(checkPackurl, headers={"User-Agent":"Debian APT-HTTP/1.3 (2.1.10)"}, timeout=2)

    except requests.exceptions.ReadTimeout as err:
        print ("\n")
        print ("Not added.")
        print ((listAfterCheck.index(repo)+1), repo)
        print (err)
        print ("\n")
        noFind.append([repo, err])
        continue # start the while loop over and try the next repo.

    except requests.exceptions.ConnectionError as err:
        print ("\n")
        print ("Not added.")
        print ((listAfterCheck.index(repo)+1), repo)
        print (err)
        print ("\n")
        noFind.append([repo, err])
        continue # start the while loop over and try the next repo.

    if checkPack.status_code == 200:
        print ((listAfterCheck.index(repo)+1), repo, checkPack.status_code)
        releaseFilesLAC.append([repo, checkPack.content])

    else:
        print ("\n")
        print ("Not added.")
        print ((listAfterCheck.index(repo)+1), repo, checkPack.status_code)
        print ("\n")
        noFind.append([repo, checkPack.status_code])

notDupURL = []
notDupRelease = []

isDupURL = []
isDupRelease = []

notValidRelease = []

word = b'Origin:'
for file in releaseFilesLAC:
    if file[1] not in notDupRelease:
        if word in file[1]:
            notDupURL.append(file[0])
            notDupRelease.append(file[1])
        else:
            notValidRelease.append(file)
    else:
        isDupURL.append(file[0])
        isDupRelease.append(file[1])

wasGH = []
oldGH = []

wasGL = []
oldGL = []

wasAS = []
oldAS = []

wasHTTP = []
oldHTTP = []

notChanged = []

for dupRelease in isDupRelease:

    indexND = notDupRelease.index(dupRelease)
    indexID = isDupRelease.index(dupRelease)

    boolGH = False
    boolGL = False
    boolAS = False
    boolHTTP = False

    if bool(re.search(r'\b(\.github\.io)\b', notDupURL[indexND])):
        
        indexID = isDupRelease.index(dupRelease)
        oldGH.append([notDupURL[indexND], isDupURL[indexID]])
        notDupURL[indexND] = isDupURL[indexID]
        wasGH.append(notDupURL[indexND])
        boolGH = True
    
    if bool(re.search(r'\b(\.gitlab\.io)\b', notDupURL[indexND])):
        
        indexID = isDupRelease.index(dupRelease)
        oldGL.append([notDupURL[indexND], isDupURL[indexID]])
        notDupURL[indexND] = isDupURL[indexID]
        wasGL.append(notDupURL[indexND])
        boolGL = True

    if bool(re.search(r'\b(\.appspot\.com)\b', notDupURL[indexND])):
        
        indexID = isDupRelease.index(dupRelease)
        oldAS.append([notDupURL[indexND], isDupURL[indexID]])
        notDupURL[indexND] = isDupURL[indexID]
        wasAS.append(notDupURL[indexND])
        boolAS = True
        
    if bool(re.search(r'(http\:\/\/)', notDupURL[indexND])):
        
        indexID = isDupRelease.index(dupRelease)
        oldHTTP.append([notDupURL[indexND], isDupURL[indexID]])
        notDupURL[indexND] = isDupURL[indexID]
        wasHTTP.append(notDupURL[indexND])
        boolHTTP = True

    if (boolGH == False and boolHTTP == False and boolGL == False and boolAS == False):
        notChanged.append([notDupURL[indexND], isDupURL[indexID]])

print ("\n")
print ("\n")
print ("There are " + str(len(listBeforeCheck)) + " repos on Parcility.co & ios-repo-updates.com combined")
print ("\n")
print ("Found " + str(len(defaultInLBC)) + " default repos but will not add to list")
#for default in defaultInLBC:
#    print (default)
print ("\n")
print ("Found " + str(len(WithIssuesInLBC)) + " repos that could cause issues.")
#for withIssues in WithIssuesInLBC:
#    print (withIssues)
print ("\n")
print ("Failed to find " + str(len(noFind)) + " repos.")
#for notFound in noFind:
#    print (notFound)
print ("\n")
print ("Found " + str(len(notValidRelease)) + " with invalid release files.")
#for invalid in notValidRelease:
#    print (invalid[0])
print ("\n")
print ("Found " + str(len(isDupRelease)) + " duplicate release files.")
#for url in isDupURL:
#   print (uel)
print ("\n")
print ("Found " + str(len(oldGH)) + " old github URL's that were changed to custom url.")
#for url in oldGH:
#    print (url)
print ("\n")
print ("Found " + str(len(oldGL)) + " old gitlab URL's that were changed to custom url.")
#for url in oldGL:
#    print (url)
print ("\n")
print ("Found " + str(len(oldAS)) + " old appspot URL's that were changed to custom url.")
#for url in oldAS:
#    print (url)
print ("\n")
print ("Found " + str(len(oldHTTP)) + " old http URL's changed to https.")
#for url in oldHTTP:
#    print (url)
print ("\n")
print ("Found " + str(len(notChanged)) + " URL's that didn't change even tho the release file was the same.")
#print ("if (github.io OR gitlab.io) url is on the right it shouldn't change")
#for url in notChanged:
#    print (url)
print ("\n")
print ("Found " + str(len(notDupURL)) + " valid repos to be added to list.")
#for url in notDupURL:
#    print (url)

notDupURL.sort()
with open('just-urls-sources.list', 'w') as f:
    for url in notDupURL:
        if url != None:
            f.write("%s\n" % url)

with open('sources.list', 'w') as f:
    for repo in notDupURL:
        if repo != None:
            f.write("deb %s/ ./\n" % repo)
