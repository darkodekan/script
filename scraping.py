import requests, math, json, csv
import sqlite3
bachelor = 87707
bachelor_pages = math.ceil(bachelor/10)

conn = sqlite3.connect('degrees.db')
#program name
#duration
#tuition
#degree type 
#school name 
#location

#overview
#program outline
#key facts
#admission requirements
#fees
#funding
levels = {"bachelor":math.ceil(87667/10), "master":math.ceil(69439/10), "phd":math.ceil(5683/10)}
conn.execute("CREATE TABLE IF NOT EXISTS degree(id int, name string, duration string, tuition string, type string, organization string, location string, overview string, program_outline string, admission_requirements string, fees_funding string)");
conn.commit()
for level in levels:
	for i in range(0, levels[level]):
		url = "https://search.prtl.co/2018-07-23/?start="+str(10*i)+"&q=en-24%7Clv-"+level+"%7Ctc-EUR%7Cuc-23"
		json_products = json.loads(requests.get(url).text)
		for degree in json_products:
			id = degree['id']
			name = degree['title']
			print(name)
			duration = ''
			try:
				duration = str((float(degree['fulltime_duration']['value'])/12))
			except Exception as e:
				print(e)
			tuition = ''
			try:
				tuition = str(degree['tuition_fee']['value']) + " " + str(degree['tuition_fee']['currency'])
			except Exception as e:
				print(e)
			print(url)
			degree_type = degree['level'] + " " + degree['degree']
			school = degree['organisation']
			print(school)
			location = ''
			try: 
				location = degree['venues'][0]['city'] + ", " + degree['venues'][0]['area'] + ', ' + degree['venues'][0]['country']
			except Exception as e:
				print(e)
			conn.execute("INSERT INTO degree(id, name, duration, tuition, type, organization, location) VALUES(?,?,?,?,?,?,?)", (id, name, duration, tuition, degree_type, school, location))
			conn.commit()
		
