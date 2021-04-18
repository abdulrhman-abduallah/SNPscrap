#! /usr/bin/python3
# a project on SNP analysis using university of bahri pipline

import bs4,requests,webbrowser,sys,os,pyperclip,openpyxl,re
from selenium import webdriver


genename=str(sys.argv[1]) #the gene name should be input as an argument 
genename=str(genename)
genename=genename.upper()
print("The Gene to be analyzed is: "+genename)
link='https://ncbi.nlm.nih.gov/gene/?term='+genename

res=requests.get(link)
#webbrowser.open(link)

page=bs4.BeautifulSoup(res.text,'lxml')

a=page.select('a') #select all elements with an <a> tag

x=0 #this stores the index of the gene of interest in the loop

for i in range(len(a)):
	m=a[i].getText()
	if genename in m:
		#print(m)
		#print(i)
		x=i
		break
		


link1=a[x].get('href') #gets the link to the gene website in ncbi

print(link1)
if 'ncbi' in link1:
	link2=link1
else:
	link2='https://ncbi.nlm.nih.gov'+link1
#print(link12)
res1=requests.get(link2)
page1=bs4.BeautifulSoup(res1.text,'lxml')

#webbrowser.open(link2)

a=page1.select('a') #select all elements with an <a> tag

x=0 #this stores the index of the gene of interest in the loop

for i in range(len(a)):
	m=a[i].getText()
	if 'Geneview' in m:
		#print(m)
		#print(i)
		x=i
		break

link3=a[x].get('href') #gets the link to the snps website
#webbrowser.open(link3)

	
browser=webdriver.Firefox()
browser.get(link3)
linkElem=browser.find_elements_by_tag_name('input')
for i in range(len(linkElem)):
	m=linkElem[i].get_attribute('value')
	if m=='Download':
		linkElem[i].click()
		break

print('you have to open sift website manually as it has security block for automated browsers')
#webbrowser.open('https://sift.bii.a-star.edu.sg/www/SIFT_dbSNP.html')

snfile=input('Type the name of excel sheet containing the SIFT results: ')


sn=openpyxl.load_workbook(snfile)


#print(sheet['A3'].value)

sheet1=sn.active
sheet2=sn.create_sheet()
half=0
y=0
h=sheet1.max_column
snps=''


for i in sheet1:
	for j in i:
		if j.value=='DELETERIOUS':
			half=half+1
			for x in range(1,h):
				sheet2.cell(row=half,column=x).value=i[x].value
				sheet2.cell(row=half,column=1).value=i[0].value
				



	
				



sn.save('snps2.xlsx')




###########################################################################################################################
snpslist=''
#The Second phase of the analysis 
snpsregex=re.compile(r'(\w)(\d*)(\w)')

for i in sheet2['F']:
	snps=snps+' '+i.value
	
snpslist=snpsregex.findall(snps)


#print(snpslist)

fasta=input('put the fasta sequence without the definition line')
browser=webdriver.Firefox()	
#move to snps&go website
browser.get('https://snps.biofold.org/snps-and-go/snps-and-go.html')

browser.find_element_by_name('proteina').send_keys(fasta) 	#fill sequence area with protein sequence

browser.find_element_by_name('posizione').send_keys(snps)	#fill the mutations area with the snpslist

browser.find_element_by_name('submit').click()


soup=bs4.BeautifulSoup(browser.page_source,features='lxml')

a=soup.select('a')

for i in a:
	if 'snps.biofold' in i.getText():
		l=i.get('href')
		
browser.get(l)

browser1=webdriver.Firefox()
browser1.get('http://provean.jcvi.org/protein_batch_submit.php?species=human')
ptid=input('protein ID(pdbid): ')
proveanlist=''
for i in snpslist:
	proveanlist=proveanlist+' '+ptid+' '+i[1]+' '+i[0]+' '+i[2]+'\n'

browser1.find_element_by_name('variants').send_keys(proveanlist)

l=browser1.find_elements_by_tag_name('input')

for i in l:
	if i.get_attribute('type')=='submit':
		i.click()






















































