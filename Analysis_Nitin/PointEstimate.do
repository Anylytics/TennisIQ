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

*Merge player data here if needed 


*Making game score into string
egen gamescore = concat(gamescore1  gamescore2), punct("-")
egen serverid_gamescore = concat(serverid gamescore),punct(",")
egen returnerid_gamescore = concat(returnerid gamescore), punct(",")

bys serverid_gamescore: egen servePointProbability = mean(wonpt)
bys returnerid_gamescore: egen returnPointProbability = mean(1-wonpt)





save pointsMoreVariables, replace
