import requests
from lxml import html
import psycopg2


res = requests.get('https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=3&ssid=20&smid=15')

tree = html.fromstring(res.text)

# print(res.text)

lst = []

i = 1
while(True):
# for i in range(5):
	link = tree.xpath('//*[@id="sample_1"]/tbody/tr[' + str(i) + ']/td[2]/a')

	if(link == []):
		break

	link = link[0].attrib.get('href')
	print("Fetching :" , link)

	res2 = requests.get(link)

	# print(res2.text)
	tree2 = html.fromstring(res2.text)

	j = 1
	while(True):
		pdf_link = tree2.xpath('//*[@id="member-wrapper"]/section[2]/div[1]/section/div[2]/table/tbody/tr['+ str(j) +']/td[2]/a')
		if(pdf_link == []):
			break
		lst.append(pdf_link[0].attrib.get('href'))
		j += 1


	print()
	print()
	print()
	i += 1



print(lst)


connection = psycopg2.connect(user = "srajika",
                                      password = "12345",
                                      host = "127.0.0.1",
                                      port = "5432",
                                      database = "postgres")

cursor = connection.cursor()

# create_table = "create table sebi_data(id serial primary key, pdf_link varchar(256));"
# cursor.execute(create_table)


insert_stmnt = "insert into sebi_data(pdf_link) values (%s);"

for i in lst:
	tup = (str(i))
	cursor.execute(insert_stmnt, tup)

connection.commit() 


if(connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
