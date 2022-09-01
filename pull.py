# -*- encoding: utf-8 -*-
'''
@File    :   pull.py   
@Contact :   1091756452@qq.com
@License :   (C)Copyright 2022-2024
 
@Desciption: 

@Author: oszn(y.liu)
@Modify Time    
------------ 
2022/9/1 10:11       
'''
# coding=<encoding name> ： # coding=utf-8

import requests
import json
import datetime

def write(path):
    f=open(path,"a+")
    json_txt=get()
    date=get_date()
    txt=f"[{json_txt['questionFrontendId']}.{json_txt['translatedTitle']}]" \
        f"({json_txt['url']}){json_txt['difficulty']}"
    f.write(date+" "+txt)
    f.close()

def get_date():
    today=datetime.date.today()
    return f"[{today.month}-{today.day}](./{today.year}/{today.month}/{today.day}.md)"
def get():
    base_url = 'https://leetcode-cn.com'
    # 获取今日每日一题的题名(英文)
    response = requests.post(base_url + "/graphql", json={
        "operationName": "questionOfToday",
        "variables": {},
        "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug     __typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"
    })
    leetcodeTitle = json.loads(response.text).get('data').get('todayRecord')[0].get("question").get('questionTitleSlug')

    # 获取今日每日一题的所有信息
    url = base_url + "/problems/" + leetcodeTitle
    response = requests.post(base_url + "/graphql",
                             json={"operationName": "questionData", "variables": {"titleSlug": leetcodeTitle},
                                   "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) {    questionId    questionFrontendId    boundTopicId    title    titleSlug    content    translatedTitle    translatedContent    isPaidOnly    difficulty    likes    dislikes    isLiked    similarQuestions    contributors {      username      profileUrl      avatarUrl      __typename    }    langToValidPlayground    topicTags {      name      slug      translatedName      __typename    }    companyTagStats    codeSnippets {      lang      langSlug      code      __typename    }    stats    hints    solution {      id      canSeeDetail      __typename    }    status    sampleTestCase    metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    envInfo    book {      id      bookName      pressName      source      shortDescription      fullDescription      bookImgUrl      pressImgUrl      productUrl      __typename    }    isSubscribed    isDailyQuestion    dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"})
    # 转化成json格式
    jsonText = json.loads(response.text).get('data').get("question")
    # print(jsonText)
    # 题目题号
    no = jsonText.get('questionFrontendId')
    # 题名（中文）
    leetcodeTitleCn = jsonText.get('translatedTitle')
    # 题目难度级别
    level = jsonText.get('difficulty')
    # 题目内容
    context = jsonText.get('translatedContent')
    return {"questionFrontendId":no,"translatedTitle":leetcodeTitle,"difficulty":level,"url":url}

if __name__ == '__main__':
    write("./index.html")
