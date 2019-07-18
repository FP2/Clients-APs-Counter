from meraki import meraki
import logging
import requests
import csv

logging.basicConfig(filename='log_apsc1.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

KEY = 'db977e503984058237f9bfbbaf91a5e67d0dbe20'

org_ids = []
org_names = []
net_ids_adm = []
net_ids_captive = []
adm_apnames = []
adm_orgs = []
net_type_adm = []
adm_serial = []
adm_counter = []
cap_apnames = []
cap_orgs = []
net_type_cap = []
cap_serial = []
cap_counter = []

try:
    logging.info('start time')
    for org in meraki.myorgaccess(KEY):
        if org.get('name') == 'CNB - Camera' and org.get('id') == '597852850533433525':
            continue
        org_names.append(org.get('name'))
        org_ids.append(org.get('id'))

    org_names_ids = sorted(list(zip(org_names, org_ids)))

    for single in org_names_ids:
        networks = meraki.getnetworklist(KEY, single[1])
        for network in networks:
            if 'ADMINISTRAÇÃO' in network.get('name'):
                set_adm = [network.get('organizationId'), network.get('name'), network.get('id')]
                net_ids_adm.append(set_adm)
            elif 'CAPTIVE PORTAL WIFI' in network.get('name'):
                set_captive = [network.get('organizationId'), network.get('name'), network.get('id')]
                net_ids_captive.append(set_captive)
            else:
                continue

    for j in org_names_ids:
        for adm in net_ids_adm:
            if j[1] == adm[0]:
                sigla_adm = [j[0]]
                adm += list(sigla_adm)
            else:
                continue
        for cap in net_ids_captive:
            if j[1] == cap[0]:
                sigla_cap = [j[0]]
                cap += list(sigla_cap)
            else:
                continue

    for net_adm in net_ids_adm:
        devices = meraki.getnetworkdevices(KEY, net_adm[2])
        for device in devices:
            device_name = device.get('name')
            device_org = meraki.getorg(KEY, net_adm[0]).get('name')
            device_serial = device.get('serial')
            adm_apnames.append(device_name)
            net_type_adm.append('ADM')
            adm_orgs.append(device_org)
            adm_serial.append(device_serial)
    for net_cap in net_ids_captive:
        devices_cap = meraki.getnetworkdevices(KEY, net_cap[2])
        for device_cap in devices_cap:
            device_name = device_cap.get('name')
            device_org = meraki.getorg(KEY, net_cap[0]).get('name')
            device_serial = device_cap.get('serial')
            cap_apnames.append(device_name)
            net_type_cap.append('CAPTIVE')
            cap_orgs.append(device_org)
            cap_serial.append(device_serial)

    final_adm = list(zip(adm_apnames, net_type_adm, adm_orgs, adm_serial))
    final_cap = list(zip(cap_apnames, net_type_cap, cap_orgs, cap_serial))
    final = final_adm + final_cap

    logging.info('all networks scanned')

    with open('serials.txt', mode='w', newline='') as serials_file:
        writer = csv.writer(serials_file)
        for item in final:
            writer.writerow(item)

    logging.info('Serials.txt created')
    logging.info('end time')

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
