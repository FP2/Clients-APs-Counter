# Clients-APs-Counter

Two simple python scripts that count the quantity of clients connected to all APs and switches,for both private and public networks,  of all the shopping malls managed by a particular company. Then it integrates the final data into a timebased database(InfluxDB) so they can make graphics out of it. 

- apscrawler1 - Accesses all the organizations in Cisco Meraki Dashboard and genarate a csv file containing all the APs and switches' serial numbers.

- apscrawler2 - Reads the csv generated by apscrawler1, use all the serials from the csv as paramaters for gettig the quantity of clients connected to all the devices and generates a dataframe with the results. Then a session on InfluxDB is started, if the database where all the data are going to be living in doesn't exist, the script will create one(which is the case for the first time the client runs the script), then all the data is written into the new database.

The client then can make different sorts of graphics based on the final data using Grafana for example.
