#!/usr/bin/env python
# coding: utf-8

# In[71]:


import json
import re
#https://stackoverflow.com/questions/42148310/convert-string-to-conditional-and-statements
# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()
for i,j in CONDITIONS.items():
    CONDITIONS[i] = j.replace("(","( ")
    CONDITIONS[i] = CONDITIONS[i].replace(")"," )")
    CONDITIONS[i] = CONDITIONS[i].replace(","," , ")
def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """
    
    # TODO: COMPLETE THIS FUNCTION!!!
    requirement = CONDITIONS[target_course]
    #print(requirement)
    A = []
    B = []
    uoc = None
    uoc_req = []
    course_req = []
    #splitting for uoc cases:
    if bool(re.findall('\d+ units.*', CONDITIONS[target_course])):
        req = re.split('(\d+ units)',CONDITIONS[target_course])
        requirement = req[0]
        uoc = int(req[1].strip(' units'))
        uoc_req = req[2]
    for i in requirement.split():
        if i in courses_list:
            A.append('True')
        #if i not in course_list #and in format of 4letters+4number: False
        elif i.lower() =='or' or i.lower() =='and':
            A.append(i.lower())
        elif re.match('[A-Z]{4}[0-9]{4}',i):
            A.append('False')
        elif i=='(' or i==')':
            A.append(i)
        elif re.match('\d',i):
            uoc = int(i)
        else: 
            pass
    if len(uoc_req)!=0:
        if bool(re.findall('level \d+ [A-Z]{4}', uoc_req)):
            level_req = re.search('level \d+ [A-Z]{4}', uoc_req)
            prereq = level_req.group()
            prereq = prereq.split()
            level = prereq[1]
            course = prereq[2]
            course_req = course + level
        else:
            for w in uoc_req.split():
                if w in courses_list:
                    B.append('True')
                elif re.match('[A-Z]{4}[0-9]{4}',w):
                    B.append('False')
    #empty
    if len(A)==0 and uoc == None:
        return True
    elif len(courses_list) == 0 and len(A)!=0:
        return False
    #no uoc
    elif uoc == None and len(A)>0:
        con = ' '.join(A)
        return eval(con)
    #annoying uoc
    else:
        con = ' '.join(A)
        complete = 0
        #simpleuoc
        if len(A)==0 and len(B)==0:
            complete = 0
            for i in courses_list:
                complete +=6
            if uoc <=complete:
                return True
            else: 
                return False
        for i in B:
            if i=='True':
                complete +=6
        if len(course_req)!=0:
            for i in courses_list:
                if course_req in i:
                    complete +=6
        if uoc <= complete:
            B = 'True'
        else: 
            B = 'False'
        con += ' '
        con += B
        return eval(con)

