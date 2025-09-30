from bs4 import BeautifulSoup as bs
from bs4 import element as bselement
from Dependencies import constants


def page_to_csv(e_no,html_doc):
    soup = bs(html_doc[0], 'html.parser')
    table = soup.find(id=constants.TableId)


    finall=[]
    for a in table.children:
        if type(a)==bselement.Tag:
            for b in a.children:
                if type(b)==bselement.Tag:
                    for c in b.children:
                        if type(c)==bselement.Tag:
                            for d in c.children:
                                if type(d)==bselement.Tag:
                                    for e in d.children:
                                        if type(e)==bselement.Tag:
                                            for f in e.children:
                                                if type(f)==bselement.Tag:
                                                    for g in f.children:
                                                        if type(g)==bselement.Tag:
                                                            for h in g.children:
                                                                if type(h)==bselement.Tag:
                                                                    scraped_text=h.text.replace('  ','').replace('\n','')
                                                                    if len(scraped_text):
                                                                        finall.append(str(scraped_text))
                                                                    


    finall=finall[1:-6]

    student_headers=finall[:12:2]
    student_details=finall[1:13:2]

    grade_headers=finall[12:-6:4][1:]
    grade_details=finall[15:-6:4][1:]

    
    #print(finall)
    write_mode='a'
    content=""
    emt=False
    
    try:
        with open(constants.CsvFile,'r') as file:
            lines=file.readlines()
            data=lines[0].replace('\n','').split(',')
            for subj in grade_headers:
                if not(subj in data):
                    emt=True
    except:
        emt=True

    if emt:
        for subj in student_headers[:2]:
            content+=subj+','

        for subj in grade_headers:
            content+=subj+','

        for subj in finall[-6:-3]:
            content+=subj+','

        content=content[:-1]+'\n'
        write_mode='w'

    for subj in student_details[:2]:
        content+=subj+','

    for subj in grade_details:
        content+=subj+','

    for subj in finall[-3:]:
        content+=subj.replace(',','/')+','
    
    content=content[:-1]+'\n'

    with open(constants.CsvFile,write_mode) as file:
        file.write(content)

    with open('Dependencies/student_names.txt','a') as file:
        file.write(student_details[0]+'\n')

    
    with open(constants.ScanLogs,'r') as file:
        data=file.readlines()

    if len(data)==5:
        data[0]=e_no+'\n'
    else:
        data=[0,0,0,0,0]
        data[0]=e_no+'\n'
        data[1]=constants.Batch+str(constants.Range[1])+'\n'
        data[2]=constants.Sem+'\n'
        data[3]=constants.CsvFile+'\n'
        data[4]=constants.GNG

    data=''.join(data)

    with open(constants.ScanLogs,'w') as file:
        file.write(data)
