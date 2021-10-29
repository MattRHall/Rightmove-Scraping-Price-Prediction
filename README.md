# Rightmove Web Scraper

## Overview
Web scraping was used to extract information from Rightmove about properties for sale (and sold subject to contract) in Buckinghamshire. Although Buckinghamshire was chosen, the web scraper can easily be modified for other counties. This information was stored in a MySQL database, which means it can scale easily. Analysis was then performed on estate agents and property prices.

## Purpose
The purpose of this project was to see how web scraped data can automatically be stored, and subsequently queried in an SQL database. I was also curious whether you could predict house prices from the basic features of the property. Although not studied in this project, enhanced features could also be collected from the property description to aid in property price forecasting.

## Estate Agent Analysis
The largest estate agent companies in Buckinghamshire are shown below. Note, some estate agents have multiple subsidiaries e.g. Connells and Sequence (UK) - Connells. Connells, Michael Graham, Frosts, LSL and Countrywide all have high shares as you would expect. Purplebricks only has c. 2.4% share (so not really threatening the estate agents in Buckinghamshire).
![Largest Market Share](images\largestmarketshare.png)

The average property price per estate agent is shown below. There are 5-6 estate agents that stand out as catering to extremely expensive properties before a tapering off. Not a surprise to see Bovingdons and Knight Frank at the top.
![Average Price](images\averageprice.png)

The chart below shows the average age of unsold properties for an estate agent, if that estate agent has more than 10 properties unsold. These are questionably the worst agents at shifting properties (maybe they have unrealistic prices). The worst estates can have average ages of properties well over a year. Naturally it could also indicate estate agents which are struggling to find fresh supply of properties (to be come younger unsold prooperties).
![Time unsold](images\timeunsold.png)


## Property Price Forecasting
















