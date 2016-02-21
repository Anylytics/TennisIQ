cd "~/Anylytics//TennisIQ"

import delimited "/Users/NitinKrishnan/Anylytics/TennisIQ/Processed/points.csv", encoding(ISO-8859-1)clear
save "Analysis_Nitin/points.dta", replace

import delimited "/Users/NitinKrishnan/Anylytics/TennisIQ/Processed/players.csv", encoding(ISO-8859-1)clear
gen serverid = _n - 1
gen returnerid = _n - 1
rename v1 name
sort serverid
save "Analysis_Nitin/players.dta", replace
 
cd "~/Anylytics//TennisIQ/Analysis_Nitin"
use points, clear
sort serverid
merge n:1 serverid using players
drop _merge
rename name servername
save points, replace

use players, clear
sort returnerid 
save players, replace

use points, clear
sort returnerid
merge n:1 returnerid using players
drop _merge
rename name returnername
save points, replace 

cd "~/Anylytics//TennisIQ"


import delimited "/Users/NitinKrishnan/Anylytics/TennisIQ/Processed/tournaments.csv", encoding(ISO-8859-1)clear
gen tournamentid = _n - 1
rename v1 tournamentname 
sort tournamentid
save "Analysis_Nitin/tournaments.dta", replace

cd "~/Anylytics//TennisIQ/Analysis_Nitin"


use atpmatchesAll, clear
keep tourney_name tourney_date winner_name winner_rank
rename winner_name name
rename winner_rank rank
save rankKey, replace

use atpmatchesAll, clear
keep tourney_name tourney_date loser_name loser_rank
rename loser_name name
rename loser_rank rank

append using rankKey
tostring tourney_date, gen(tS)
egen datename = concat(tS name)
drop tS
duplicates drop datename, force
drop datename 
rename name servername
rename tourney_date date
sort date servername

tostring date, gen(dateString)
gen yearmonth = substr(dateString,1,6)
sort servername yearmonth
save rankKey, replace

use rankKey, clear
duplicates drop servername, force
keep servername
save uniquenames, replace 

use rankKey, clear
duplicates drop yearmonth, force
keep yearmonth
cross using uniquenames 
sort servername yearmonth
merge servername yearmonth using rankKey 
drop tourney_name - dateString _merge
sort servername yearmonth
by servername: gen c = _n
by server: ipolate rank c, gen(rank_interp) 
replace rank = round(rank_interp)
sort servername yearmonth
drop rank_interp
sort servername yearmonth
save rankKey, replace




*Merge player data here if needed 
use points, clear
tostring date, gen(yearmonth)
replace yearmonth = substr(yearmonth,1,6)
sort servername yearmonth
merge servername yearmonth using rankKey
keep if _merge == 1 | _merge == 3
rename rank serverrank
drop c _merge
save points, replace

use rankKey, clear
rename servername returnername
sort returnername yearmonth
save rankKey, replace

use points, clear
sort returnername yearmonth
merge returnername yearmonth using rankKey
keep if _merge == 1 | _merge == 3
rename rank returnerrank
drop c
save points, replace








*Making game score into string
egen gamescore = concat(gamescore1  gamescore2), punct("-")
egen serverid_gamescore = concat(serverid gamescore),punct(",")
egen returnerid_gamescore = concat(returnerid gamescore), punct(",")

gen n = 1

bys serverid_gamescore: egen servePointProbability = mean(wonpt)
bys serverid_gamescore: egen servePointFreq = sum(n)
bys returnerid_gamescore: egen returnPointProbability = mean(1-wonpt)
bys returnerid_gamescore: egen returnPointFreq = sum(n)

*Against top 20 players
*foreach x in 100 124 83 205 259 43 38 192 225 53 120 295 13 264 171 287 80 178 101 315{
*}



save pointsMoreVariables, replace

use pointsMoreVariables, clear

keep serverid gamescore servePointProbability serverid_gamescore servePointFreq
duplicates drop serverid_gamescore, force
drop serverid_gamescore
split gamescore, p("-") destring
replace gamescore1 = ceil(gamescore1/15)
replace gamescore2 = ceil(gamescore2/15)
rename gamescore1 playerScore
rename gamescore2 opponentScore

save serviceWinProbabilites, replace 

export delimited using "/Users/NitinKrishnan/Anylytics/TennisIQ/Analysis_Nitin/serviceWinProbabilities.csv", replace


use pointsMoreVariables, clear

keep returnername gamescore returnPointProbability returnerid_gamescore returnPointFreq
duplicates drop returnerid_gamescore, force
drop returnerid_gamescore
split gamescore, p("-") destring
replace gamescore1 = ceil(gamescore1/15)
replace gamescore2 = ceil(gamescore2/15)
rename gamescore1 opponentScore
rename gamescore2  playerScore

save returnwinProbabilities, replace


export delimited using "/Users/NitinKrishnan/Anylytics/TennisIQ/Analysis_Nitin/returnWinProbabilities.csv", replace


*Top 20 - serving
use pointsmoreVariables, clear
egen OK = anymatch(returnerid), values(100 124 83 205 259 43 38 192 225 53 120 295 13 264 171 287 80 178 101 315)
keep if OK
drop OK
*keep if returnerid == 100 | 124 | 83 | 205 | 259 | 43 | 38 | 192 | 225 | 53 | 120 | 295 | 13 | 264 | 171 | 287 | 80 | 178 | 101 | 315

bys serverid_gamescore: egen servePointProbability_top20 = mean(wonpt)
bys serverid_gamescore: egen servePointFreq_top20 = sum(n)
bys returnerid_gamescore: egen returnPointProbability_top20 = mean(1-wonpt)
bys returnerid_gamescore: egen returnPointFreq_top20 = sum(n)



keep servername gamescore servePointProbability_top20 servePointFreq_top20 serverid_gamescore
duplicates drop serverid_gamescore, force
drop serverid_gamescore
split gamescore, p("-") destring
replace gamescore1 = ceil(gamescore1/15)
replace gamescore2 = ceil(gamescore2/15)
rename gamescore1 playerScore
rename gamescore2 opponentScore
sort servername gamescore

save serviceWinProbabilites_Top20, replace 


export delimited using "/Users/NitinKrishnan/Anylytics/TennisIQ/Analysis_Nitin/serviceWinProbabilities_Top20.csv", replace


*Top 20 - returning
use pointsmoreVariables, clear
*egen OK = anymatch(serverid), values(100 124 83 205 259 43 38 192 225 53 120 295 13 264 171 287 80 178 101 315)
egen OK = anymatch(serverid), values(100 124 83 205 259)
keep if OK
drop OK
*keep if returnerid == 100 | 124 | 83 | 205 | 259 | 43 | 38 | 192 | 225 | 53 | 120 | 295 | 13 | 264 | 171 | 287 | 80 | 178 | 101 | 315

bys serverid_gamescore: egen servePointProbability_top20 = mean(wonpt)
bys serverid_gamescore: egen servePointFreq_top20 = sum(n)
bys returnerid_gamescore: egen returnPointProbability_top20 = mean(1-wonpt)
bys returnerid_gamescore: egen returnPointFreq_top20 = sum(n)


keep returnername gamescore returnPointProbability_top20 returnPointFreq_top20 returnerid_gamescore returnerid
duplicates drop returnerid_gamescore, force
drop returnerid_gamescore
split gamescore, p("-") destring
replace gamescore1 = ceil(gamescore1/15)
replace gamescore2 = ceil(gamescore2/15)
rename gamescore1 opponentScore
rename gamescore2 playerscore
sort returnername gamescore

save returnwinProbabilities_Top20, replace



export delimited using "/Users/NitinKrishnan/Anylytics/TennisIQ/Analysis_Nitin/returnWinProbabilities_Top20.csv", replace









