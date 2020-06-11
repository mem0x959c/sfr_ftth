import sys, requests, multiprocessing
import sfr_ftth

def GetUniqueAddressesFromTxtFile(txtFilePath):
    with open(txtFilePath, encoding='utf-8') as f:
        lines = f.readlines()
    addresses = [sfr_ftth.NormalizePostalAddress(a) for a in lines]
    addresses.sort()
    return addresses
    
def PrintSfrEligibilityFromTxtFile(txtFilePath, debug):
    addresses = GetUniqueAddressesFromTxtFile(txtFilePath)
    session = requests.Session()
    with multiprocessing.Pool(processes=16) as pool:
        results = pool.starmap(sfr_ftth.GetEligibilityByPostalAddress2, [(a, session, debug) for a in addresses])
    for r, a in zip(results, addresses):
        print('{}, {}'.format(a, r[1]))

if __name__ == "__main__":    
    debug = False
    if len(sys.argv) >= 2:
        txtFilePath = sys.argv[1]
        PrintSfrEligibilityFromTxtFile(txtFilePath, debug)
    else:
        print('Usage: {} <txt_file_path>'.format(sys.argv[0]))
        sys.exit(1)
