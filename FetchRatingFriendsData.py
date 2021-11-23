import codeforces_api
import csv
import time
import requests
from codeforces_api.api_request_maker import CodeforcesApiRequestMaker

anonim_cf_api = codeforces_api.CodeforcesApi () # Anonymous access.
#writes the data into filename.csv
def WriteIntoFile(filename,rows): 
    fields = ['Handle','Friends'] 
    with open(filename, 'w',newline='') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile)    
        # writing the fields 
        csvwriter.writerow(fields)  
        # writing the data rows 
        csvwriter.writerows(rows)

#returns the list of handles from a contest
def GenerateRecentHandles(contest_id):
    contest_standings=anonim_cf_api.contest_standings(contest_id,show_unofficial=True)["rows"]
    handles=[]
    for row in contest_standings:
        handles.append(row.party.members[0].handle)
    return handles

#fetches hacking data for a particular User from CF API
def GetRatingFriends():
    rows=[]
    j=1
    for UserHandle in GenerateRecentHandles(1475):  #took handles from the most participated contest in history of codeforces as of 11/21
        if(j>3000): break
        j+=1
        if(len(UserHandle)<3):
            continue
        time.sleep(2)
        information=anonim_cf_api.user_info([UserHandle])[0]
        rows.append([information.rating,information.friend_of_count]) #handle,friends
    WriteIntoFile("friends.csv",rows)

GetRatingFriends()