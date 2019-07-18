from meraki import meraki
import requests
import csv
import logging
from datetime import datetime
import pandas as pd
from influxdb import InfluxDBClient

logging.basicConfig(
    filename='log_apsc2.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

API = 'db977e503984058237f9bfbbaf91a5e67d0dbe20'

sorted_adm = []
sorted_captive = []
adm = []
captive = []
dbnames = []


try:
    logging.info('start time.')

    with open('serials.txt', 'r') as serials_file:
        reader = csv.reader(serials_file)
        serials_list = list(reader)
        serials_file.close()

    counter_adm = 0
    counter_cap = 0
    total_counter_adm = 0
    total_counter_cap = 0

    for i in serials_list:
        if i[1] == 'ADM':
            adm.append(i)
        else:
            captive.append(i)

    for i in adm:
        counter_adm = len(meraki.getclients(API, i[3], 300))
        date_raw = str(datetime.utcnow())
        date_no_milli = date_raw[:20]
        date_T = date_no_milli.replace(" ", "T")
        date_T_Z = date_T.replace(".", "Z")
        total_counter_adm += counter_adm
        set_adm_final = [i[2], i[1], i[0], counter_adm, date_T_Z]
        sorted_adm.append(set_adm_final)
    for j in captive:
        counter_cap = len(meraki.getclients(API, j[3], 300))
        date_raw = str(datetime.utcnow())
        date_no_milli = date_raw[:20]
        date_T = date_no_milli.replace(" ", "T")
        date_T_Z = date_T.replace(".", "Z")
        total_counter_cap += counter_cap
        set_cap_final = [j[2], j[1], j[0], counter_cap, date_T_Z]
        sorted_captive.append(set_cap_final)

    sorted_final = sorted_adm + sorted_captive

    logging.info('all aps scanned.')
    logging.info('adm: {}'.format(total_counter_adm))
    logging.info('captive: {}'.format(total_counter_cap))

    labels = ['shopping', 'network', 'ap_name', 'clients', 'tempo']
    df_clients = pd.DataFrame.from_records(sorted_final, columns=labels)

    client = InfluxDBClient('localhost', 8086)

    dbs = client.get_list_database()
    for i in dbs:
        for j in i.values():
            dbnames.append(j)
    if 'clients' not in dbnames:
        client.create_database('clients')

    for row_index, row in df_clients.iterrows():
        tag1 = row[0]
        tag2 = row[1]
        tag3 = row[2]
        time = row[4]
        fieldValue = row[3]
        json_body = [
            {
                "measurement": "clients",
                "tags": {
                    "shopping": tag1,
                    "network": tag2,
                    "ap_name": tag3
                },
                "time": time,
                "fields": {
                    "clients": fieldValue
                }
            }
        ]
        client = InfluxDBClient('localhost', 8086, database='clients')
        client.write_points(json_body)

    logging.info('all points writen in clients database.')
    logging.info('end time.')

except requests.exceptions.ConnectionError as r:
    co_error = "Connection error raised."
    logging.error('{}'.format(co_error))
    tipo = (type(r))
    print('{}'.format(co_error))
    print('{}'.format(tipo))

except TimeoutError as t:
    to_error = "Connection timeout error raised."
    logging.error('{}'.format(to_error))
    tipo = (type(t))
    print('{}'.format(to_error))

    print('{}'.format(tipo))

except ConnectionError as c:
    con_error = '"Connection error raised."'
    logging.error('{}'.format(con_error))
    tipo = (type(c))
    print('{}'.format(con_error))
    print('{}'.format(tipo))

except Exception as unknown:
    logging.error('{}'.format(unknown))
    tipo = (type(unknown))
    logging.error('{}'.format(tipo))
    print('{}'.format(unknown))
