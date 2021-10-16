use `rightmove`;

# COUNT THE NUMBER OF PROPERTIES
SELECT COUNT(*) FROM `buckinghamshire`;

# 203 estate agents (RMV implies 224, so some not included)
SELECT COUNT(DISTINCT `branchId`) FROM `buckinghamshire`;

# Connells is the most popualr estate agent with 534 properties
SELECT `companyName`, COUNT(`propertyId`) FROM `buckinghamshire`
GROUP BY `companyName`
ORDER BY COUNT(`propertyId`) DESC;