def log(text,e_no='',stat=''):
	column_pos=30
	space_gap=column_pos-len(text)
	#print(text,' '*space_gap,'||',e_no,stat)
	stuff=text+(' '*space_gap)+'|| '+e_no+' '+stat+'\n'
	with open('Dependencies/file.txt','a') as file:
		file.write(stuff)