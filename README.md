# gva-scraper
a little thing to scrape the gun violence archive

Description: copies data from gunviolencearchive.org into two .csv files: GVA-Table.csv for the tabular data, and GVA-Details.csv for details.

Usage:
gvascrape [tableFileName.csv] [detailFileName.csv] [nextUrl]
all arguments are optional
example: gvascrape.py accident_kid_table.csv accident_kid_details.csv accidental-child-deaths

tableFileName.csv
  the name of the file which records tabular data from gunviolencearchive.org reports such 
  as http://www.gunviolencearchive.org/reports/mass-shooting?year=2016. 
  default: gvaTable.csv
  The file contains 1 row for each table row, and 10 columns:
  ID, date, state,	city,	dead,	wounded,	incident_url,	cite_1,	lat, long

detailFileName.csv
  the name of the file which records incident detail data from gunviolencearchive.org incidents such
  as http://www.gunviolencearchive.org/incident/738749
  default: gvaDetails.csv
  The file contains 1 row for each incident page, and 6 columns
  ID,	Participants,	Characteristics,	Notes,	Guns,	Sources, 1

nextUrl
  The right hand side of the url on the gunviolencearchive.org site for the report you want to scrape
  default: 'reports/mass-shooting?year=2016'
  example: to scrape the 2014 mass shootings, use 'reports/mass-shooting?year=2016'
  

