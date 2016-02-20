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
keep tourney_date winner_name winner_rank
rename winner_name name
rename winner_rank rank
save rankKey, replace

use atpmatchesAll, clear
keep tourney_date loser_name loser_rank
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
save rankKey, replace


*Merge player data here if needed 
use points, clear
sort date servername
nearmrg servername date using rankKey, nearvar(date)
rename rank serverrank
drop _merge
save points, replace

use rankKey, clear
rename servername returnername
sort date returnername
save rankKey, replace

use points, clear
sort date returnername
nearmrg date returnername using rankKey, nearvar(date)
rename rank returnerrank
drop _merge
save points, replace





*Making game score into string
egen gamescore = concat(gamescore1  gamescore2), punct("-")
egen serverid_gamescore = concat(serverid gamescore),punct(",")
egen returnerid_gamescore = concat(returnerid gamescore), punct(",")

bys serverid_gamescore: egen servePointProbability = mean(wonpt)
bys returnerid_gamescore: egen returnPointProbability = mean(1-wonpt)

*Against top 20 players
*foreach x in 100 124 83 205 259 43 38 192 225 53 120 295 13 264 171 287 80 178 101 315{
*}

keep if returnerid == 100 & 124 & 83 & 205 & 259 & 43 & 38 & 192 & 225 & 53 & 120 & 295 & 13 & 264 & 171 & 287 & 80 & 178 & 101 & 315


save pointsMoreVariables, replace

use pointsMoreVariables, clear

keep servername gamescore servePointProbability serverid_gamescore
duplicates drop serverid_gamescore, force
drop serverid_gamescore
split gamescore, p("-") destring
replace gamescore1 = ceil(gamescore1/15)
replace gamescore2 = ceil(gamescore2/15)
rename gamescore1 playerScore
rename gamescore2 opponentScore

export delimited using "/Users/NitinKrishnan/Anylytics/TennisIQ/Analysis_Nitin/serviceWinProbabilities.csv", replace


use pointsMoreVariables, clear

keep returnername gamescore returnPointProbability returnerid_gamescore
duplicates drop returnerid_gamescore, force
drop returnerid_gamescore
split gamescore, p("-") destring
replace gamescore1 = ceil(gamescore1/15)
replace gamescore2 = ceil(gamescore2/15)
rename gamescore1 opponentScore
rename gamescore2  playerScore

export delimited using "/Users/NitinKrishnan/Anylytics/TennisIQ/Analysis_Nitin/returnWinProbabilities.csv", replace

 






