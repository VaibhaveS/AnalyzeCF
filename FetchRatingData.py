import codeforces_api
import csv
import time
import networkx as nx
import matplotlib.pyplot as plt
anonim_cf_api = codeforces_api.CodeforcesApi () # Anonymous access.

def GenerateRecentHandles(contest_id):
    contest_standings=anonim_cf_api.contest_standings(contest_id,show_unofficial=True)["rows"]
    handles=[]
    for row in contest_standings:
        handles.append(row.party.members[0].handle)
    return handles

l = GenerateRecentHandles(1593)
print(l)
rows = []
cnt = 0
for str in l:
    if cnt >= 20:
        break
    try:
        ratingChanges = anonim_cf_api.user_rating(str)
        for i in ratingChanges:
            rows.append([str, i.new_rating])
    except:
        continue
    cnt += 1
fields = ['User', 'Rating'] 
with open("Rating.csv", 'w',newline='') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)    
    # writing the fields 
    csvwriter.writerow(fields)  
    # writing the data rows 
    csvwriter.writerows(rows)
