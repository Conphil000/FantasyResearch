# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 21:02:36 2022

@author: Conor
"""
import sys
sys.setrecursionlimit(10000)

import pandas as pd
import random
import string
import pickle

import requests
from bs4 import BeautifulSoup

class PKL:
    def __init__(self,folder):
        self._folder = folder
    def SET(self,obj,name):
        pickle.dump(obj, open(f"{self._folder}//{name}.p",'wb'))
    def GET(self,name):
        return pickle.load(open(f"{self._folder}//{name}.pkl",'rb'))

cxn = PKL('pklSupporting')

def get_soup(url):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
    req = requests.get(url,headers)
    soup = BeautifulSoup(req.content,'html.parser')
    return soup

#row = rows[5]
def grab_href(row):
    try:
        return row.find(href=True)['href']
    except TypeError:
        return None
def grab_a(row):
    try:
        return row.a.contents[0]
    except AttributeError:
        return None
    
def active_players(cxn,refresh = False):
    
    try:
        if refresh:
            raise FileNotFoundError
        players = cxn.GET('ACTIVE_PLAYER_URL')
    except FileNotFoundError:
        players = {}
        for i in [i for i in string.ascii_uppercase]:
            
            url = f'https://www.pro-football-reference.com/players/{i}/'
            rows = get_soup(url).find_all(lambda t: t.name == 'b')
            
            dict_out = {i:j for i,j in zip(map(grab_a,rows),map(grab_href,rows)) if i != None}
            
            players = {**players,**dict_out}
            
        tdf = pd.DataFrame({'players':list(players.keys()),'url':list(players.values())})
        
        cxn.SET(tdf,'ACTIVE_PLAYER_URL')
    return players

players = active_players(cxn)

# def search_player(name):
#     fn = name.split(' ')[0][:2]
#     ln = name.split(' ')[1][:4]
#     str_name = ln+fn+1
#     return \
#         pd.read_html(
#             f"https://www.pro-football-reference.com/players/comeback.cgi?player=AlleJo02"
#         )[0]

# %%
def average_position(name):
    [0]

average_position()

def main():
    pass

bench_depth = {'QB':1,'WR':2,'RB':2,'TE':1,'W-R-T':1,'K':1,'DEF':1,'BN':6,'IR':2}

people_in_draft = 10

def expand_depth(bench_depth):
    return [item for sublist in [bench_depth[i]*[i] for i in bench_depth] for item in sublist]

def random_strategy(bench_depth,seed = 123):
    tl = expand_depth(bench_depth)
    random.seed(seed)
    random.shuffle(tl)
    return tl

def semi_random_strategy_V001(bench_depth,seed = 123,no_kicky = 10):
    n_seed = 0
    while True:
        tl = random_strategy(bench_depth,seed+n_seed)
        if no_kicky > len(tl):
            raise ValueError
        if 'K' in tl[:no_kicky]:
            n_seed += 1
        else:
            break
    return tl
        
semi_random_strategy_V001(bench_depth)
            
len(random_strategy(bench_depth))


# Passing
POINTS_PASS_TD = 4
POINTS_PASS_25_YARDS = 1
POINTS_PASS_2PT_CONVERSION = 2
POINTS_PASS_INTERCEPTED = -2

# Rushing
POINTS_RUSH_TD = 6
POINTS_RUSH_10_YARDS = 1
POINTS_RUSH_2PT_CONVERSION = 2

# Receiving
POINTS_RECEIVE_TD = 6
POINTS_RECEIVE_10_YARDS = 1
POINTS_RECEIVE_2PT_CONVERSION = 2

# Misc. Offense
POINTS_KICKOFF_RETURN_TD = 6
POINTS_PUNT_RETURN_TD = 6
POINTS_FUMBLE_RECOVERED = 6
POINTS_FUMBLE_LOST = -2

# %% Strategy

# This needs to beat the auto draft for most too.

if __name__ == '__main__':
    pass
    