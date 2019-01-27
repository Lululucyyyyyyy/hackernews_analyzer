import requests
import os
import csv
import time
import pprint

x = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
y = os.path.realpath('/Users/wenmo/Development/polyglot/cohort-1/data/goodwords.txt')
z = os.path.realpath('/Users/wenmo/Development/polyglot/cohort-1/data/badwords.txt')

tweets = set()
goodwords = set()
badwords = set()

#create sets for words
def wordlists(path, set):
    with open(path, "r") as g:
        line = g.readlines()[35:]
        for word in line:
            words = word.split(',')
            for i in words:
                temp = i
                temp = temp.strip(' ')
                temp = temp.strip('\n')
                set.add(temp)

def display(set):
    for word in set:
        #print (word)
        pass

wordlists(y, goodwords)
wordlists(z, badwords)

class TweetAnalyzer:
    def __init__(self, goodwords_list, badwords_list):
        self.goodwords = goodwords_list
        self.badwords = badwords_list

    def get_stories(self):
        new_response = requests.get(x)
        top_five_ids = new_response.json()[:10]

        story2 = []
        for top_id in top_five_ids:
            curr_story_api_url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(top_id)
            curr_story = requests.get(curr_story_api_url).json()
            story2.append(curr_story)
        return story2

    def get_comments(self, story2):
        story2 = self.get_stories()
        comments = {}   
        for story in story2:
            if 'kids' in story:
                comment_ids = story['kids'][:10]
                title = story['title']
                comments[title] = [] 
                for comment_id in comment_ids:
                    curr_id = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(comment_id)
                    curr_comment_obj = requests.get(curr_id).json()
                    if 'text' in curr_comment_obj:
                        curr_comment = curr_comment_obj['text']
                        comments[title].append(curr_comment)
        return comments
    
    def analyze_all_comments(self):
        print('analyzing comments')
        story2 = self.get_stories()
        comments = self.get_comments(story2)
        for comment in comments:
            gnum = 0
            bnum = 0
            total = 0
            for words in comment:
                words = comment.lower().split()
                for word in words:
                    if word in self.goodwords:
                        gnum += 1
                    if word in self.badwords:
                        bnum += 1
                    total += 1
            comment_sentiment_pos = gnum / total
            comment_sentiment_neg = bnum / total
            print(comment +  " positive: "+ " {0:.0%}".format(comment_sentiment_pos) + " negative: " + " {0:.0%}".format(comment_sentiment_neg))

    def analyze_comments(self, story):
        #get comments for one story
        entire_one_story = {}
        if 'kids' in story:
            comment_ids = story['kids'][:10]
            title = story['title']
            entire_one_story[title] = []
            comments = {}
            comment_text = {}
            for comment_id in comment_ids:
                comments[comment_id] = {}
                curr_id = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(comment_id)
                curr_comment_obj = requests.get(curr_id).json()
                sentiment = {}
                if 'text' in curr_comment_obj:
                    curr_comment = curr_comment_obj['text']
                    comment_text['text'] = [curr_comment]
                    sentiment['sentiment'] = []
                    for words in curr_comment:
                        words = curr_comment.lower().split()
                        for word in words:
                            total = 0
                            gnum = 0
                            bnum = 0
                            if word in self.goodwords:
                                gnum += 1
                            if word in self.badwords:
                                bnum += 1
                            total += 1
                        if gnum > bnum:
                            sentimentt = 'positive'
                        elif gnum < bnum:
                            sentimentt = 'negative'
                        else:
                            sentimentt = 'neutral'
                    sentiment['sentiment'].append(sentimentt)
                    comments[comment_id].update(comment_text)
                    comments[comment_id].update(sentiment)
           
                entire_one_story[title] = [comments]
                #return entire_one_story
        else:
            pass

        

    def full_dict(self):
        stories_list = self.get_stories()
        my_list = []
        for story in stories_list:
            my_list.append(self.analyze_comments(story))
        #return my_list

if __name__ == "__main__":
    a1 = TweetAnalyzer(goodwords, badwords)
    print(a1.full_dict())





