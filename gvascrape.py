from bs4 import BeautifulSoup
from gvaincident import GVAIncident
from gvaincident import GVAIncidentDeets
import requests, sys, os, argparse
## parse the command lines for 3 parameters: the name of the output files for table and page details, and the next URL value
## next url is everything after "http://www.gunviolencearchive.org/" in the URL http://www.gunviolencearchive.org/reports/mass-shooting?year=2016
## for the front page (e.g. http://www.gunviolencearchive.org/mass-shooting), next_url = 'mass-shooting'
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('tableFileName', metavar='table output filename', type=str, nargs='?', default="GVA_Table.csv",
                    help='name of output file for table details')
parser.add_argument('detailFileName', metavar='page details output filename', type=str, nargs='?', default="GVA_Details.csv",
                    help='name of output file for table details')
parser.add_argument('nextUrl', metavar='next url', type=str, nargs='?', default='reports/mass-shooting?year=2016',
                    help='name of output file for table details')

args = parser.parse_args()

def scrape(results, soup, base_url):      
        table = soup.find("table")
        for row in table.find_all('tr')[1:]:
                col = row.find_all('td')
                
                date = col[0].string
                state= col[1].string
                city = col[2].string
                killed = col[4].string
                injured = col[5].string
                incident_url = col[6].ul.li.a.get('href')
                incident_id = incident_url[-6:]
                incident_id = incident_id
                event_url = col[6].ul.li.findNext('li').a.get('href')
                #get incident deatils from incident page
                incident = requests.get(base_url + incident_url)
                i = incident.content
                soup = BeautifulSoup(i,"html.parser")
                scrape_i(incident_id, soup)
                record = GVAIncident(incident_id, date, state, city, killed, injured, incident_url, event_url)   
##              print "added record " + incident_id
                results.append(record)

def scrape_i(incident_id, soup):
        incident_deets = []
        content = ""
        participants = soup.find("h2",string="Participants")
        #participants
        try:
                for strings in participants.parent.strings:
                        content = content + strings
                participants = content.replace('\n', ' ').replace('\r', '')
                participants = '"'+participants+'"'
        except AttributeError:
                participants = "Not on page"
                
        #characteristics
        characteristics = soup.find("h2",string="Incident Characteristics")
        content = ""
        try:
                for strings in characteristics.parent.strings:
                        content = content + strings
                characteristics = content.replace('\n', ' ').replace('\r', '')
                characteristics = '"'+characteristics+'"'
        except AttributeError:
                characteristics = "Not on page"

        #note
        note = soup.find("h2",string="Notes")                    
        try:
                note = note.nextSibling.nextSibling.get_text()
                note = note.replace('\n', ' ').replace('\r', '')
                note = '"'+note+'"'                
        except AttributeError:
                note = "Not on page"
                
        #guns
        guns = soup.find("h2",string="Guns Involved")
        content = ""
        try:
                for strings in guns.parent.strings:
                        content = content + strings
                guns = content.replace('\n', ' ').replace('\r', '')
                guns = '"'+guns+'"'
        except AttributeError:
                guns = "Not on page"

        #sources
        sources = soup.find("h2",string="Sources")
        content = ""
        try: 
                for strings in sources.parent.strings:
                        content = content + strings
                sources = content.replace('\n', ' ').replace('\r', '')
                sources = '"'+sources+'"'                
        except AttributeError:
                sources = "Not on page"

        incident_deets = GVAIncidentDeets(incident_id, participants, characteristics, note, guns, sources)
              
        #write the file
        global args
        target = open(args.detailFileName, 'a')
        target.write(repr(incident_deets))
        target.write("\n")
        print "wrote deet results" + incident_id
        target.close()
        

def write_csv(results):
        global args
        target = open(args.tableFileName,'a')
        for r in results:
                target.write(repr(r))
                target.write("\n")
        print "wrote results"
        target.close()

def main():
       
        #erase the file if they exists
        try:
                os.remove(args.tableFileName)
                os.remove(args.detailFileName)
        except OSError:
                print "No files to deletes"
        results = []
        record = []
        base_url = 'http://www.gunviolencearchive.org/'
        next_url = args.nextUrl
        while next_url:
                print base_url+next_url
                next_page = requests.get(base_url + next_url)
                c = next_page.content
                soup = BeautifulSoup(c,"html.parser")
                scrape(results, soup, base_url)
                write_csv(results)
                results=[]
                next_url = soup.find('a', {'title': 'Go to next page'})
                if next_url:
                        next_url = next_url.get('href')

if __name__ == "__main__":
        main()
