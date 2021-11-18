import codeforces_api
import csv
import time
import requests
from codeforces_api.api_request_maker import CodeforcesApiRequestMaker

anonim_cf_api = codeforces_api.CodeforcesApi () # Anonymous access.

fields = ['geometry', 'divide and conquer', 'interactive', 'bitmasks', 'string suffix structures', 'dp', 'hashing', 'brute force', 'binary search', 'number theory', 'graphs', 'dfs and similar', 'combinatorics', 'expression parsing', 'fft', 'schedules', 'trees', 'implementation', '2-sat', 'chinese remainder theorem', 'matrices', 'strings', 'meet-in-the-middle', 'shortest paths', 'ternary search', '*special', 'sortings', 'probabilities', 'data structures', 'graph matchings', 'games', 'flows', 'greedy', 'constructive algorithms', 'dsu', 'math', 'two pointers'] 

#writes the data into filename.csv
def WriteIntoFile(filename,rows):
    fields.insert(0,"Handle")
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
        if(j>1000): break
        j+=1
        if(len(UserHandle)<3):
            continue
        time.sleep(1)
        d=dict()
        for column in fields: d[column]=0
        submissions=anonim_cf_api.user_status(UserHandle)
        for submission in submissions:
            if(submission.verdict=="OK"):
                tags=submission.problem.tags 
                rating=submission.problem.rating
                for tag in tags:
                    if(rating!=None):
                        d[tag]+=rating
                    else: d[tag]+=1000
        row=[UserHandle]
        for column in fields: row.append(d[column])
        rows.append(row)
        
    WriteIntoFile("problems.csv",rows)

GetRatingFriends()
