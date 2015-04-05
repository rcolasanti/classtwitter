#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2015  <cardiff.colasanti@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
#  

import tweepy
import json
import datetime
import time
import sys

#from ScrolledText import *
from tkinter import *
import tkinter.scrolledtext as tkst
from tkinter import filedialog
# File contining the twitter keys
from twitterinit import cfg,account
from matplotlib.figure import Figure
#from tkFileDialog   import askopenfilename,asksaveasfile

class TkinterText(Frame):
    def __init__(self, parent):
        # Frame containing a Scrolled text to display tweet and sender 
        Frame.__init__(self, parent)
        self.txt = tkst.ScrolledText(self, undo=True)
        self.txt['font'] = ('arial', '15')
        self.txt.tag_configure('bold_italics', font=('Arial', 18, 'italic'))
        self.txt.tag_configure('big', foreground='gray',font=('Arial', 18,'bold'))
        self.txt.tag_configure('small', foreground='gray',font=('Arial', 10,))
        self.txt.tag_configure('color', foreground='blue', font=('Arial', 18, 'bold'))
        self.txt.pack(expand=True, fill='both')
            
    def add_text(self,text,time):
        self.txt.insert(INSERT,text+"\n\n",'bold_italics')
        self.txt.see(END)
        
    def add_sender(self,name):
        self.txt.insert(INSERT,"From: ",'color')
        self.txt.insert(INSERT,name+"\n",'big')
        self.txt.see(END)
        

class TkTwitter:
    def __init__(self):#,question,results_file):
        self.api = self.get_api(cfg)
        # Dictionay of responces
        self.results = dict()
        self.time_start =datetime.datetime.fromtimestamp(time.mktime(time.localtime()))
        #self.save_file = results_file

        self.window = Tk()
        self.window.resizable(width=FALSE, height=FALSE)
        
        menu = Menu(self.window)
        self.window.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Load Question",command = self.load_question)
        filemenu.add_command(label="Save Tweets",command = self.save_tweets)
        # Question
        self.question_lb1 = Label(self.window, text="Question", font='arial 20 bold', wraplength=900, justify=LEFT)
        self.question_lb1.pack(side=TOP,expand=True, fill='both')
        
        self.f1 = TkinterText(self.window)
        self.f1.pack(side = TOP, padx =20, pady =20)
        
        btn = Button( self.window , text = 'Finish', command = self.save_tweets)
        btn.pack(side = BOTTOM, padx =20, pady =20)
        self. window.mainloop()
                
    def get_api(self,cfg):
        # Connect to Twitter
        auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
        auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
        return tweepy.API(auth)

    def load_question(self):
        # calls the open file dialog box
        name = filedialog.askopenfilename()
        with open(name) as in_file:
            for line in in_file:
                self.question_lb1.configure(text=line)
        self. window.after(2000,self.task)
                


    def save_tweets(self):
        # Seve the responces
        # Open the save dialog box
        out_file = filedialog.asksaveasfile(mode='w')
        for r in self.results:
            out_file.write(self.results[r]+"\n") 
        out_file.close()
        exit(0)
        
    def task(self):
        # Get current tweets from the account
        search_results = self.api.search(account, count=1000)
        for tweet in search_results:
            # Only want to print out the tweets once
            # if the tweet is already in the list it is not printed  out
            if not tweet.id in self.results:
                # Only place tweets that have been sent after the 
                # program has started
                # DEBUG print(tweet.created_at+ datetime.timedelta(hours=1),self.time_start)
                if (tweet.created_at+ datetime.timedelta(hours=1))>self.time_start:
                    self.f1.add_sender(tweet._json['user']['name'])
                    self.f1.add_text(tweet.text[13:],tweet.created_at)
                    # A new tweet is printed and added to a list indexed
                    # by tweet id
                    self.results[tweet.id] = tweet._json['user']['name']+","+tweet.text[13: ]

        self.window.after(10000,self.task)  # Reschedule event in 10 seconds




def main():
    TkTwitter()

    
if __name__ == "__main__":
    main()
