use `rightmove`;

# COUNT THE NUMBER OF PROPERTIES
SELECT COUNT(*) FROM `buckinghamshire`;

# 203 estate agents (RMV implies 224, so some not included)
SELECT COUNT(DISTINCT `branchId`) FROM `buckinghamshire`;

# Connells is the most popualr estate agent with 534 properties
SELECT `companyName`, COUNT(`propertyId`) FROM `buckinghamshire`
GROUP BY `companyName`
ORDER BY COUNT(`propertyId`) DESC;

# Market share as  % of total
WITH `grouped` AS (
	SELECT `companyName`, COUNT(`propertyId`) as `total_properties`
    FROM `buckinghamshire`
    GROUP BY `companyName`)
SELECT `companyName`, `total_properties` / (SELECT COUNT(`propertyId`) FROM `buckinghamshire`) FROM `grouped`
	ORDER BY `total_properties` / (SELECT COUNT(`propertyId`) FROM `buckinghamshire`) DESC;

# ESTATE AGENT AVERAGE PROPERTY PRICE
SELECT `companyName`, ROUND(AVG(`price`),2) as `average` FROM `buckinghamshire`
GROUP BY `companyName`
ORDER BY `average` DESC
LIMIT 20;
    
# Estate Agent Branches with the Most STC properties
SELECT `branchId`, `companyName`, `branchName`, COUNT(`propertyId`) FROM `buckinghamshire`
WHERE `soldSTC` = 1 
GROUP BY `branchId`;
   
# PURPLEBRICK MARKET SHARE
SET @v1 := (SELECT COUNT(*) FROM `buckinghamshire`);
SELECT `companyName`, COUNT(`propertyId`)/@v1 FROM `buckinghamshire`
WHERE `companyName` = 'purplebricks';

SELECT `companyName`, COUNT(`propertyId`) FROM `buckinghamshire`
WHERE `companyName` = 'purplebricks';

SELECT COUNT(*) FROM `buckinghamshire`;
   
# LONGEST TIME TO SELL
SELECT * FROM `buckinghamshire`;
   
#SELECT `propertyId`, DATEDIFF(CONVERT(added, DATE), '27-10-21') FROM `buckinghamshire`;

SELECT `propertyId`, DATEDIFF(added, NOW()) FROM `buckinghamshire`
WHERE `soldSTC` = 0;

SELECT `propertyId`, DATEDIFF(added, '20211020') FROM `buckinghamshire`
WHERE `soldSTC` = 0;

SELECT *, CONVERT(added, DATE), DATEDIFF(added, '20211020') FROM `buckinghamshire`;




