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
#print(l)
cnt = 0
userProblem = dict()
currentRating = dict()
userRatingChange = dict()
rows = []
for str in l:
    print(str, cnt)
    time.sleep(2)
    if cnt >= 100:
        break
    try:
        ratingChanges = anonim_cf_api.user_rating(str)
    except:
        continue
    ratingChanges.reverse()
    if(len(ratingChanges) < 5):
        continue
    currentRating[str] = ratingChanges[0].new_rating
    n = 0
    avgRatingChange = 0
    for i in range(min(5, len(currentRating))):
        avgRatingChange += (ratingChanges[i].new_rating - ratingChanges[i].old_rating)
        n += 1
    avgRatingChange /= n
    userRatingChange[str] = avgRatingChange
    try:
        submission = anonim_cf_api.user_status(str)
    except:
        cnt += 1
        continue
    print("Not except")
    submission.reverse()
    cntr = 0
    ratingAvg = 0
    for i in submission:
        if cntr >= 10:
            break
        problem = i.problem
        #print(problem.rating)
        if problem.rating is not None:
            ratingAvg += problem.rating
            cntr += 1
        #cntr += 1
    ratingAvg /= 10
    userProblem[str] = ratingAvg
    rows.append([str, avgRatingChange, ratingAvg, ratingChanges[0].new_rating])
    cnt += 1
fields = ['User', 'AvgRatingChange', 'AvgProblemRating', 'CurrRating']
with open("Rating_Prediction.csv", 'w',newline='') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)    
    # writing the fields 
    csvwriter.writerow(fields)  
    # writing the data rows 
    csvwriter.writerows(rows)










