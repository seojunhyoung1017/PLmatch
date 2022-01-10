# PLmatch
Regression analysis between weather and scores in PL matches

The three data sets that will be used in this project are as follows:
	The first data set is the Premier League (Football league, England) result data and the URL is 
https://www.bbc.com/sport/football/premier-league/scores-fixtures/2020-10. By changing the key for the 
date on the far right, the result data of the PL games up to November 2019 can be scrapped. (example of 
URL : https://www.bbc.com/sport/football/premier-league/scores-fixtures/{year}-{month}) This is the 
data provided by the BBC sport, which allows the date of the match, teams that played the match, and the 
score of the match to be scrapped. 

	The second data set is climate data, which includes the weather and temperature of the global 
region over time, and the URL is https://www.metaweather.com/api./ This API delivers JSON over 
HTTPS for access to climate data. By using /api/location/search/?lattlong=(latt),(long) URL, it is 
possible to get a special code number in the area called (woeid) as a result by entering the latitude and 
longitude of a specific region. Then, by using /api/location/(woeid)/(date) URL, entering (woeid) and date 
will provide data about maximum temperature, minimum temperature, weather status, wind speed, etc. 
MetaWeather is an open API that provides reliable JSON responses according to the query.

	The third data set is geospatial data, which includes the latitude and longitude of the global region, 
and the URL is https://maps.googleapis.com/maps/api/. This is the open API of Google Maps, and by 
entering the human-readable address through geocoding, the latitude and longitude of that address can be 
obtained. For example, by using /api/geocode/json?address=Old Trafford&Key=API_KEY URL, we can 
obtain the latitude and longitude of Old Trafford, which is the home of Manchester United. This API 
makes it easy to obtain geospatial data for the target region.

	The first data set provides the home team (I will extract home stadium data via URL as below), 
date of the match, and scores, and it can be combined with the third data set to extract the latitude and 
longitude of the match playing area. Furthermore, this result can be combined with the second dataset to 
obtain climate data at the date of the match in home stadium latitude and longitude. To be specific, firstly, 
the date of the game and home stadium information will be scrapped from the PL match dataset. Secondly, 
the latitude and longitude of the home stadium will be extracted by Google Maps open API. Lastly, the 
weather at the match time will be obtained by entering latitude, longitude, and match date through 
MetaWeather API.
(Home stadiums of PL teams URL : https://en.wikipedia.org/wiki/List_of_Premier_League_stadiums)

	I would like to investigate the correlation between the number of goals in the football match and 
the weather in the end as I proceed with this project. Merging the three datasets will show the number of 
goals scored in all matches from November 2019, and the weather at that time can be classified into three 
categories: clear, cloudy, and rainy. Through the data on the number of scores in the classified three 
groups, the paired samples t-test will be conducted to examine the correlation between the number of 
scores and the weather. As a football fan, I always felt that I could not see many goals in the match when 
it rained, and I am glad that I can look into whether this really matters.

  How to run pl_match.py file?
When operating this program through cmd, the source should be determined as local or remote.
For example) python pl_match.py --source remote or --source local
Activating the grade flag will save the program running time to operate various APIs, bringing in only one month of November 2020 of Premier League game data for the convenience of graders. :)
For example) python JUNHYOUNG_SEO_proj2.py --source remote --grade or --source local --grade
This will store data marked as _grade.csv, and also in local source, it will call up data labeled _grade.csv and generate the final_data_grade.csv.
If you do not invoke the grade flag, program will scrape all of match data in bbcsports.com, which is data for a year.
And it takes a lot of time to accept data via weather API, in my experience, it took me about 20minutes. 
