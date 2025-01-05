SELECT * FROM Fires WHERE State = "TX" AND STAT_CAUSE_DESCR LIKE "Campfire"	USWildFires
SELECT OWNER_DESCR FROM FIres WHERE State = "OR" AND FIRE_YEAR = 2015 ORDER BY FIRE_SIZE DESC LIMIT 1	USWildFires
SELECT COUNTY FROM Fires WHERE State = "WA" AND FIRE_YEAR = 2012	USWildFires
SELECT count(*) FROM Fires WHERE FIRE_YEAR = 2010 AND STAT_CAUSE_DESCR LIKE "%Arson%"	USWildFires
SELECT count(DISTINCT FIRE_YEAR) FROM Fires	USWildFires
SELECT avg(DISCOVERY_DATE) FROM Fires where FIRE_YEAR BETWEEN 2000 AND 2004	USWildFires
SELECT STAT_CAUSE_CODE FROM Fires GROUP BY STAT_CAUSE_CODE ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT FIRE_YEAR FROM Fires ORDER BY FIRE_SIZE DESC LIMIT 1	USWildFires
SELECT count(*) FROM Fires WHERE OWNER_DESCR = "MISSING/NOT SPECIFIED"	USWildFires
SELECT COUNTY FROM Fires GROUP BY COUNTY ORDER BY count(*)	USWildFires
SELECT count(DISTINCT STAT_CAUSE_DESCR) FROM Fires	USWildFires
SELECT sum(FIRE_SIZE) FROM Fires WHERE State = "NY" and FIRE_YEAR = "2006"	USWildFires
SELECT * FROM Fires WHERE State = "UT" AND FIRE_YEAR = 1997 ORDER BY FIRE_SIZE DESC LIMIT 1	USWildFires
SELECT count(*) FROM Fires WHERE COUNTY = "Gloucester" AND FIRE_SIZE > 10	USWildFires
SELECT State FROM Fires GROUP BY State ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT STAT_CAUSE_DESCR FROM Fires GROUP BY STAT_CAUSE_DESCR ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT OWNER_DESCR FROM Fires GROUP BY OWNER_DESCR ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT count(*) FROM Fires WHERE STAT_CAUSE_DESCR LIKE "%Campfire%" AND FIRE_YEAR = 2014	USWildFires
SELECT sum(FIRE_SIZE) FROM Fires WHERE State = "TX" AND FIRE_YEAR BETWEEN 2000 AND 2010	USWildFires
SELECT State FROM Fires GROUP BY State ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT STAT_CAUSE_DESCR FROM Fires GROUP BY STAT_CAUSE_DESCR ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT sum(FIRE_SIZE) FROM Fires	USWildFires
SELECT sum(FIRE_SIZE) FROM Fires WHERE STATE = "TX" AND FIRE_YEAR BETWEEN 2000 AND 2010  UNION SELECT sum(FIRE_SIZE) FROM Fires WHERE STATE = "TX" AND FIRE_YEAR BETWEEN 1990 AND 2000	USWildFires
SELECT count(*) FROM Fires WHERE OWNER_DESCR = "MISSING/NOT SPECIFIED"	USWildFires
SELECT LATITUDE FROM Fires GROUP BY LATITUDE ORDER BY count(*) DESC LIMIT 1	USWildFires
SELECT CrimeTS FROM GreaterManchesterCrime GROUP BY CrimeTS ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT Outcome FROM GreaterManchesterCrime WHERE Location LIKE "%Street%" GROUP BY Outcome ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT Type FROM GreaterManchesterCrime WHERE LSOA LIKE "%Salford%" GROUP BY Type ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT count(*) FROM GreaterManchesterCrime WHERE Outcome = "Under investigation"	GreaterManchesterCrime
SELECT count(*) FROM GreaterManchesterCrime	GreaterManchesterCrime
SELECT Location FROM GreaterManchesterCrime GROUP BY Location ORDER BY count(*) DESC LIMIT 3	GreaterManchesterCrime
SELECT Type FROM GreaterManchesterCrime WHERE Outcome LIKE "%Investigation complete%" GROUP BY Type ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT count(*) FROM GreaterManchesterCrime WHERE Type LIKE "%Drug%"	GreaterManchesterCrime
SELECT count(*) FROM GreaterManchesterCrime WHERE Outcome LIke "%Under investigation%"	GreaterManchesterCrime
SELECT Location FROM GreaterManchesterCrime WHERE Type LIke "%Drug%" GROUP BY Location ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT Type FROM GreaterManchesterCrime GROUP BY Type ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT Location FROM GreaterManchesterCrime GROUP BY Location ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT Location FROM GreaterManchesterCrime GROUP BY Location ORDER BY count(*) LIMIT 1	GreaterManchesterCrime
SELECT Location FROM GreaterManchesterCrime WHERE Type = "Violence and sexual offences" GROUP BY Location ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT Location FROM GreaterManchesterCrime GROUP BY Location ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT Type FROM GreaterManchesterCrime WHERE Outcome = "Awaiting court outcome" GROUP BY Type ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT Type FROM GreaterManchesterCrime WHERE Outcome = "Investigation complete; no suspect identified" GROUP BY Type ORDER BY count(*) DESC LIMIT 1	GreaterManchesterCrime
SELECT Outcome FROM GreaterManchesterCrime WHERE CrimeID = "6B:E2:54:C6:58:D2"	GreaterManchesterCrime
SELECT T1.school_district FROM FINREV_FED_17 as T1 JOIN FINREV_FED_KEY_17 as T2 ON T1.state_code = T2.state_code WHERE T2.state = "Wisconsin" ORDER BY T1.t_fed_rev DESC LIMIT 1	StudentMathScore
SELECT avg(T1.c14) FROM FINREV_FED_17 as T1 JOIN FINREV_FED_KEY_17 as T2 ON T1.state_code = T2.state_code WHERE T2.state = "Virginia"	StudentMathScore
SELECT T2.state, sum(c14),sum(c25) FROM FINREV_FED_17 as T1 JOIN FINREV_FED_KEY_17 as T2 ON T1.state_code = T2.state_code JOIN NDECoreExcel_Math_Grade8 as T3 ON T2.state = T3.state GROUP BY T2.state ORDER BY T3.average_scale_score DESC LIMIT 10	StudentMathScore
SELECT T1.school_district, max(T1.c14), T3.average_scale_score FROM FINREV_FED_17 as T1 JOIN FINREV_FED_KEY_17 as T2 ON T1.state_code = T2.state_code JOIN NDECoreExcel_Math_Grade8 as T3 ON T2.state = T3.state UNION SELECT T1.school_district, max(T1.c25), T3.average_scale_score FROM FINREV_FED_17 as T1 JOIN FINREV_FED_KEY_17 as T2 ON T1.state_code = T2.state_code JOIN NDECoreExcel_Math_Grade8 as T3 ON T2.state = T3.state	StudentMathScore
SELECT state FROM NDECoreExcel_Math_Grade8 ORDER BY average_scale_score DESC LIMIT 1	StudentMathScore
SELECT T1.school_district, max(T1.t_fed_rev / T3.average_scale_score) FROM FINREV_FED_17 as T1 JOIN FINREV_FED_KEY_17 as T2 on T1.state_code = T2.state_code JOIN NDECoreExcel_Math_Grade8 as T3 ON T2.state = T3.state	StudentMathScore
SELECT T2.state, T3.average_scale_score FROM FINREV_FED_KEY_17 as T2 JOIN FINREV_FED_17 as T1 ON T1.state_code = T2.state_code JOIN NDECoreExcel_Math_Grade8 as T3 ON T2.state = T3.state GROUP BY T2.state ORDER BY sum(T1.t_fed_rev) DESC LIMIT 1	StudentMathScore
SELECT T1.school_district, min(T1.t_fed_rev / T3.average_scale_score) FROM FINREV_FED_17 as T1 JOIN FINREV_FED_KEY_17 as T2 on T1.state_code = T2.state_code JOIN NDECoreExcel_Math_Grade8 as T3 ON T2.state = T3.state	StudentMathScore
SELECT T2.state, T3.average_scale_score FROM FINREV_FED_KEY_17 as T2 JOIN FINREV_FED_17 as T1 ON T1.state_code = T2.state_code JOIN NDECoreExcel_Math_Grade8 as T3 ON T2.state = T3.state GROUP BY T2.state ORDER BY sum(T1.t_fed_rev) LIMIT 1	StudentMathScore
SELECT state FROM NDECoreExcel_Math_Grade8 ORDER BY average_scale_score DESC LIMIT 1	StudentMathScore
SELECT average_scale_score FROM NDECoreExcel_Math_Grade8 WHERE state = "California"	StudentMathScore
SELECT count(DISTINCT school_district) FROM FINREV_FED_17 as T1 JOIN FINREV_FED_KEY_17 as T2 ON T1.state_code = T2.state_code WHERE T2.state = "Indiana"	StudentMathScore
SELECT state_code FROM FINREV_FED_KEY_17 WHERE state = "Virginia"	StudentMathScore
SELECT T2.state FROM FINREV_FED_KEY_17 as T2 JOIN FINREV_FED_17 as T1 ON T1.state_code = T2.state_code GROUP BY T2.state ORDER BY sum(t_fed_rev) DESC LIMIT 1	StudentMathScore
SELECT sum(T1.c14), sum(T1.c25) FROM FINREV_FED_17 as T1 JOIN FINREV_FED_KEY_17 as T2 ON T1.state_code = T2.state_code WHERE T2.state = "Colorado"	StudentMathScore
SELECT t_fed_rev FROM FINREV_FED_17 WHERE school_district LIKE "%Pecatonia Area%"	StudentMathScore
SELECT average_scale_score FROM NDECoreExcel_Math_Grade8 WHERE state = "North Carolina" UNION SELECT average_scale_score FROM NDECoreExcel_Math_Grade8 WHERE state = "South Carolina"	StudentMathScore
SELECT average_scale_score FROM NDECoreExcel_Math_Grade8 WHERE state = "North Carolina" UNION SELECT average_scale_score FROM NDECoreExcel_Math_Grade8 WHERE state = "New York"	StudentMathScore
SELECT count(*) FROM FINREV_FED_17 WHERE c25 > c14	StudentMathScore
SELECT groupName, groupYear FROM torrents	WhatCDHipHop
SELECT groupName, artist FROM torrents	WhatCDHipHop
SELECT DISTINCT tag FROM tags	WhatCDHipHop
SELECT DISTINCT releaseType FROM torrents	WhatCDHipHop
SELECT groupName FROM torrents WHERE groupYear > 2000 ORDER BY totalSnatched DESC LIMIT 5	WhatCDHipHop
SELECT DISTINCT groupName FROM torrents WHERE totalSnatched > 100 AND releaseType = "album"	WhatCDHipHop
SELECT T2.groupName FROM torrents as T2 JOIN tags as T1 ON T1.id = T2.id WHERE T1.tag = "houston" ORDER BY totalSnatched DESC LIMIT 1	WhatCDHipHop
SELECT groupName FROM torrents WHERE artist = "lasean camry" AND totalSnatched = (SELECT max(totalSnatched) FROM torrents WHERE artist = "lasean camry") UNION SELECT groupName FROM torrents WHERE artist = "lasean camry" AND totalSnatched = (SELECT min(totalSnatched) FROM torrents WHERE artist = "lasean camry")	WhatCDHipHop
SELECT groupName FROM torrents WHERE releaseType = "album" ORDER BY totalSnatched DESC LIMIT 10	WhatCDHipHop
SELECT T1.tag FROM torrents as T2 JOIN tags as T1 ON T1.id = T2.id WHERE T2.groupYear >= 2010 GROUP BY T1.tag ORDER BY T2.totalSnatched DESC LIMIT 10	WhatCDHipHop
SELECT groupYear FROM torrents GROUP BY groupYear ORDER BY count(groupName) LIMIT 1	WhatCDHipHop
SELECT groupName FROM torrents ORDER BY totalSnatched DESC LIMIT 1	WhatCDHipHop
SELECT artist FROM torrents WHERE groupYear = 2015 GROUP BY artist ORDER BY totalSnatched DESC LIMIT 1	WhatCDHipHop
SELECT T1.tag, T2.groupName FROM torrents as T2 JOIN tags as T1 ON T1.id = T2.id	WhatCDHipHop
SELECT groupYear FROM torrents GROUP BY groupYear ORDER BY count(groupName) DESC LIMIT 1	WhatCDHipHop
SELECT artist FROM torrents GROUP BY artist ORDER BY count(groupName) DESC LIMIT 1	WhatCDHipHop
SELECT artist FROM torrents GROUP BY artist ORDER BY avg(totalSnatched) DESC LIMIT 1	WhatCDHipHop
SELECT groupYear FROM torrents GROUP BY groupYear ORDER BY count(groupName) DESC LIMIT 1	WhatCDHipHop
SELECT groupName FROM torrents ORDER BY totalSnatched DESC LIMIT 1	WhatCDHipHop
SELECT releaseType FROM torrents GROUP BY releaseType ORDER BY sum(totalSnatched) DESC LIMIT 1	WhatCDHipHop
SELECT artist FROM torrents GROUP BY artist ORDER BY sum(totalSnatched) DESC LIMIT 1	WhatCDHipHop
SELECT sum(totalSnatched), releaseType FROM torrents GROUP BY releaseType	WhatCDHipHop
SELECT sum(totalSnatched) FROM torrents WHERE groupYear BETWEEN 2000 AND 2010 UNION SELECT sum(totalSnatched) FROM torrents WHERE groupYear < 2000	WhatCDHipHop
SELECT count(*) FROM ( SELECT groupName FROM torrents GROUP BY groupName HAVING count(*) > 1 )	WhatCDHipHop
SELECT artist FROM torrents GROUP BY artist ORDER BY count(groupName) DESC LIMIT 1	WhatCDHipHop
SELECT sum(totalSnatched) FROM torrents WHERE releaseType = "ep"  UNION SELECT sum(totalSnatched) FROM torrents WHERE releaseType = "album"	WhatCDHipHop
SELECT artist FROM torrents GROUP BY artist HAVING count(*) = 1	WhatCDHipHop
SELECT artist FROM torrents WHERE groupYear > 2010 GROUP BY artist	WhatCDHipHop
SELECT AwayTeam FROM football_data WHERE HomeTeam = "Omiya Ardija" AND Season LIKE "%2018%"	WorldSoccerDataBase
SELECT count(*) FROM football_data WHERE Season LIKE "%2010%" AND Country = "Spain"	WorldSoccerDataBase
SELECT MATCH FROM betfront ORDER BY DRAW_OPENING DESC LIMIT 1	WorldSoccerDataBase
SELECT YEAR FROM betfront GROUP BY YEAR ORDER BY count(*) DESC LIMIT 1	WorldSoccerDataBase
SELECT count(*) FROM football_data WHERE PSH != "" AND PSD != "" AND PSA != ""	WorldSoccerDataBase
SELECT count(*) FROM football_data WHERE B365H > PSH	WorldSoccerDataBase
SELECT count(*) FROM football_data WHERE FTHG + FTAG > 5	WorldSoccerDataBase
SELECT max(B365A) FROM football_data	WorldSoccerDataBase
SELECT count(*) FROM football_data WHERE FTHG = 0 AND FTAG = 0	WorldSoccerDataBase
SELECT count(Div) FROM football_data	WorldSoccerDataBase
SELECT count(League) FROM football_data WHERE Country != "Scotland" and Country != "England" and Referee != ""	WorldSoccerDataBase
SELECT B365D FROM football_data WHERE HomeTeam = "Swindon" and AwayTeam = "Millwall" and Season = "2016/2017"	WorldSoccerDataBase
SELECT votedby FROM hall_of_fame WHERE yearid = "2000" GROUP BY votedby ORDER BY count(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT count(*) FROM player WHERE weight > 200	TheHistoryofBaseball
SELECT player_id FROM player_award WHERE year = 2010 AND award_id = "Rookie of the Year"	TheHistoryofBaseball
SELECT player_id FROM salary WHERE year >= 2010 ORDER BY salary DESC LIMIT 1	TheHistoryofBaseball
SELECT T2.salary FROM salary as T2 JOIN hall_of_fame as T1 ON T1.player_id = T2.player_id WHERE T1.inducted = "Y"	TheHistoryofBaseball
SELECT min(votes), yearid FROM hall_of_fame WHERE inducted = "Y" AND yearid >= 1871 GROUP BY yearid	TheHistoryofBaseball
SELECT salary FROM salary WHERE league_id = "NL"	TheHistoryofBaseball
SELECT salary FROM salary WHERE league_id = "AL"	TheHistoryofBaseball
SELECT birth_country FROM player as T1 JOIN player_award as T2 ON T1.player_id = T2.player_id GROUP BY T1.birth_country ORDER BY count(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT T1.birth_country FROM hall_of_fame as T2 JOIN player as T1 ON T1.player_id = T2.player_id WHERE T2.inducted = "Y" AND T2.yearid >= 1871	TheHistoryofBaseball
SELECT award_id FROM player_award as T1 JOIN salary as T2 ON T1.player_id = T2.player_id GROUP BY T1.award_id ORDER BY avg(T2.salary) DESC LIMIT 1	TheHistoryofBaseball
SELECT DISTINCT yearid FROM hall_of_fame WHERE needed_note != ""	TheHistoryofBaseball
SELECT T1.birth_country FROM player as T1 JOIN hall_of_fame as T2 ON T1.player_id = T2.player_id WHERE T2.inducted = "Y" GROUP BY T1.birth_country ORDER BY count(*) DESC LIMIT 10	TheHistoryofBaseball
SELECT T1.player_id, T1.award_id , min(T1.year - T2.birth_year) FROM player_award as T1 JOIN player as T2 ON T1.player_id = T2.player_id GROUP BY T1.award_id	TheHistoryofBaseball
SELECT T1.player_id, T1.award_id , max(T1.year - T2.birth_year) FROM player_award as T1 JOIN player as T2 ON T1.player_id = T2.player_id GROUP BY T1.award_id	TheHistoryofBaseball
SELECT T2.team_id FROM hall_of_fame as T1 JOIN salary as T2 ON T1.player_id = T2.player_id AND T1.yearid = T2.year WHERE T1.inducted = "Y" GROUP BY T2.team_id ORDER BY count(*) DESC LIMIT 10	TheHistoryofBaseball
SELECT avg(T1.death_year - T1.birth_year) FROM player as T1 JOIN hall_of_fame as T2 ON T1.player_id = T2.player_id WHERE T2.inducted = "Y"	TheHistoryofBaseball
SELECT avg(T1.weight) FROM player as T1 JOIN player_award as T2 ON T1.player_id = T2.player_id GROUP BY notes	TheHistoryofBaseball
SELECT T2.notes FROM hall_of_fame as T1 JOIN player_award as T2 ON T1.player_id = T2.player_id WHERE T1.inducted = "Y" GROUP BY notes ORDER BY count(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT player_id FROM player_award_vote WHERE year = "1971" ORDER BY points_won DESC LIMIT 1	TheHistoryofBaseball
SELECT T1.birth_month FROM player as T1 JOIN hall_of_fame as T2 ON T1.player_id = T2.player_id WHERE T2.inducted = "Y" GROUP BY T1.birth_month ORDER BY count(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT league_id FROM player_award WHERE year = "2006" GROUP BY league_id ORDER BY count(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT DISTINCT notes FROM player_award WHERE player_id = "willite01"	TheHistoryofBaseball
SELECT count(*) FROM (SELECT player_id FROM player_award GROUP BY player_id HAVING count(*) > 10)	TheHistoryofBaseball
SELECT birth_city FROM player GROUP BY birth_city ORDER BY count(*) DESC LIMIT 1	TheHistoryofBaseball
SELECT avg(T1.weight) FROM player as T1 JOIN player_award as T2 ON T1.player_id = T2.player_id WHERE T2.award_id = "TSN All-Star" AND notes = "3B"	TheHistoryofBaseball
SELECT player_id FROM salary WHERE year = "2015" ORDER BY salary DESC LIMIT 1	TheHistoryofBaseball
SELECT DISTINCT commod FROM sampledata15	Pesticide
SELECT count(*) FROM sampledata15 WHERE origin = "3"	Pesticide
SELECT T2.commod FROM resultsdata15 as T2 JOIN sampledata15 as T1 ON T1.sample_pk = T2.sample_pk WHERE T1.year = 15 GROUP BY T2.commod ORDER BY sum(T2.concen) DESC LIMIT 10	Pesticide
SELECT commod FROM sampledata15 WHERE origin = 2 AND commod not in (SELECT commod FROM sampledata15 WHERE origin = 1)	Pesticide
SELECT T1.growst, avg(T2.concen) FROM sampledata15 as T1 JOIN resultsdata15 as T2 ON T1.sample_pk = T2.sample_pk GROUP BY T1.growst	Pesticide
SELECT T1.variety FROM resultsdata15 as T2 JOIN sampledata15 as T1 ON T1.sample_pk = T2.sample_pk WHERE T2.commod = "AP" GROUP BY T1.variety ORDER BY sum(T2.concen) DESC LIMIT 1	Pesticide
SELECT commod FROM resultsdata15 WHERE concen > lod	Pesticide
SELECT lab FROM resultsdata15 GROUP BY lab ORDER BY count(*) DESC LIMIT 5	Pesticide
SELECT T1.country FROM sampledata15 as T1 JOIN resultsdata15 as T2 ON T1.sample_pk = T2.sample_pk GROUP BY T1.country ORDER BY sum(T2.concen) LIMIT 1	Pesticide
SELECT distst FROM sampledata15 GROUP BY distst ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT max(concen) FROM resultsdata15	Pesticide
SELECT year, month, day FROM sampledata15 WHERE sample_pk = 3763	Pesticide
SELECT distst FROM sampledata15 WHERE commod = "AP" GROUP BY distst ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT growst FROM sampledata15 WHERE commod = "AP" GROUP BY growst ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT count(DISTINCT variety) FROM sampledata15	Pesticide
SELECT site FROM sampledata15 WHERE sample_pk = 3763	Pesticide
SELECT country FROM sampledata15 WHERE sample_pk = 6480 AND origin = 2	Pesticide
SELECT quantity FROM sampledata15 WHERE sample_pk = 9628	Pesticide
SELECT testclass FROM resultsdata15 WHERE sample_pk = 7498	Pesticide
SELECT confmethod FROM resultsdata15 as T2 JOIN sampledata15 as T1 ON T1.sample_pk = T2.sample_pk ORDER BY year, month, day DESC LIMIT 1	Pesticide
SELECT lab FROM resultsdata15 GROUP BY lab ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT max(testclass) FROM resultsdata15	Pesticide
SELECT conunit FROM resultsdata15 WHERE sample_pk = 3879	Pesticide
SELECT conunit FROM resultsdata15 WHERE commod = "PO"	Pesticide
SELECT mean FROM resultsdata15 WHERE commod = "AP"	Pesticide
SELECT max(extract) FROM resultsdata15	Pesticide
SELECT lab FROM resultsdata15 GROUP BY lab ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT lab FROM resultsdata15 WHERE commod = "AP"	Pesticide
SELECT count(*) FROM sampledata15 WHERE origin = "2"	Pesticide
SELECT commod FROM resultsdata15 WHERE mean = "A" GROUP BY commod ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT state FROM sampledata15 WHERE claim = "PO" GROUP BY state ORDER BY count(*) DESC LIMIT 1	Pesticide
SELECT max(country) FROM sampledata15	Pesticide
SELECT max(commod) FROM resultsdata15	Pesticide
SELECT max(pestcode) FROM resultsdata15	Pesticide
SELECT Country FROM nuclear_power_plants GROUP BY Country ORDER BY sum(Capacity) DESC LIMIT 1	GeoNuclearData
SELECT Country FROM nuclear_power_plants GROUP BY Country ORDER BY sum(Capacity) LIMIT 1	GeoNuclearData
SELECT Country FROM nuclear_power_plants GROUP BY Country ORDER BY sum(Name) DESC LIMIT 3	GeoNuclearData
SELECT Country FROM nuclear_power_plants GROUP BY Country ORDER BY count(Name) DESC LIMIT 1	GeoNuclearData
SELECT Country FROM nuclear_power_plants WHERE Status = "Shutdown" GROUP BY Country ORDER BY count(Name) DESC LIMIT 1	GeoNuclearData
SELECT Name FROM nuclear_power_plants ORDER BY Capacity DESC LIMIT 1	GeoNuclearData
SELECT count(*) FROM nuclear_power_plants WHERE Country = "France" and Status = "Operational"	GeoNuclearData
SELECT count(Name) FROM nuclear_power_plants WHERE Status = "Under Construction"	GeoNuclearData
SELECT ReactorModel FROM nuclear_power_plants GROUP BY ReactorModel ORDER BY count(*) DESC LIMIT 1	GeoNuclearData
SELECT Country FROM nuclear_power_plants WHERE Name = "Chinon-A3"	GeoNuclearData
SELECT Name FROM nuclear_power_plants where Status = "Operational" and Country = "Japan"	GeoNuclearData
SELECT Country FROM nuclear_power_plants ORDER BY OperationalFrom LIMIT 1	GeoNuclearData
SELECT count(*) FROM nuclear_power_plants WHERE Country = "Japan" AND Status = "Under Construction"	GeoNuclearData
SELECT Status FROM nuclear_power_plants WHERE Country = "United States" ORDER BY Capacity DESC LIMIT 1	GeoNuclearData
SELECT max(Capacity) FROM nuclear_power_plants WHERE ReactorType = "PWR" and Status = "Operational"	GeoNuclearData
SELECT Country FROM nuclear_power_plants WHERE Status = "Under Construction" GROUP BY Country ORDER BY count(*) DESC LIMIT 1	GeoNuclearData
SELECT Country FROM nuclear_power_plants WHERE Status = "Under Construction" GROUP BY Country ORDER BY count(*) DESC LIMIT 1	GeoNuclearData
SELECT Longitude, Latitude FROM nuclear_power_plants WHERE ReactorType = "BWR" ORDER BY ConstructionStartAt LIMIT 1	GeoNuclearData
SELECT Country FROM nuclear_power_plants GROUP BY Country ORDER BY sum(Capacity) DESC LIMIT 1	GeoNuclearData
SELECT Source FROM nuclear_power_plants GROUP BY Source ORDER BY count(*) DESC LIMIT 1	GeoNuclearData
SELECT ReactorType FROM nuclear_power_plants GROUP BY ReactorType ORDER BY avg(Capacity) DESC LIMIT 1	GeoNuclearData
SELECT Country FROM nuclear_power_plants WHERE Name = "Kursk-1"	GeoNuclearData
