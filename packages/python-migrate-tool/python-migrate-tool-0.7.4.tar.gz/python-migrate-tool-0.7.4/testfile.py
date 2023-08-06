import re
from alaya.utils.transfer_address import addresstoapt

file = open("D:/client-sdk/forPR/python tool/client-python-tool/test/testaddress1.sol","r+",encoding = 'utf-8')
new = []
for line in file:
    #0.4.26 0.5.17 0.6.12 0.7.1
    if 'pragma solidity' in line :
      if "0.4." in line:
          ind = line.find('0.4.')
          ind1 = line.find(';')
          line=line[:ind]+'0.4.26'+line[ind1:]
      if "0.5." in line:
          ind = line.find('0.5.')
          ind1 = line.find(';')
          line=line[:ind]+'0.5.17'+line[ind1:]
      if "0.6." in line:
          ind = line.find('0.6.')
          ind1 = line.find(';')
          line=line[:ind]+'0.6.12'+line[ind1:]
      if "0.7." in line:
          ind = line.find('0.7.')
          ind1 = line.find(';')
          line=line[:ind]+'0.7.1'+line[ind1:]
    if 'LAT' in line:
        index=line.find('LAT')
        s=re.findall('LAT.*?\n',line)
        if len(s[0]) < 44:
            if (line[index-1].isspace() and line[index-2].isnumeric()) and (s[0][3]==';' or s[0][3].isspace):
               line = line.replace('LAT','ATP')
    if 'LAX' in line:
        index=line.find('LAX')
        s=re.findall('LAX.*?\n',line)
        if len(s[0]) < 44:
            if (line[index-1].isspace() and line[index-2].isnumeric()) and (s[0][3]==';' or s[0][3].isspace):
               line = line.replace('LAX','ATX')
    if 'lax' in line:
        index=line.find('lax')
        s=re.findall('lax.*?\n',line)
        if len(s[0]) < 44:
            if (line[index-1].isspace() and line[index-2].isnumeric()) and (s[0][3]==';' or s[0][3].isspace):
               line = line.replace('lax','atx')
        if len(s[0])==44:
           ts=addresstoapt(s[0][0:42])
           line=line[:index]+ts+s[0][-2:]
        if len(s[0])>44 and addresstoapt(s[0][0:42]):
           a1=[]
           a2=[]
           for a in re.finditer('lax',s[0]):
              a1.append(a.span())
           for a0 in re.finditer(',',s[0]):
              a2.append(a0.span())
           if len(a1)>=len(a2):
               addr=line[:index]
               for i in range(len(a1)):
                   if i == len(a1)-1:
                      addr=addr+addresstoapt(s[0][a1[i][0]:a1[i][0]+42])+s[0][a1[i][0]+42:]
                   else:
                      addr = addr+addresstoapt(s[0][a1[i][0]:a2[i][0]-1]) + s[0][a2[i][0]-1:a2[i][1]+1]
               line=addr
    if 'lat' in line:
        index=line.find('lat')
        s=re.findall('lat.*?\n',line)
        if len(s[0]) < 44:
            if (line[index-1].isspace() and line[index-2].isnumeric()) and (s[0][3]==';' or s[0][3].isspace):
               line = line.replace('lat','atp')
        if len(s[0])==44:
           ts=addresstoapt(s[0][0:42])
           line=line[:index]+ts+s[0][-2:]
        if len(s[0])>44 and addresstoapt(s[0][0:42]):
           a1=[]
           a2=[]
           for a in re.finditer('lat',s[0]):
              a1.append(a.span())
           for a0 in re.finditer(',',s[0]):
              a2.append(a0.span())
           if len(a1)>=len(a2):
               addr=line[:index]
               for i in range(len(a1)):
                   if i == len(a1)-1:
                      addr=addr+addresstoapt(s[0][a1[i][0]:a1[i][0]+42])+s[0][a1[i][0]+42:]
                   else:
                      addr = addr+addresstoapt(s[0][a1[i][0]:a2[i][0]-1]) + s[0][a2[i][0]-1:a2[i][1]+1]
               line=addr
    if '0x' in line:
        index=line.find('0x')
        s=re.findall('0x.*?\n',line)
        if len(s[0])==44:
           ts=addresstoapt(s[0][1:42])
           line=line[:index]+ts+s[0][-2:]
        if len(s[0])>44 and addresstoapt(s[0][0:42]):
           a1=[]
           a2=[]
           for a in re.finditer('0x',s[0]):
              a1.append(a.span())
           for a0 in re.finditer(',',s[0]):
              a2.append(a0.span())
           if len(a1)>=len(a2):
               addr=line[:index]
               for i in range(len(a1)):
                   if i == len(a1)-1:
                      addr=addr+addresstoapt(s[0][a1[i][0]:a1[i][0]+42])+s[0][a1[i][0]+42:]
                   else:
                      addr = addr+addresstoapt(s[0][a1[i][0]:a2[i][0]-1]) + s[0][a2[i][0]-1:a2[i][1]+1]
               line=addr
    new.append(line)

file.seek(0)
for n in new:
    file.write(n)
file.close()
