import codeforces_api
import csv
import time
import requests
from codeforces_api.api_request_maker import CodeforcesApiRequestMaker

#writes the data into filename.csv
def WriteIntoFile(filename,rows): 
    fields = ['Hacker', 'defender', 'Verdict'] 
    with open(filename, 'w',newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile)    
        # writing the fields 
        csvwriter.writerow(fields)  
        # writing the data rows 
        csvwriter.writerows(rows)

#fetches hacking data for a particular User from CF API
def GetDataHacking(UserHandle):
    anonim_cf_api = codeforces_api.CodeforcesApi () # Anonymous access.
    rows=[]
    RatingChange=anonim_cf_api.user_rating(UserHandle)
    for contest in RatingChange: 
        contest_id=contest.contest_id
        try:
            r = anonim_cf_api.contest_hacks(contest_id)
            for j in r: #edge between hacker -> defender
                if(UserHandle in [j.hacker.members[0].handle,j.defender.members[0].handle]):
                    rows.append([j.hacker.members[0].handle,j.defender.members[0].handle,j.verdict])
        except: pass
    WriteIntoFile("Hacks.csv",rows)

#GetDataHacking("vai53")





