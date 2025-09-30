from Dependencies import constants 


def generate_stats():
	grades_count={}
	text=""
	with open(constants.CsvFile,'r') as file:
		content=file.read().split('\n')[1:]
		for line in content:
			fields=line.split(',')
			grades=fields[2:-3]
			for grade in grades:
				grade=grade.replace(' ','')
				if not(grade in grades_count):
					grades_count[grade]=0

		text+=','*(len(content[0].split(','))-1)+'\n'
		for grade in sorted(grades_count.keys()):
			counter=[]
			for i in range(2,len(content[0].split(','))-3):	
				counter.append(0)
				for line in content:
					if line:
						if line.split(',')[i].replace(' ','')==grade:
							counter[-1]+=1
			
			text+=','+grade
			for c in counter:
				text+=','+str(c)
			text+=', Total('+grade+') = '+str(sum(counter))+',,\n'
	with open(constants.CsvFile,'a') as file:
		#print(text)
		file.write(text)

#generate_stats()