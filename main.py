from access_db import DBAccess
from api import API
import logging


logger = logging.getLogger()
logging.basicConfig(
    filename="Main_logfile.log",
    format="[%(asctime)s][%(levelname)s] %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M"
    )

logger.info("Script started")



path = "" 
#edit if needed
db = "Stock Database.db"
dbaccess = DBAccess(path,db)
api = API()

update_list = dbaccess.get_list_of_needed_updates()
#hämta lista för vilka företag som har släppt ny rapport

if not update_list:
    logging.info("update_list is empty")
    earnings_update_list = dbaccess.check_earnings_last_update()
    api.add_list(earnings_update_list)
    earnings = api.get_earnings_date()
    dbaccess.update_earnings_date(earnings)
    dbaccess.close_connection()
    exit()
    #updates earnings if needed and then exits script
else:
    logging.info("update list include: "+  ", ".join(update_list))


api.add_list(update_list)
api.get_financials()

financials, failed_calls, time = api.get_all()
   

if len(failed_calls) != 0:
    for i in range(len(failed_calls)):
        logging.warning("Stock "+ failed_calls[i]+ " failed to download data")
        

failed_update = dbaccess.insert_financial_data(financials)
#insert data to table, return list of tables where new data was not inserted

updated = list(set(failed_update).symmetric_difference(update_list))
#create list for those that did get updated successfully

dbaccess.update_last_update(time,updated)
#update only those that did get updated

earnings_update_list = dbaccess.check_earnings_last_update()
#check if old earnings date got new dates

complete_earnings_list = list(set(updated).union(earnings_update_list))

api.add_list(complete_earnings_list)
#reseting list of companies in api instance if some failed to update

earnings = api.get_earnings_date()

dbaccess.update_earnings_date(earnings)

dbaccess.close_connection()
#close connection


#todo
#upload to github and write readme file

















#get data (
#   kolla om företaget finns i vår databas, om inte laddar ner. obs alla från Sp500
#   när vi har kollat ett företags finns i tabellen, ladda ner dess info och sedan spara nästa kvartalls raport release, evnt error om de inte finns
#   check listan med alla kommande kvartalls rapporter, jämnför med dagens datum. om nästa rapport är äldre än dagens datum "gammal" så updatera.
#   ex abs report release 24/09/16 < today så update.
#   updaterar företagets rapport efter varje earnings call.
#   automatiserad check varje dag kl xx:xx om earnings har kommit
#   när ett flretag har fått en update och updaterat sin tabell så skall även nästa earnings call updateras
#   i sp500 tabell listan
#

#)



#clean/format data
#   database med aktier
#   tabell för alla företag som är med i sp500 och när deras nästa earnings är
#   tabell för varje företag och deras statements, börja bara med balance cheet utvidga sen om vi vill
#   När en update kommer in, formatera tabellen så att vi får den enkel och läsbar.
#   sedan updatera SQL tabellen för x företag.

#plannering
#börja med att skapa en klass för att få rå data,
#klass api
#   alla temp här under
#       ta ner en lista för alla företag i sp500
#       listan behöver ej updateras efter som sp500 sällan ändrar företag i sin bucket "rebalancing"
#       ladda ner alla nuvarande rapporter för alla sp500 företag "skapa tabeller för dem sen"
#
#   schema lagda updateringar
#       checka lista för nästa earnings vs today hos alla företag "ej med api utan via sql tabell"
#       vid en update, ladda ner företagets balance sheet sedan skicka till formaterings klass
#
#formaterings klass
#   skapa database
#       försök göra i python med sql-lite #  OBS FÖRETAGETS NAMN ÄR PRIMARY KEY
#       efter databas skapa tabell vid namn sp500 earnings calls 
#       skapa tabeller för varje företag med deras balance sheet       
#
#   temp/först runs
#       tabellen kommer i senaste>äldre, ändra till tvärt om så första > senaste
#       dem kan fortsätta vara radvis
#

#TODO
#fixa function i troligen API klassen där vi får nästa earnings
#fixa så att vi kan updatera våra SQL tabeller i access_db
#fixa så vi kan skapa tabeller med financiell data i access_db

