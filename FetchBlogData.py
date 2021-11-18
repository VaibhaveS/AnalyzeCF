import codeforces_api
import csv
import time
import networkx as nx
import matplotlib.pyplot as plt
anonim_cf_api = codeforces_api.CodeforcesApi () # Anonymous access.
graph = {}
cnt = 0
auth = anonim_cf_api.blog_entry_view(89227).author_handle
blogCount = {}
rating = {}
totalNoOfComments = {}
BlogIdAuthor = {}
BlogIdnoOfComments = {}
comments = []
for blog_id in range(89227, 89228):
    time.sleep(2)
    author=str(anonim_cf_api.blog_entry_view(blog_id).author_handle)
    BlogIdAuthor[blog_id] = author
    if(author in blogCount):
        blogCount[author] += 1
    else:
        blogCount[author] = 1
    rati =  anonim_cf_api.user_info([author])
    rating[author] = rati[0].rating
    commentsList = anonim_cf_api.blog_entry_comments(blog_id) #list of commented objects
    BlogIdnoOfComments[blog_id] = len(commentsList)
    if(author in totalNoOfComments):
        totalNoOfComments[author] += len(commentsList)
    else:
        totalNoOfComments[author] = len(commentsList)
    i=0
    for j in commentsList:
        if(i>15):
            break
        i+=1
        comments.append(j.commentator_handle);
    graph[author] = comments;
    cnt += 1
for users in comments:
    if(users != auth):
        try:
            blogEntries = list(anonim_cf_api.user_blog_entries(users));
            blogId = []
            if(len(blogEntries) > 0):
                if(users in blogCount):
                    blogCount[users] += len(blogEntries)
                else:
                    blogCount[users] = len(blogEntries)
                if users not in rating:
                    rati = anonim_cf_api.user_info([users])
                    rating[users] = rati[0].rating
            for j in range(min(len(blogEntries),100)):
                time.sleep(2)
                l = list(anonim_cf_api.blog_entry_comments(blogEntries[j].id))
                BlogIdAuthor[blogEntries[j].id] = users
                BlogIdnoOfComments[blogEntries[j].id] = len(l)
                if(users in totalNoOfComments):
                    totalNoOfComments[users] += len(l)
                else:
                    totalNoOfComments[users] = len(l)
                temp = []
                for k in range(min(len(l), 100)):
                    temp.append(l[k].commentator_handle);
        except:
            continue
"""rows = []
Keys = list(blogCount.keys())
for entry in Keys:
    try:
        rows.append([entry, rating[entry], blogCount[entry], totalNoOfComments[entry]])
    except:
        continue
print(rows)"""
"""fields = ['Author', 'Rating', 'BlogCount', 'Total_no_of_comments'] 
with open("Blogs.csv", 'w',newline='') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)    
    # writing the fields 
    csvwriter.writerow(fields)  
    # writing the data rows 
    csvwriter.writerows(rows)"""
Keys1 = list(BlogIdAuthor.keys())
rows = []
for entry in Keys1:
    try:
        rows.append([entry, BlogIdAuthor[entry], BlogIdnoOfComments[entry]])
    except:
        continue
print(rows)
fields = ['BlogId', 'Author', 'No_of_comments'] 
with open("BlogId.csv", 'w',newline='') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)    
    # writing the fields 
    csvwriter.writerow(fields)  
    # writing the data rows 
    csvwriter.writerows(rows)

