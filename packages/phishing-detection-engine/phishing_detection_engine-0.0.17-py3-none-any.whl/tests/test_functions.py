from phishing_detection_engine import functions

# test case to check phishtank varified phish
def test_phishTankAPI():
    assert functions.phishingDetection().isUrlPhishing("http://verifycasi-facebooks.gq/") == "Phishing URL"

# test case to check abuseIP API
def test_abuseIPAPI():
    assert functions.phishingDetection().isUrlPhishing("58.220.56.64") == "Phishing URL"