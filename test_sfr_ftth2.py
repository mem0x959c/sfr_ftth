import sys, csv, requests, multiprocessing
import sfr_ftth

#csv file format: x,y,imb_id,num_voie,cp_no_voie,type_voie,nom_voie,batiment,code_poste,nom_com,catg_loc_imb,imb_etat,pm_ref,pm_etat,code_l331,geom_mod,type_imb
def MakeAddressFromCsvRow(row):
    address = '{} {} {}, {} {}'.format(row['num_voie'], row['type_voie'], row['nom_voie'], row['code_poste'], row['nom_com'])
    return sfr_ftth.NormalizePostalAddress(address)

def GetAddressesFromCsvFile(csvFilePath):
    addresses = set()
    with open(csvFilePath, encoding='utf-8') as csvFile:
        reader = csv.DictReader(csvFile)        
        next(reader)
        for row in reader:
            address = MakeAddressFromCsvRow(row)
            addresses.add(address)
    return sorted(addresses)

def GetNonDeployedAddressesFromCsvFile(csvFilePath):
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
    addresses = GetAddressesFromCsvFile(csvFilePath)
    #addresses = GetNonDeployedAddressesFromCsvFile(csvFilePath)
    session = requests.Session()
    with multiprocessing.Pool(processes=50) as pool:
        results = pool.imap(sfr_ftth.GetEligibilityByPostalAddress2, [(a, session, debug) for a in addresses])
        
        numEligible = 0
        num666 = 0
        numWip = 0
        for r, a in zip(results, addresses):
            print('{}, code {}, eligible {}, workInProgress {}'.format(a, r[0], r[1], r[2]))
            if r[1] == True: numEligible += 1
            if r[0] == 666: num666 += 1
            if r[2] == True: numWip += 1
        
        numAddresses = len(addresses)
        print("Number of eligible addresses {} / {} ({:.2f}%)".format(numEligible, numAddresses, numEligible/numAddresses*100))
        print("Number of workInProgress==True {} / {} ({:.2f}%)".format(numWip, numAddresses, numWip/numAddresses*100))
        print("Number of code 666 {} / {} ({:.2f}%)".format(num666, numAddresses, num666/numAddresses*100))

if __name__ == "__main__":
    debug = False
    if len(sys.argv) >= 2:
        csvFilePath = sys.argv[1]
        PrintSfrEligibility(csvFilePath, debug)
        #CompareArcepSfrEligibility(csvFilePath, debug)
    else:
        print('Usage: {} <csv_file_path>'.format(sys.argv[0]))
        sys.exit(1)
