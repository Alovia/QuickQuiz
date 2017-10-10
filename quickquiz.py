##!/bin/python

import sys
import random
import os
import json
import getopt

class UI(object):

    def __init__(self):
        self.quiz          = False
        self.topic         = ""
        self.section       = ""
        self.randomQ       = False
        self.all_questions = False
        
    def show_help(self):
        print "QuickQuiz is a simple quiz facility that allows you to test yourself."
        print "\nOptions:"
        print "-h --help       Show this help."
        print "-a --all        Show all topics and sections"
        print "-q --quiz       Run a quiz, all questions is the default, otherwise select with:"
        print "-t --topic=     Select topic=<topic>."
        print "-s --section=   Select section=<section>"
        print "-r --random     Select random questions from all available topics."

        
    def commands(self, argv):
        try:
            opts, args = getopt.getopt(argv, "haqt:s:",
                                       ["help","all","topics=", "sections=", "quiz","topic=","section="])
        except getopt.GetoptError:
            self.show_help()
            sys.exit(2)
    
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                self.show_help()
                sys.exit()

            if opt in ("-a", "--all"):
                self.all_questions = True

            if opt in ("-q", "--quiz"):                
                self.quiz = True

            if opt in ("-t", "--topic"):                
                self.topic = arg

            if opt in ("-s", "--section"):                
                self.section = arg

            if opt in ("-r", "--random"):                
                self.randomQ = True
                

def readQuizFile(topic):

    filename = "./questions/"+topic+".JSON"

    try:
        f = open(filename,"r")
    except IOError:
        print "There was an error opening:", filename
        sys.exit()
        
    try:
        questions = json.loads(f.read())['questions']
    except (ValueError, KeyError, TypeError):
        print "JSON format error: maybe a trailing comma?"
        sys.exit()
        
    f.close()

    return questions

def getTopics():
    return [f.replace('.JSON','')
            for f in os.listdir("./questions")
            if f.endswith(".JSON")]
   
def getSections(topic, questions):
    sections = []
    for q in questions:
        if q.get("T") == topic and q.get("S") not in sections:
            sections.append(q.get("S"))
    return list(sections)

def readAll():
    questions = []
    for t in getTopics():
        questions = questions + readQuizFile(t)
    return list(questions)


def countQuestionsInTopic(topic, questions):
    topic_count = 0
    for q in questions:
        if q.get("T") in topic: 
            topic_count += 1
    return topic_count        

def selectQuestionByTopic(topic, questions):
    result = []
    for q in questions:
        if q.get("T") == topic: 
           result.append(q)
    return result   

def selectQuestionByTopicAndSection(topic, section, questions):
    result = []
    for q in questions:
        if q.get("T") == topic and q.get("S") == section: 
           result.append(q)
    return result   


def doQuiz(cmd, questions):

    if cmd.randomQ == True:
        shuffle(questions)
        
    correct = 0
    wrong = 0
    question_count = 0
    question_total = len(questions)
    
    for q in questions:
        question_count += 1
        print "Topic:",      q.get("T")
        print "Section:",    q.get("S")
        print "Question:\n", q.get("Q")
        result = raw_input('Press the <enter> to reveal the answer: >')
        print "Answer:\n", q.get("A")
        result = ""
        while result not in ['w', 'c', 'q']:
            result = raw_input('Press q to quit, C for correct, W for wrong: >')
        if result == 'w':
            wrong += 1
        elif result == 'c':
            correct += 1
        print "Score:  %d questions of a total of %d, %d correct and %d wrong" %(
            question_count, question_total, correct, wrong )
        if result == 'q':
            sys.exit()
            
        
def main(argv):

    cmd = UI()
    cmd.commands(argv)    
    questions = readAll()
    if cmd.all_questions == True:
        topic_list = getTopics()
        print "There are %d topics for a total of %d questions:" % (len(topic_list), len(questions))
        for t in topic_list:
            print t
            section_list = getSections(t, questions)
            for s in section_list:
                print "\t",s
    elif cmd.topic != "":
        if cmd.quiz == False:
            cmd.quiz = True
        topic_list = getTopics()
        if cmd.section != "":
            questions = selectQuestionByTopicAndSection(cmd.topic, cmd.section, questions) 
        else:
            questions = selectQuestionByTopic(cmd.topic, questions) 
            
    if cmd.quiz == True:
        if len(questions) > 0:
            doQuiz(cmd, questions)
        else:
            print "You did not select any questions, typo?"


if __name__ == '__main__':
    main(sys.argv[1:])
