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
    if status == 1:
        return 'VOUS ÊTES ÉLIGIBLE AUX OFFRES FIBRE DE SFR'
    elif status == 1101 or status == 3101:
        return 'La fibre de SFR est en cours de déploiement dans votre ville'
    elif status == 1102:
        return 'La fibre de SFR est en cours de déploiement dans votre quartier'
    elif status == 0:
        return 'La fibre de SFR est en cours de déploiement dans votre rue'
    elif status == 666:
        return 'Une difficulté a été rencontrée sur le raccordement fibre de votre adresse'
    elif status == 3402:
        return 'Les équipes SFR réalisent actuellement les travaux de raccordement de votre quartier à la fibre'
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
    return (status, EligibilityStatusToString(status))

def GetEligibilityByPostalAddress(postalAddress, session = None, debug = False):
    idRa = GetIdRa(postalAddress, session, debug)
    if idRa is None:
        return (-1, 'Addresse inconnue: {}'.format(postalAddress))
    res = GetEligibilityByIdRa(idRa, session, debug)
    if res is None:
        return (-1, 'Erreur pour l\'adresse: {}, IdRa {}'.format(postalAddress, idRa))
    return res

def GetEligibilityByPostalAddress2(args):
    try:
        (postalAddress, session, debug) = args
        return GetEligibilityByPostalAddress(postalAddress, session, debug)
    except:
        return (-1, 'Erreur pour l\'addresse: {}'.format(postalAddress))