import sys, requests, multiprocessing
import sfr_ftth

def GetAddressesFromTxtFile(txtFilePath):
    with open(txtFilePath, encoding='utf-8') as f:
        lines = f.readlines()
    addresses = [sfr_ftth.NormalizePostalAddress(a) for a in lines]
    return addresses
    
def PrintSfrEligibilityFromTxtFile(txtFilePath, debug):
    addresses = GetAddressesFromTxtFile(txtFilePath)
    session = requests.Session()
    with multiprocessing.Pool(processes=20) as pool:
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
    if len(sys.argv) >= 2:
        txtFilePath = sys.argv[1]
        debug = False
        PrintSfrEligibilityFromTxtFile(txtFilePath, debug)
    else:
        print('Usage: {} <txt_file_path>'.format(sys.argv[0]))
        sys.exit(1)
