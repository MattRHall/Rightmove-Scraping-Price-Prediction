# Rightmove Web Scraper

## Overview
Web scraping was used to extract information from Rightmove about properties for sale (and sold subject to contract) in Buckinghamshire. Although Buckinghamshire was chosen, the web scraper can easily be modified for other counties. This information was stored in a MySQL database, which means it can scale easily. Analysis was then performed on estate agents and property prices.

## Purpose
The purpose of this project was to see how web scraped data can automatically be stored, and subsequently queried in an SQL database. I was also curious whether you could predict house prices from the basic features of the property. Although not studied in this project, enhanced features could also be collected from the property description to aid in property price forecasting.

## Estate Agent Analysis
The largest estate agent companies in Buckinghamshire are shown below. Note, some estate agents have multiple subsidiaries e.g. Connells and Sequence (UK) - Connells. Connells, Michael Graham, Frosts, LSL and Countrywide all have high shares as you would expect. Purplebricks only has c. 2.4% share (so not really threatening the estate agents in Buckinghamshire).
![Largest Market Share](https://github.com/MattRHall/Rightmove-Scraping-Price-Prediction/blob/master/images/largestmarketshare.png)

The average property price per estate agent is shown below. There are 5-6 estate agents that stand out as catering to extremely expensive properties before a tapering off. Not a surprise to see Bovingdons and Knight Frank at the top.
![Average Price](https://github.com/MattRHall/Rightmove-Scraping-Price-Prediction/blob/master/images/averageprice.png)

The chart below shows the average age of unsold properties for an estate agent, if that estate agent has more than 10 properties unsold. These are questionably the worst agents at shifting properties (maybe they have unrealistic prices). The worst estates can have average ages of properties well over a year. Naturally it could also indicate estate agents which are struggling to find fresh supply of properties (to be come younger unsold prooperties).
![Time unsold](https://github.com/MattRHall/Rightmove-Scraping-Price-Prediction/blob/master/images/timeunsold.png)


## Property Price Forecasting
The features below were used to predict property prices in buckinghamshire. Categorical encoding was applied to the SubPropertyType feature (number of categories was reduced). Logarithmic transformation was applied to the property prices to make their distribution more normal.

- preOwned: 'New Home' or 'Resale'.
- beds: Number of properties in property.
- bathrooms: Number of bathrooms in property.
- closest train: Distance to closest train station.
- garage: 0 = no garage, 1 = garage.
- garden: 0 = no garden, 1 = garden.
- parking: 0 = no parking, 1 = parking.
- pool: 0 = no pool, 1 = pool.
- type_Bungalow: 0 = not bungalow, 1 = bungalow.
- type_Detached: 0 = not detached, 1 = detached.
- type_End-of-Terrace: 0 = not end-of-terrance, 1 = end-of-terrace.
- type_Flat: 0 = not flat, 1 = flat.
- type_Garage: 0 = no Garage, 1 = Garage.
- type_Land: 0 = not land plot, 1 = land plot.
- type_Mobile-Home: 0 = not mobile-home, 1 = mobile-home.
- type_Retirement: 0 = not retirement, 1 = retirement.
- type_Semi-Detached: 0 = not semi-detached, 1 = semi-detached.
- type_Terraced: 0 = not terraced, 1 = terraced.

The results of the **multiple linear regression** were interesting, although an R-Squared of 0.62 indicates moderate model accuracy. Most of the relationships between the dependent and independent variable were as expected. Houses with more bedrooms, more bathrooms, a garden, a pool, and detached were predicted to be more expensive. Houses which were retirement properties, mobile homes, terraced or semi-detached were predicted to be cheaper. Properties classified as a Garage saw a 85% reduction in property price prediction, which also makes sense. Properties with a pool had a 53% uplift in property price prediction.

Interestingly, every mile a property moves away from a train station, the predicted property value decreases by 4%. The closest train station feature is more than just transport, it is a proxy for urban vs. rural properties. 

One odd feature was 'parking'. Adding a 'parking' to a property decreased the predicted property value by 4.5%. The other odd feature was'preOwned', with second hand properties having a 23% premium. I suspect it is because new build properties tend to be smaller.

The true vs. predicted values (log prices) are shown below.
![Time unsold](https://github.com/MattRHall/Rightmove-Scraping-Price-Prediction/blob/master/images/regressionresults.png)

In addition to multiple linear regression, a **GradientBoosting** model was trained which achieved a R-squared of 0.73. When we relax the assumption of linearity, we can achieve greater performance.

## Extra Work
It might be possible to use the textual description of a property to extra information about the property. For example, words like 'modernization' are good ways to identify the state of a property.




























