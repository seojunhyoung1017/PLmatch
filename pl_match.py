#!/usr/bin/env python
# coding: utf-8

import argparse
import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--source", choices=["remote", "local"], required=True, type=str, help="An Option to choose!")
parser.add_argument("--grade", required=False, action='store_true')
args = parser.parse_args()
source = args.source
grade = args.grade

#When source is remote
def remote(grade = grade):
#Calling basic info of team and the stadium
    url = f'https://en.wikipedia.org/wiki/2020-21_Premier_League'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,'html.parser')
    table = soup.find('table',{'class':'wikitable'})
    hometeam = list()
    for row in table.find_all('tr'):
        release = dict()
        cols = row.find_all('td')
        if len(cols) == 0 :
            continue
        release['team_name'] = cols[0].text.strip()
        release['stadium'] = cols[2].text.strip()
        hometeam.append(release)

# I added this data manually since it is not included in webpage
    relagated_team1 = dict()
    relagated_team2 = dict()
    relagated_team3 = dict()
    relagated_team1['team_name'] = 'Watford'
    relagated_team1['stadium'] = 'Vicarage Road'
    hometeam.append(relagated_team1)
    relagated_team2['team_name'] = 'Norwich City'
    relagated_team2['stadium'] = 'Carrow Road'
    hometeam.append(relagated_team2)
    relagated_team3['team_name'] = 'AFC Bournemouth'
    relagated_team3['stadium'] = 'Dean Court'
    hometeam.append(relagated_team3)

# web-scraping, match info
    if grade == True:
        year = 2020
        month = 11
    else:
        year = 2019
        month = 12
    match = []
    while True:
        month_conv = str(month).zfill(2)
        url = f'https://www.bbc.com/sport/football/premier-league/scores-fixtures/{year}-{month_conv}'
        if resp.status_code != 200:
            break
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text,'html.parser')
        blocks = soup.find_all('div', {'class':'qa-match-block'})
        for block in blocks:
            team_list=[]
            home_score=[]
            away_score=[]
            release={}
            release['match_date'] = str(year),block.h3.text
            for team in block.find_all('span', {'class' :'gs-u-display-none gs-u-display-block@m qa-full-team-name sp-c-fixture__team-name-trunc'}):
                team_list.append(team.text)
            for row in block.find_all('span', {'class':'sp-c-fixture__number sp-c-fixture__number--home sp-c-fixture__number--ft'}):
                home_score.append(row.text)
            for row in block.find_all('span',{'class':'sp-c-fixture__number sp-c-fixture__number--away sp-c-fixture__number--ft'}):
                away_score.append(row.text)
            if home_score == []:
                break
            release['team_list'] = team_list
            release['home_score'] = home_score
            release['away_score'] = away_score
            match.append(release)
        month += 1
        if month == 13 :
            year += 1
            month = 1     

#Data-cleaning
    rst=[]
    for a in match:
        year = a['match_date'][0]
        month = datetime.datetime.strptime(a['match_date'][1].split()[2],'%B').month
        day = a['match_date'][1].split()[1]
        day = re.sub("\D", "", day)
        b = len(a['home_score'])
        for i in range(b):
            match_data={}
            match_data['match_date'] = f'{year}/{month}/{day}'
            match_data['home_team'] = a['team_list'][i*2]
            match_data['total_goals'] = int(a['home_score'][i]) + int(a['away_score'][i])
            rst.append(match_data)  

#Web-scraped dataframe
    match_dtfr = pd.DataFrame.from_records(rst)
    if grade == True:
        match_dtfr.to_csv('match_data_grade.csv')
    else:
        match_dtfr.to_csv('match_data.csv')

#Stadium lat/ long (geocoding)
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    key = 'APIKEY'
    for a in hometeam:
        adrs = a['stadium']
        get_params = {'address' : adrs, 'key' : key}
        rsp = requests.get(url, params = get_params)
        a['lat/long'] = rsp.json()['results'][0]['geometry']['location']['lat'], rsp.json()['results'][0]['geometry']['location']['lng']
    geo_dtfr = pd.DataFrame.from_records(hometeam)
    if grade == True:
        geo_dtfr.to_csv('geocode_data_grade.csv')
    else:
        geo_dtfr.to_csv('geocode_data.csv')

#Data-integration : match data + geolocation
    def ltlngdetect(team_name):
        for a in hometeam:
            if a['team_name'] == team_name:
                return a['lat/long']
    for a in rst:
        a['lat/long'] = ltlngdetect(a['home_team'])

#weather API
    url = f'https://www.metaweather.com/api/location/search'
    weat_rst=[]
    for a in rst:
        release={}
        lattlong = str(a['lat/long'][0])+','+ str(a['lat/long'][1])
        params = {'lattlong':lattlong}
        rsp = requests.get(url, params = params)
        woeid = rsp.json()[0]['woeid']
        dte = a['match_date']
        new_url = f'https://www.metaweather.com/api/location/{woeid}/{dte}'
        rsp = requests.get(new_url)
        release['lat/long'] = lattlong
        release['woeid'] = woeid
        release['date'] = dte
        release['weather'] = rsp.json()[0]['weather_state_name']
        weat_rst.append(release)
    weather_dtfr = pd.DataFrame.from_records(weat_rst)
    if grade == True:
        weather_dtfr.to_csv('weather_data_grade.csv')
    else:
        weather_dtfr.to_csv('weather_data.csv')

#Final data (This needs only number of goals and weather)
    fn_dt = [weather_dtfr['weather'], match_dtfr['total_goals']]
    final_dtfr = pd.concat(fn_dt, axis=1)
    if grade == True:
        final_dtfr.to_csv('final_data_grade.csv')
    else:
        final_dtfr.to_csv('final_data.csv')

#When source is local
def local(grade=grade):
    if grade == True:
        match_dtfr = pd.read_csv('match_data_grade.csv')
        geo_dtfr = pd.read_csv('geocode_data_grade.csv')
        weather_dtfr = pd.read_csv('weather_data_grade.csv')
    else :
        match_dtfr = pd.read_csv('match_data.csv')
        geo_dtfr = pd.read_csv('geocode_data.csv')
        weather_dtfr = pd.read_csv('weather_data.csv')
    fn_dt = [weather_dtfr['weather'], match_dtfr['total_goals']]
    final_dtfr = pd.concat(fn_dt, axis=1)
    if grade == True:
        final_dtfr.to_csv('final_data_grade.csv')
    else:
        final_dtfr.to_csv('final_data.csv')

if source == "remote":
    remote()
if source == 'local':
    local()
