import sfr_ftth

def TestNormalizePostalAddress():
    test_normalize_address_data = [
    ('1 place du château, 38300 bourgoin jallieu', '1 PLACE DU CHATEAU, 38300 BOURGOIN JALLIEU'),
    ('27 rue du belvédère, 38300 Bourgoin-Jallieu', '27 RUE DU BELVEDERE, 38300 BOURGOIN JALLIEU'),
    ('1 rue du martin pêcheur, 38300 bourgoin jallieu', '1 RUE DU MARTIN PECHEUR, 38300 BOURGOIN JALLIEU'),
    ('1 rue camille saint-saëns, 38300 bourgoin jallieu', '1 RUE CAMILLE SAINT SAENS, 38300 BOURGOIN JALLIEU'),
    ('2 avenue du médipôle, 38300 bourgoin jallieu', '2 AVENUE DU MEDIPOLE, 38300 BOURGOIN JALLIEU')
    ]

    for (readAddress, expectedNormalizedAddress) in test_normalize_address_data:
        actualNormalizedAddress = sfr_ftth.NormalizePostalAddress(readAddress)
        if actualNormalizedAddress == expectedNormalizedAddress:
            print("Test passed for NormalizePostalAddress('{}')".format(readAddress))
        else:
            print("Test failed for NormalizePostalAddress('{}'): actual is '{}', expected  is '{}'".format(readAddress, actualNormalizedAddress, expectedNormalizedAddress))

if __name__ == "__main__":
    TestNormalizePostalAddress()
    