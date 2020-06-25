import requests, json

def NormalizePostalAddress(postalAddress):
    a = ''
    for c in postalAddress.upper().replace("''", "'").replace('  ', ' '):
        if c in '-\'':
            c = ' '
        elif c in 'ÀÂÆ':
            c = 'A'
        elif c == 'Ç':
            c = 'C'
        elif c in 'ÉÈÊË':
            c = 'E'
        elif c in 'ÎÏ':
            c = 'I'
        elif c in 'ÔŒ':
            c = 'O'
        elif c in 'ÙÛÜ':
            c = 'U'
        elif c in '\t\r\n\f':
            c = ''
        a += c
    return a

def GetStringsWordDifference(a, b):
    if len(a[0]) > len(b[0]):
        return [x for x in a.split() if x not in b.split()]
    else:
        return [x for x in b.split() if x not in a.split()]

def AreSimilarPostalAddresses(a1, a2):
    A1 = NormalizePostalAddress(a1)
    A2 = NormalizePostalAddress(a2)
    if A1 == A2:
        return True
    
    for pr in [(' AV ' ,' AVENUE '), (' BD ', ' BOULEVARD '), (' IMP ', ' IMPASSE '), (' RTE ', ' ROUTE '), (' ST ', ' SAINT ')]:
        A1 = A1.replace(pr[0], pr[1])
        A2 = A2.replace(pr[0], pr[1])
        if A1 == A2:
            return True
    
    token1 = A1.split(',')
    token2 = A2.split(',')
    if len(token1) == 2 and len(token1) == len(token2) and token1[1] == token2[1]:
        strDiffs = GetStringsWordDifference(token1[0], token2[0])
        for str in strDiffs:
            if str in ['DE']:
                return True
    return False

def GetIdRa(postalAddress, session, debug = False):
    address = NormalizePostalAddress(postalAddress)
    payload = { 'size': '10', 'input': address }
    if session is None:
        session = requests.Session()
    req = session.get('https://api.sfr.fr/service-eligibility/api/rest/v1/suggestAddress', params=payload)
    if debug: print(req.status_code)
    if req.status_code != 200:
        return None
    resp = req.json()
    if debug: print(json.dumps(resp, indent=4))
    if resp['state'] != 'COMPLETE':
        return None
    if 'data' not in resp:
        return None
    ids = [x[0] for x in resp['data'].items() if AreSimilarPostalAddresses(postalAddress, x[1])]
    if len(ids) != 1:
        return None
    return ids[0]
    
def EligibilityStatusToString(status):
    if status == 1 or status == 3304:
        return 'VOUS ÊTES ÉLIGIBLE AUX OFFRES FIBRE DE SFR'
    elif status == 1101 or status == 3101:
        return 'La fibre de SFR est en cours de déploiement dans votre ville'
    elif status == 1102 or status == 3102 or status == 3103:
        return 'La fibre de SFR est en cours de déploiement dans votre quartier'
    elif status == 0:
        return 'La fibre de SFR est en cours de déploiement dans votre rue'
    elif status == 666:
        return 'Une difficulté a été rencontrée sur le raccordement fibre de votre adresse'
    elif status == 3302 or status == 3401 or status == 3402:
        return 'Les équipes SFR réalisent actuellement les travaux de raccordement de votre quartier à la fibre'
    elif status == 100:
        return 'Votre adresse est temporairement inéligible à la fibre'
    elif status in [2, 1401, 2101, 2102, 3403]:
        return 'VOUS ÊTES ÉLIGIBLE AUX OFFRES TRÈS HAUT DÉBIT (cable) DE SFR'.format(status)
    else:        
        return 'status inconnu: {} !'.format(status)
    
def GetEligibilityByIdRa(idRa, session, debug = False):
    payload = { 'idRa': idRa }
    if session is None:
        session = requests.Session()
    req = session.get('https://api.sfr.fr/service-eligibility/api/rest/v1/eligibilityByIdRa', params=payload)
    if debug: print(req.status_code)
    if req.status_code != 200:
        return None
    resp = req.json()
    if debug: print(resp['state'])
    if resp['state'] != 'COMPLETE':
        return None
    if debug: print(json.dumps(resp['data'], indent=4))    
    thdLine = resp['data']['eligibilityLookup']['installationAddresses'][0]['installationTHD']['thdLine']
    if debug: print(thdLine)
    status = thdLine['horizontalEligibilityStatus']
    eligible = thdLine['horizontalEligibility']
    workInProgress = thdLine['workInProgress']
    return (status, eligible, workInProgress)

def GetEligibilityByPostalAddress(postalAddress, session = None, debug = False):
    idRa = GetIdRa(postalAddress, session, debug)
    if idRa is None:
        return (-1, False, False)
    res = GetEligibilityByIdRa(idRa, session, debug)
    if res is None:
        return (-2, False, False)
    return res

def GetEligibilityByPostalAddress2(args):
    try:
        (postalAddress, session, debug) = args
        res = GetEligibilityByPostalAddress(postalAddress, session, debug)
        if res[0] == -2:
            res = GetEligibilityByPostalAddress(postalAddress, session, debug) # try again I've noticed there are spurious failures
        return res
    except:
        return (-3, False, False)