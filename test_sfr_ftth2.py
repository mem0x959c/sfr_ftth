import sys, csv, requests, multiprocessing
import sfr_ftth

#csv file format: x,y,imb_id,num_voie,cp_no_voie,type_voie,nom_voie,batiment,code_poste,nom_com,catg_loc_imb,imb_etat,pm_ref,pm_etat,code_l331,geom_mod,type_imb
def MakeAddressFromCsvRow(row):
    address = '{} {} {}, {} {}'.format(row['num_voie'], row['type_voie'], row['nom_voie'], row['code_poste'], row['nom_com'])
    return sfr_ftth.NormalizePostalAddress(address)

def GetUniqueAddressesFromCsvFile(csvFilePath):
    addressToDeployed = {}
    with open(csvFilePath, encoding='utf-8') as csvFile:
        reader = csv.DictReader(csvFile)        
        next(reader)
        for row in reader:
            address = MakeAddressFromCsvRow(row)
            deployed = row['imb_etat']=='deploye'
            previousDeployed = addressToDeployed.get(address)
            #print('{} {} {}'.format(address, previousDeployed, deployed))
            if previousDeployed is None:
                addressToDeployed[address] = deployed
            else:
                addressToDeployed[address] = previousDeployed or deployed
    addresses = [a for a,d in addressToDeployed.items() if not d]
    addresses.sort()
    return addresses
    
def PrintSfrEligibility(csvFilePath, debug):
    session = requests.Session()
    with open(csvFilePath, encoding='utf-8') as csvFile:
        reader = csv.DictReader(csvFile)        
        next(reader)
        for row in reader:
            address = MakeAddressFromCsvRow(row)
            (statusCode, statusText) = sfr_ftth.GetEligibilityByPostalAddress(address, session, debug)
            #if 'status inconnu' in statusText:
                #    print('{}, {} ({})'.format(address, statusText, statusCode))
            print('{}, {} ({})'.format(address, statusText, statusCode))
    
def CompareArcepSfrEligibility(csvFilePath, debug):
    addresses = GetUniqueAddressesFromCsvFile(csvFilePath)
    session = requests.Session()
    with multiprocessing.Pool(processes=16) as pool:
        results = pool.starmap(sfr_ftth.GetEligibilityByPostalAddress2, [(a, session, debug) for a in addresses])
    for r, a in zip(results, addresses):
        if r[0] == 1:
            print(a)
        #elif r[0] == -1:
        #    print('erreur sur cette addresse {}'.format(a))

if __name__ == "__main__":    
    debug = False
    if len(sys.argv) >= 2:
        csvFilePath = sys.argv[1]
        #PrintSfrEligibility(csvFilePath, debug)
        CompareArcepSfrEligibility(csvFilePath, debug)
    else:
        print('Usage: {} <csv_file_path>'.format(sys.argv[0]))
        sys.exit(1)
