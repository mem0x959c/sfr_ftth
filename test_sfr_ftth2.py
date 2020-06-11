import sys, csv, requests, multiprocessing
import sfr_ftth

#csv file format: x,y,imb_id,num_voie,cp_no_voie,type_voie,nom_voie,batiment,code_poste,nom_com,catg_loc_imb,imb_etat,pm_ref,pm_etat,code_l331,geom_mod,type_imb

def PrintSfrEligibilityRowHandler(csvFilePath, debug):
    with open(csvFilePath, encoding='utf-8') as csvFile:
        reader = csv.DictReader(csvFile)        
        next(reader)
        for row in reader:
            address = '{} {} {}, {} {}'.format(row['num_voie'], row['type_voie'], row['nom_voie'], row['code_poste'], row['nom_com'])
            (statusCode, statusText) = sfr_ftth.GetEligibilityByPostalAddress(address, debug)
            #if 'status inconnu' in statusText:
                #    print('{}, {} ({})'.format(address, statusText, statusCode))
            print('{}, {} ({})'.format(address, statusText, statusCode))
    
def CompareArcepSfrEligibility(csvFilePath, debug):
    addresses = []
    with open(csvFilePath, encoding='utf-8') as csvFile:
        reader = csv.DictReader(csvFile)        
        next(reader)
        for row in reader:
            if row['imb_etat'] == 'deploye':
                continue            
            address = '{} {} {}, {} {}'.format(row['num_voie'], row['type_voie'], row['nom_voie'], row['code_poste'], row['nom_com'])
            addresses.append(address)
    session = requests.Session()
    with multiprocessing.Pool(processes=16) as pool:
        results = pool.starmap(sfr_ftth.GetEligibilityByPostalAddress, [(a, session, debug) for a in addresses])
    for r, a in zip(results, addresses):
        if r[0] == 1:
            print(a)
        #elif r[0] == -1:
        #    print('erreur sur cette addresse {}'.format(a))

def main(argv):
    debug = False
    csvFilePath = ''
    if len(argv) >= 2:
        csvFilePath = argv[1]
        #PrintSfrEligibility(csvFilePath, debug)
        CompareArcepSfrEligibility(csvFilePath, debug)
    else:
        print('Usage: <csv_file_path>', argv[0])
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
