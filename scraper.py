import requests
from bs4 import BeautifulSoup
import json


smit_link = input("Enter the SMIT Exam Link : ")
custom_link = []   # particular subjects URLs
header =  { 
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)'
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Mobile Safari/537.36' 
          }
fileName = smit_link[25:29]


def main():

    fileDict = {}
    session = requests.Session()

    html = session.get(smit_link.strip(), headers=header)
    soup = BeautifulSoup(html.content, 'html.parser')

    join_link = "https://result.smtech.in/grade.php?subid="

    fetch_links(join_link, soup)   # function call for fetching particular subjects

    for url in custom_link:
        html = session.get(url.strip(), headers=header)
        soup = BeautifulSoup(html.content, 'html.parser')

        write_text_into_file(soup)
        read_file(fileDict)
        convert_to_json(fileDict)


# Function which fetches data from individual exam links
def fetch_links(join_link, soup):
    for div in soup.find_all("div", {"class": "card-body"}):
        for paragraph in div.select("p"):
            for link in paragraph.select("a"):
                href = link['href']
                subcode = href[href.index('=')+1:]
                custom_link.append(join_link + subcode)


# Function which writes the soup into text format
def write_text_into_file(soup):
    writeTextFile = open("{}.txt".format(fileName), "w")
    writeTextFile.write(soup.find('pre').getText())
    writeTextFile.close()


# Function which reads data from text format
def read_file(fileDict):
    readTextFile = open("{}.txt".format(fileName))
    line = readTextFile.readline()

    read_text_from_File(fileDict, readTextFile, line)  # Important
    readTextFile.close()


# Function which arranges all data
def read_text_from_File(fileDict, readTextFile, line):

    count = 1
    code = "SUB"
    credit = 0.0
    reg = 0
    name = ""

    while line:
            try:
                line=line.strip().split()
            except: break
            if(len(line)==0 or line[0][0:3]=="REG" or line[0][0:3]=="SIK" or line[0][0:3]=="GRA" or line[0][0:3]=="Abb" or line[0][0:3]=="Abs" or line[0][0:3]=="S>=" or line[0][0:3]=="P>=" or line[0][0:3]=="Sto" or line[0][0:3]=="Gra"):
                line = readTextFile.readline()
                continue
            elif(line[0]=="Subject"):
                if(line[1]=="Code"):
                    code=line[3]
                elif(line[1]=="Title"):
                    i = 3
                    while(i < len(line)):
                        name += line[i]+" "
                        i += 1
                elif(line[1]=="Credit"):
                    credit = float(line[3][0:3])
            else:
                Dict = {}
                try:
                    reg = int(line[0])
                except: continue
                fileDict[reg] = fileDict.get(reg, {})
                Dict['sub'] = name
                Dict['int'] = line[1]
                Dict['ext'] = line[2]
                Dict['tot'] = line[3]
                Dict['grade'] = line[4]
                Dict['credit'] = credit
                fileDict[reg][code] = Dict
            line = readTextFile.readline()
     

# A function which converts the text fike into json format
def convert_to_json(fileDict):
    jsonDump = open("{}.json".format(fileName), "w")
    jsonDump.write(json.dumps(fileDict))
    jsonDump.close()

if __name__ == "__main__":
    main()