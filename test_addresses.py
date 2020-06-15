import sfr_ftth

def MyAssert(actual, expected, message):
    if actual == expected:
        print("Test passed for {}".format(message))
    else:
        print("Test failed for {}:\n  actual is   '{}',\n  expected is '{}'".format(message, actual, expected))


def TestNormalizePostalAddress():
    test_data = [
    ('1 place du château, 38300 bourgoin jallieu', '1 PLACE DU CHATEAU, 38300 BOURGOIN JALLIEU'),
    ('27 rue du belvédère, 38300 Bourgoin-Jallieu', '27 RUE DU BELVEDERE, 38300 BOURGOIN JALLIEU'),
    ('1 rue du martin pêcheur, 38300 bourgoin jallieu', '1 RUE DU MARTIN PECHEUR, 38300 BOURGOIN JALLIEU'),
    ('1 rue camille saint-saëns, 38300 bourgoin jallieu', '1 RUE CAMILLE SAINT SAENS, 38300 BOURGOIN JALLIEU'),
    ('2 avenue du médipôle, 38300 bourgoin jallieu', '2 AVENUE DU MEDIPOLE, 38300 BOURGOIN JALLIEU')
    ]
    
    print()
    print(TestNormalizePostalAddress.__name__)
    for (realAddress, expectedNormalizedAddress) in test_data:
        actualNormalizedAddress = sfr_ftth.NormalizePostalAddress(realAddress)
        MyAssert(actualNormalizedAddress, expectedNormalizedAddress, realAddress)

def TestAreSimilarPostalAddresses():
    test_data = [
    ('1 place du château, 38300 bourgoin jallieu', '1 PLACE DU CHATEAU, 38300 BOURGOIN JALLIEU'),
    ('27 rue du belvédère, 38300 Bourgoin-Jallieu', '27 RUE DU BELVEDERE, 38300 BOURGOIN JALLIEU'),
    ('1 rue du martin pêcheur, 38300 bourgoin jallieu', '1 RUE DU MARTIN PECHEUR, 38300 BOURGOIN JALLIEU'),
    ('1 rue camille saint-saëns, 38300 bourgoin jallieu', '1 RUE CAMILLE SAINT SAENS, 38300 BOURGOIN JALLIEU'),
    ('2 avenue du médipôle, 38300 bourgoin jallieu', '2 AVENUE DU MEDIPOLE, 38300 BOURGOIN JALLIEU'),
    ('1 rte st marcel bel accueil, 38300 bourgoin jallieu', '1 RTE DE SAINT MARCEL BEL ACCUEIL, 38300 BOURGOIN JALLIEU')
    ]
    
    print()
    print(TestAreSimilarPostalAddresses.__name__)
    for pr in test_data:
        MyAssert(sfr_ftth.AreSimilarPostalAddresses(pr[0], pr[1]), True, pr)

if __name__ == "__main__":
    TestNormalizePostalAddress()
    TestAreSimilarPostalAddresses()