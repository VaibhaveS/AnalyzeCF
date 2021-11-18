import codeforces_api
import csv
import time
import requests
from codeforces_api.api_request_maker import CodeforcesApiRequestMaker

#writes the data into filename.csv
def WriteIntoFile(filename,rows): 
    fields = ['Handle','Total_Submissions', 'Accepted', 'Hacked','Other'] 
    with open(filename, 'w',newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile)    
        # writing the fields 
        csvwriter.writerow(fields)  
        # writing the data rows 
        csvwriter.writerows(rows)

#fetches hacking data for a particular User from CF API
def GetDataHacking(UserHandle):
    if(len(UserHandle)<3):
        return 0
    anonim_cf_api = codeforces_api.CodeforcesApi () # Anonymous access.
    rows=[UserHandle,0,0,0,0] #handle,total,accepted,hacks,others
    Submissions=anonim_cf_api.user_status(UserHandle)
    for Submission in Submissions:
        verdict=Submission.verdict 
        if(verdict=='CHALLENGED'):
            rows[3]+=1
        elif(verdict=='OK'):
            rows[2]+=1
        else:
            rows[4]+=1 
    rows[1]+=len(Submissions)
    WriteIntoFile("Submissions.csv",[rows])

GetDataHacking("vai53")
