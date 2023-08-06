import requests
import json
import IPy
import base64
from bs4 import BeautifulSoup
import csv
import os.path
from IPy import IP
from tld import get_tld
import whois
import datetime
import favicon
import re
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import numpy as np
import os


class phishingDetection:

    def __isGenuineABUSEIP(self, url_to_check):
        # Defining the api-endpoint
        url = 'https://api.abuseipdb.com/api/v2/check'

        headers =  {
        'Accept': 'application/json',
        'Key': 'b9e8e8c88f0c42cb256e6cc0c6970ee9334ac1bfa97dfd57421b3402dedbab3c9a2ed5cddba06ff0'
        }

        # check if given parameter is already an IP address
        try:
            IPy.IP(url_to_check)
            ip_to_check = url_to_check
        except:
            try:
                resp = requests.get(url_to_check, stream=True)
                ip_to_check = resp.raw._fp.fp.raw._sock.getpeername()[0]
            except:
                return -2

        # getting values for query
        querystring = {
            'ipAddress' : ip_to_check,
            'maxAgeInDays': '365'
        }
        try:
            response = requests.request(method='GET', url=url, headers=headers, params=querystring)

            # Formatted output
            decodedResponse = json.loads(response.text)
            json.dumps(decodedResponse, sort_keys=True, indent=4)
            score = decodedResponse.get("data").get("abuseConfidenceScore")
            if score <= 25:
                return 1
            elif 25 < score <= 60:
                return 0
            elif 60 < score <= 100:
                return -1
        except:
            return -2


    def __isGenuinePhishTank(self, url_to_check):
        # Defining the api-endpoint
        url = 'https://checkurl.phishtank.com/checkurl/'

        post_data = {
                'url': base64.b64encode(url_to_check.encode("utf-8")),
                'format': 'json',
                'app_key': '21332de8eba6d0efa8134aeb69867f3b626b2fc3bfc82ead0c1a0a6d4bc3cecb'
            }
        try:
            response = requests.post(url, data=post_data)
            data = response.json()
            to_return = data.get("results").get("valid")
            if to_return is not None:
                if to_return == False:
                    return 0
                else:
                    return -1
            else:
                return 0
        except:
            return -2


    def __give_domain_part_of_website(self, url_to_check):
        temp_url = str(url_to_check)
        without_http = ""
        without_www = ""
        # remove http if exists
        if temp_url.find("http://") != -1:
            temp_1 = temp_url.partition("http://")
            without_http = temp_1[2]

        # remove https if exists
        elif temp_url.find("https://") != -1:
            temp_2 = temp_url.partition("https://")
            without_http = temp_2[2]

        # remove www if exists
        with_www = without_http
        if with_www.find("www.") != -1:
            temp_3 = with_www.partition("www.")
            without_www = temp_3[2]
        else:
            without_www = without_http
        my_res = get_tld(url_to_check, as_object=True)
        myTld = my_res.tld
        if myTld.find(".") != -1:
            combineTld = myTld.rpartition(".")
            ccTld = combineTld[1] + combineTld[2]
        else:
            ccTld = str('.') + myTld
        combined_domain = without_www.partition(ccTld)
        final_domain = combined_domain[0]
        return final_domain


    def __is_url_length_friendly(self, url_to_check):  # feature 2 "URL length good or not"
        curr_length = len(url_to_check)
        if curr_length <= 60:
            print("Legitimate URL feature: 'Length of URL'")
            return 1
        else:
            print("Phishing URL feature: 'Length of URL'")
            return -1


    # helper for ip_address checking feature
    def __is_ip_address_hex_coded(self, url_to_check):
        number_of_times = 0
        length = len(url_to_check)
        length -= 1
        # parse the url to see 0x in it
        for x in range(length):
            if url_to_check[x] == "0" and url_to_check[x+1] == "x":
                number_of_times += 1
        return number_of_times

    
    def __is_url_shortening_service_used(self, old_url, new_url):
        old_url_length = len(old_url)
        new_url_length = len(new_url)
        if new_url_length-old_url_length > 6:
            # temp sol
            print("Phishing URL feature: 'Shortening service'")
            return -1
        else:
            print("Legitimate URL feature: 'Shortening service'")
            return 1


    def __is_url_having_at_the_rate_symbol(self, url_to_check):
        length = len(url_to_check)
        # parse the url to see @ in it
        for x in range(length):
            if url_to_check[x] == "@":
                print("Phishing URL feature: '@ symbol usage'")
                return -1
        print("Legitimate URL feature: '@ symbol usage'")
        return 1


    def __is_position_double_slash_good(self, url_to_check):
        temp_url = str(url_to_check)
        indexOf = temp_url.find("//")
        if indexOf > 6:
            print("Phishing URL feature: 'index of //'")
            return -1
        else:
            print("Legitimate URL feature: 'index of //'")
            return 1


    def __tell_if_dash_symbol_present(self, url_to_check):
        try:
            my_res = get_tld(url_to_check, as_object=True)
            myDomain = my_res.domain
            indexOf = myDomain.find("-")
            if indexOf == -1:
                print("Legitimate URL feature: 'use of - in Domain'")
                return 1
            else:
                print("Phishing URL feature: 'use of - in Domain'")
                return -1

        except Exception as e:
            print(e)
            print(
                "<<<------------------------Exception Feature: double dash-------------------------->>>")
            print("Suspicious URL feature: 'use of - in Domain'")
            return 0


    def __tell_sub_domain_and_multilevel_domain(self, url_to_check):
        final_domain = self.__give_domain_part_of_website(url_to_check)
        number_of_dots_in_domain = final_domain.count(".")
        if number_of_dots_in_domain == 1 or number_of_dots_in_domain == 0:
            print("Legitimate URL feature: 'Number of Dots in Domain'")
            return 1
        elif number_of_dots_in_domain == 2:
            print("Suspicious URL feature: 'Number of Dots in Domain'")
            return 0
        else:
            print("Phishing URL feature: 'Number of Dots in Domain'")
            return -1


    def __tell_is_domain_registered(self, domain_name):
        """
        A function that returns a boolean indicating
        whether a `domain_name` is registered
        """
        try:
            whois_info = whois.whois(domain_name)
            # print(whois_info)

            # whois_info = ipwhois.IPWhois(domain_name)
            # print(whois_info.registrar)
        except Exception:
            print("<<<------------------------Exception Feature: is domain registered-------------------------->>>")
            return False
        else:
            return bool(whois_info.domain_name)


    def __tell_is_registrar_well_known(self, domain_name):
        registrars = ('GigiCert', 'GeoTrust', 'The SSL Store', 'Verisign', 'GoDaddy', 'NortonLifeLock', 'Thawte',
                    'Comodo Cybersecurity', 'GlobalSign', 'Comodo', 'CA/Browser Forum', 'Network Solutions',
                    'Identrust', 'Entrust', 'StartCom', 'DigiNotar', 'Certificate Authority Security Council',
                    'HTTP Public Key Pinning', 'SAFE-BioPharma Association', 'ACTALIS S.p.A.', 'CAcert.org', 'DNSimple',
                    'RSA', 'Buypass', 'Sectigo Inc.', 'Symantec', 'RapidSSLonline', 'Entrust Datacard',
                    'SecureTrust', 'SSL.com', 'GoGetSSL', 'AlphaSSL', 'NameCheap', 'MarkMonitor Inc.',
                    'MarkMonitor, Inc.', 'RegistrarSafe, LLC', 'eName Technology Co.,Ltd.', 'ABOVE.COM PTY LTD.',
                    'CSC Corporate Domains', 'R01-RU', 'SNAPNAMES 57, LLC', 'Letshost.ie', 'eNom, Inc.', 'NameCheap, Inc',
                    'Internet Invest, Ltd. dba Imena.ua', 'Whois Networks Co., Ltd.', 'REGRU-SU', 'NAMECHEAP INC',
                    'DropCatch.com 1054 LLC', 'Serbia Broadband - Srpske kablovske mreže', 'Safenames Ltd.',
                    'Nom-IQ Limited t/a Com Laude [Tag = NOMIQ]', 'Xiamen 35.Com Technology Co., Ltd.',
                    'Hetzner Online GmbH', 'RD-RU', 'Ascio Technologies, Inc', 'GMO Internet, Inc. d/b/a Onamae.com',
                    'Bizcn.com, Inc.', 'Pair Domains', 'Best Drop Names LLC', 'One.com A/S', 'DomainPeople, Inc.',
                    'MarkMonitor Inc', 'Free Drop Zone LLC', 'NETIM', 'Onlinenic Inc', 'HOGAN LOVELLS (PARIS) LLP',
                    'Savethename.com LLC', 'DropCatch.com 558 LLC', 'GoDaddy.com, LLC', 'Domansverige AB',
                    'Coöperatieve Rabobank U.A.', 'Digital Transformation Agency – QLD',
                    'Sree Jain Infotech dba bookandhost.com', 'INSTRA CORPORATION PTY. LTD.',
                    'Nics Telekomunikasyon Ticaret Ltd. Sti.', 'home.pl S.A.', 'DropCatch.com 1071 LLC',
                    'A.R.C. Informatique Inc.', 'REGTIME LTD.', '厦门易名科技股份有限公司', 'SNAPNAMES 17, LLC',
                    'Irideos s.p.a.', 'DOMAIN TRAIN, INC.', 'ST Registry', 'GoDaddy.com', 'ТОВ "НІК.ЮЕЙ"',
                    'ZNet Technologies Private Limited', 'Global Village GmbH', 'Webdev SRL',
                    'MarkMonitor Inc. ( https://nic.at/registrar/434 )', 'easyDNS Technologies, Inc.', 'OVH',
                    'DHH.si d.o.o.', '广东时代互联科技有限公司', 'PT Ardh Global Indonesia', 'ANNULET, INC',
                    'Coral Reef Domains LLC', 'Tucows (Australia) Pty Ltd trading as OpenSRS', '101 Domain',
                    'British Telecommunications plc [Tag = BTWEBSERVICES]', 'OVH sas', 'DropCatch.com 415 LLC',
                    'dotNice Italia s.r.l.', 'Gandi Services Inc., Gandi SAS', 'Dominiok di Laura De Luca', 'Gandi SAS',
                    'MarkMonitor Corporate Services Inc', 'DropCatch.com 891 LLC', 'G-Server d.o.o.',
                    'Ne.W.S. New Web Solutions s.r.l.', 'TMG Landelijke Media B.V.', 'Freshbreweddomains.com LLC',
                    'Firstround Names LLC', '北京新网数码信息技术有限公司', 'REALTIME REGISTER B.V.', 'Google LLC',
                    'Safenames Ltd', 'Namespro Solutions Inc.', '北京光速连通科贸有限公司', 'Neudomains Digital, S.L.',
                    'REG-MOJEID', 'Entorno Digital, S.A.', '123-Reg Limited', 'PT INDOSAT MEGA MEDIA',
                    'DropCatch.com 628 LLC', 'Reg2C.com Inc.', 'Center of Ukrainian Internet Names (UKRNAMES)',
                    '赛尔网络有限公司', 'GANDI', 'DomainSite, Inc.', 'CSC Corporate Domains Inc.', 'Network Solutions, LLC',
                    'DomainContext, Inc.', 'SCALEWAY', 'News and Media Holding a.s.', '厦门三五互联科技股份有限公司',
                    'Glide Slope Domains, LLC', 'RUCENTER-SU', 'Cosmotown, Inc.',
                    'TUCOWS Inc t/a TUCOWS [Tag = TUCOWS-CA]', 'UNIREGISTRAR CORP', 'Telecom Italia s.p.a.',
                    'Namecheap Inc.', 'Kementerian Komunikasi dan Informatika', 'Slow Motion Domains LLC',
                    'PSI-Japan Inc.', 'BigRock Solutions Ltd.', 'Communigal Communication Ltd',
                    'Beijing Innovative Linkage Software Service Co. Ltd', 'DANESCO TRADING LTD', 'NameCheap, Inc.',
                    'Zone Media OÜ', 'Porkbun LLC', 'ORDIPAT', 'Edomains LLC', 'Digital Registra',
                    'Soluciones Corporativas IP, SLU', 'NETIM SARL', 'Sarek', 'Entorno Digital',
                    's IT Solutions AT Spardat GmbH ( https://nic.at/registrar/388 )',
                    'Interdominios, Inc.', 'INDOREG', 'RegistryGate GmbH', 'AVENIR TELEMATIQUE',
                    'DropCatch.com 1184 LLC', 'Whois Corp.(http://whois.co.kr)', 'REGISTER S.P.A.', 'NET-CHINESE',
                    'Webcentral Group Ltd. trading as Melbourne IT', 'Threepoint Domains LLC', 'Hosting Concepts B.V.',
                    'Ports Group AB', 'eNom LLC [Tag = ENOM]', 'ABN Amro Bank N.V.', 'DomainRoyale.com LLC',
                    'Moniker Online Services LLC', 'Servizi Internet S.r.l.', 'KOREA SERVER HOSTING INC.',
                    'Blue Spark Limited t/a Blue Spark [Tag = BLUESPARK]', 'MasterofMyDomains.net LLC', 'TFN',
                    'Markmonitor Inc', 'Domain The Net Technologies Ltd', 'Onlinenic Inc', 'Corporation Service Company',
                    'Thirdroundnames LLC', 'Register NV dba Register.eu', 'IGNUM s.r.o.', 'DropCatch.com 940 LLC',
                    'Telia Eesti AS', 'Netpia.com, Inc.', 'Tuonome Registrar S.r.l.',
                    'InterNetX GmbH ( https://nic.at/registrar/80 )', 'CPS-Datensysteme GmbH', 'DYNADOT LLC',
                    'REG-INTERNET-CZ', 'Tiscali Italia S.p.a.', 'PSI-Japan, Inc.', 'NameSecure L.L.C.',
                    'Registration Technologies, Inc.', 'R01-SU', 'NamePal.com #8023, LLC', 'DropCatch.com 376 LLC',
                    'NIC .PE', 'SilverbackDomains.com LLC', 'APT', 'united domains AG', 'IT.Gate S.p.A.',
                    'DropCatch.com 864 LLC', 'Central Comercializadora de Internet S.A.S',
                    'Markmonitor Inc. t/a MarkMonitor Inc. [Tag = MARKMONITOR]', 'CV. Jogjacamp', 'SNAPNAMES 41, LLC',
                    'DomainTheNet.com', 'KEY-SYSTEMS GmbH', 'Sav.com, LLC', 'DropCatch.com 1235 LLC',
                    'dhosting.pl Sp. z o.o.', 'Tool.Domains', 'Name.com, Inc.', 'Dynadot5 LLC',
                    'Web Werks India Pvt. Ltd. D/B/A ZenRegistry.com', 'Atak Domain', 'CSC', 'INWX GmbH & Co. KG.',
                    'HINET', 'Domaintimemachine.com LLC', 'Nordreg AB', 'eNOM, Inc', 'InternetX', 'Everyones Internet,'
                    'LLC dba SoftLayer', 'India Links Web Hosting Pvt Ltd', 'TOMAS',
                    '4D Data Centres Limited [Tag = 49REG]', 'PCHOME', 'Vautron Rechenzentrum AG',
                    'Net 4 India Limited', 'Shinjiru MSC Sdn Bhd', 'TUCOWS, INC.', 'Key-Systems GmbH', 'REGRU-RU',
                    'Lexsynergy Limited', 'DNC Holdings, Inc', 'Hong Kong Domain Name Registration Company Limited',
                    'Copper Domain Names LLC', 'Desert Sand Domains, LLC', 'Israel Internet Association ISOC-IL',
                    'SNAPNAMES 63, LLC', 'Instra Corporation (www.instra.com)', 'NameCheap', 'Safebrands SAS',
                    'DropCatch.com 1322 LLC', 'RELCOMHOST-RU', 'Jagat Informasi Solusi (int)', 'Infomaniak Network SA',
                    'Aegean Domains LLC', 'NameWeb BVBA', '1 Api GmbH', 'Sify Limited', 'GIP RENATER', 'REG-TZNIC',
                    'Megazone(http://HOSTING.KR)', 'Xiamen Chinasource Internet Service Co.,Ltd.',
                    'CommuniGal Communication Ltd.', 'Sav.com', 'Dynadot14 LLC', 'DOMENUS-RU', 'DropCatch.com 1279 LLC',
                    '浙江贰贰网络有限公司', 'BigRock Solutions Ltd', 'Dynadot3 LLC', 'IP Twins SAS',
                    'THE NAMEIT CORPORATION DBA NAMESERVICES.NET', 'P.A. Viet Nam Company Limited', 'MARKMONITOR Inc.',
                    'NINET Company d.o.o.', 'NPO', 'ERANET INTERNATIONAL LIMITED', 'DreamHost, LLC',
                    'Akky (Una division de NIC Mexico)', 'Sav.com LLC', 'DomainTact LLC',
                    'Marcaria.com International, Inc.', '101domain GRS Limited', '101domain GRS Ltd', 'Misto Ltd.',
                    'Metaname', 'DropCatch.com 774 LLC', 'NamePal.com #8026, LLC', 'Fastweb s.p.a.',
                    'DropCatch.com 1384 LLC', 'Reliable Software, Ltd', 'Endurance Domains Technology LLP',
                    'DropCatch.com 591 LLC', 'eNom, LLC', 'abcdomain (ABCDomain LLC)', 'IHS Telekom, Inc',
                    'Eurodns S.A.', 'NICS Telekomunikasyon A.S.', 'Launchpad.com Inc.', 'REGTIME-RU', 'LiveDns Ltd',
                    'Register.com, Inc.', 'DropJump.com, LLC', 'DomainContext Inc.', '101domain, Inc.', 'DYNADOT, LLC',
                    'Name SRS AB', 'Arcanes Technologies', 'Yleisradio', 'ARDIS-RU', 'New Frontier, Inc.',
                    'Digital Transformation Agency', 'Genesys Informatica S.r.l.',
                    'Chengdu west dimension digital technology Co., LTD',
                    'Sibername Internet and Software Technologies Inc.',
                    'Nameshield SAS', 'Blacknight Internet Solutions Ltd.',
                    'ERNET India', 'ONLINE SAS', 'Soluciones Corporativas IP, SL',
                    'CSC CORPORATE DOMAINS INC.', 'PT Registrasi Nama Domain', 'nazwa.pl sp. z o.o.', 'Domraider SAS',
                    'MarkMonitor', 'Domain Robot', 'TLD Registrar Solutions Ltd', 'Blue Ltd.', 'OVH SAS', 'TWNIC',
                    'Webnames.ca Inc.', 'Tucows Inc.', 'Sanoma', 'PDR Ltd.', 'NAMESHIELD',
                    'EDUCATION SERVICES AUSTRALIA LIMITED', 'InsaneNames LLC',
                    'Web Commerce Communications Limited dba WebNic.cc', 'Dotname Korea Corp.',
                    'Gabia, Inc.(http://www.gabia.co.kr)', 'COREhub, S.R.L.', 'FBS Inc.', 'CJSC REGISTRAR R01',
                    'SNAPNAMES 31, LLC', 'Markmonitor', 'URL SOLUTIONS INC.', 'National Informatics Centre',
                    'Domainwards.com LLC', 'LA DomainNames LLC', 'Todaynic.com, Inc.', 'Webglobe - Yegon, s. r. o.',
                    'RCS & RDS SA', 'TLDS L.L.C. d/b/a SRSPlus', 'PSI-USA, Inc. dba Domain Robot',
                    'Register S.p.a.', 'NameSilo, LLC', 'SAFENAMES LTD', 'REG-IGNUM', 'DNSPod, Inc.', 'MarkMonitor Inc.',
                    'Alibaba Cloud Computing Ltd. d/b/a HiChina (www.net.cn)', 'MidWestDomains, LLC', 'Loopia AB',
                    'Netregistry Pty Ltd', 'Authentic Web Inc.', 'SHANGHAI BEST ORAY INFORMATION S&T CO., LTD.',
                    'www.NameSRS.com', 'Launchpad, Inc. (HostGator)', 'Webair Internet Development', 'CentralNic Ltd',
                    'Easyspace Ltd.', 'ENDURANCE', 'EURODNS S.A.', 'Chengdu West Dimension Digital Technology Co., Ltd.',
                    'NIC-VE', 'CV. Rumahweb Indonesia', 'Charleston Road Registry Billable', 'Aftermarket.pl Limited',
                    'Arsys Internet, S.L. dba NICLINE.COM', 'GANDI SAS', 'Cybercom', '北京神州长城通信技术发展中心',
                    'WEBNAMES.CA INC', 'Gabia, Inc.', 'RTL Nederland B.V.', 'Tucows Domains Inc.', 'Fournetix s.r.o.',
                    'Instra Corporation Pty Ltd.', 'humbly, LLC', 'Rijksoverheid', 'CBN Registrar', 'Rebel.ca', 'Ascio',
                    'Beijing Guoxu Network Technology Co. LTD', 'InternetX GmbH', 'OnlineNIC, Inc.', 'ITnet s.r.l.',
                    'Panservice s.a.s.', 'NOMINALIA INTERNET S.L.', 'Dinahosting s.l.', 'GMO INTERNET, INC.',
                    'MarkMonitor International Canada Ltd.', 'OVH, SAS', 'domene.si', 'ORANGE', 'REG-ACTIVE24',
                    'GiDiNet di Iunco Daniele Antonio', 'NamePal.com #8016, LLC', 'DropCatch.com 577 LLC',
                    'Dynadot17 LLC', '1&1 IONOS SE', 'Prolocation B.V.', 'Dynadot LLC', '烟台帝思普网络科技有限公司',
                    'REG-MARKMONITOR', 'ТОВ "Геонiк Нет"', 'NIC Chile', 'Alphanet sp. z o.o.', 'SALENAMES-RU',
                    'Amazon.com, Inc. t/a Amazon.com, Inc. [Tag = AMAZON-COM]', 'Consulting Service Sp. z o.o.',
                    'Domainhawks.net LLC', 'EuroDNS SA', 'Key-Systems LLC', 'Registrar NIC .DO (midominio.do)',
                    'Hogan Lovells International LLP', 'easyDNS Technologies Inc.', 'Ascio Technologies Inc. - DK Branch',
                    'EuropeanConnectionOnline.com LLC', 'ENOM, INC.', 'Register.mu',
                    'Beijing Brandma International Networking Technology Ltd.', 'Amazon Registrar, Inc.', 'DREAMHOST',
                    'Ascio Technologies Inc. Denmark – filial af Ascio Technologies Inc. USA t/a Ascio Technologies inc '
                    '[Tag = ASCIO]', 'Go France Domains, LLC', 'GoDaddy', 'H88 S.A.', 'Gabia Inc.', 'IKOULA NET',
                    'Blue Angel Domains LLC', 'nicar', 'CCI REG S.A.', 'T.H.NIC Co., Ltd.', 'Namecheap, Inc.',
                    'DonDominio (SCIP)', 'Tucows.com Co.', 'SHANGHAI MEICHENG TECHNOLOGY INFORMATION DEVELOPMENT CO., '
                                                            'LTD.', 'Cronon AG', 'BRANDSIGHT, INC.', 'Rebel.ca Corp.',
                    'British Broadcasting Corporation [Tag = BBC]', 'SNAPNAMES 38, LLC', 'CSC Corp Domains', 'Via',
                    'SNAPNAMES 7, LLC', 'DREAMSCAPE NETWORKS INTERNATIONAL PTE LTD', 'Netregistry Wholesale Pty Ltd',
                    'ARSENAL-D', 'Hosting Concepts B.V. d/b/a Openprovider', 'GKG.NET, INC.', 'Vitalwerks Internet '
                                                                                                'Solutions, '
                                                                                                'LLC / No-IP.com',
                    'TIERRANET INC. DBA DOMAINDISCOVER', 'NetEarth One, Inc.', '北京国旭网络科技有限公司', 'TELEFÓNICA UK LIMITED ['
                                                                                                'Tag = '
                                                                                                'O2-HOLDINGS-LTD]',
                    'Registrar of domain names REG.RU LLC', 'CloudFlare, Inc.', 'DropCatch.com 425 LLC',
                    'Japan Registry Services Co.,Ltd.(JPRS)', 'AZ.pl Sp. z o.o.', 'Whois Corp.', 'premium.pl Sp. z '
                                                                                                'o.o.', '成都飞数科技有限公司',
                    'SINGNET PTE LTD', 'Websupport, s.r.o.', 'Vodafone Limited [Tag = VODAFONE]', 'NIC-REG1', 'Axtel, '
                                                                                                                'S.A.B. '
                                                                                                                'de '
                                                                                                                'C.V.',
                    'NETWORK SOLUTIONS, LLC.', '北京万维通港科技有限公司', 'NORDNET', 'Arq Group Limited doing business as '
                                                                            'Melbourne IT',
                    '厦门商中在线科技股份有限公司（原厦门商中在线科技有限公司）', 'Inames Co., Ltd.(http://www.inames.co.kr)', 'REG-GRANSY',
                    'SILCA', 'Rebel.com', 'INWX GmbH & Co. KG', 'BEELINE-RU', 'Genious Communications SARL/AU',
                    'SNAPNAMES 58, LLC', 'Ringier Axel Springer Slovakia, a. s', 'Namecheap', 'Domain Gold Zone LLC',
                    '中企动力科技股份有限公司', 'Domain.com, LLC', 'PlanetHoster', 'Xin Net Technology Corporation',
                    '北京中科三方网络技术有限公司', 'www.NAMES.plus', 'DropCatch.com 1167 LLC', 'Société Française du Radiotéléphone '
                                                                                    '- SFR', 'Above.com Pty Ltd.',
                    'Zoznam, s.r.o.', 'SWAN, a.s.', 'SNAPNAMES 29, LLC', 'InterNetx GmbH [Tag = INTERNETX-DE]',
                    'Net-Chinese Co., Ltd.', 'Internet Domain Service BS Corp', 'Uniregistrar Corp t/a Uniregistry [Tag '
                                                                                '= UNIREG]', 'Total Web Solutions '
                                                                                            'Limited trading as '
                                                                                            'TotalRegistrations',
                    'Internet Domain Service BS Corp.', 'SafeNames Ltd', 'GoDaddy.com, LLC. [Tag = GODADDY]',
                    'ING BANK N.V.', 'Cloudflare, Inc.', 'PT Biznet Gio Nusantara', 'ResellerCamp',
                    'EPAG domainservices GmbH', 'DropCatch.com 1239 LLC', 'ТОВ "Інтернет Інвест"', 'Burnsidedomains.com '
                                                                                                    'LLC', 'GRANSY S.R.O '
                                                                                                            'D/B/A '
                                                                                                            'SUBREG.CZ',
                    'NICENIC INTERNATIONAL GROUP CO., LTD', 'Tecnologia, Desarrollo Y Mercado S. de R.L. de C.V.',
                    'dotFM', 'NameCase GmbH', 'BRANDON GRAY INTERNET SERVICES INC. (dba "NameJuice.com")', '1API GmbH',
                    'UdomainName.com LLC', 'Wingu Networks, S.A. de C.V.', 'RegistrarSafe, LLC', 'Wild West Domains, '
                                                                                                'LLC', 'Koreacenter '
                                                                                                        'co.,Ltd',
                    'Agnat Sp. z o.o.', 'Megazone Corp., dba HOSTING.KR', 'SNAPNAMES 6, LLC', 'Domainjungle.net LLC',
                    'Supermedia sp. z o.o.', 'ICI - Registrar', 'InterNetX GmbH', 'Abbey Road Domains LLC',
                    'FindYouADomain.com LLC', 'Tiger Technologies LLC', '成都西维数码科技有限公司', 'Registrar.eu', 'Consortium '
                                                                                                        'GARR',
                    'united-domains AG', 'TPP Wholesale Pty Ltd', 'REG-CZNIC', 'Mesh Digital Limited', '123-Reg Limited '
                                                                                                        't/a 123-reg ['
                                                                                                        'Tag = '
                                                                                                        '123-REG]',
                    'Mps Infotecnics Limited', '! #1 Host Canada, LLC', 'Web Lovers AB', 'DropCatch.com 1094 LLC',
                    'CSC CORPORATE DOMAINS INC', 'DropCatch.com 993 LLC', 'Dotname Korea Corp.('
                                                                            'http://www.dotname.co.kr)', 'InterSpace '
                                                                                                        'Ltd',
                    'MARKMONITOR INC.', 'Epik, Inc.', 'Hostopia', 'MESH DIGITAL LIMITED', 'Jiangsu Bangning Science & '
                                                                                            'technology Co. Ltd.',
                    'Namebay', 'PortsGroup AB', 'ACTIVE 24, s.r.o.', 'Sssasss, LLC', 'iwantmyname', 'ТОВ "Центр '
                                                                                                    'Інтернет-Імен '
                                                                                                    'України"',
                    '阿里云计算有限公司（万网）', 'eName Technology Co., Ltd.', 'No registrar listed.  This domain is directly '
                                                                    'registered with Nominet.', 'Hogan Lovells (Paris) '
                                                                                                'LLP',
                    'West263 International Limited', 'DropCatch.com 746 LLC', 'BT Italia s.p.a.', 'URL Solutions, '
                                                                                                    'Inc.',
                    'Instra Corporation Pty Ltd', 'CINECA Consorzio Interuniversitario', 'DotArai Co., Ltd.',
                    'FastDomain Inc.', 'DomainLadder LLC', 'Markmonitor, Inc.', 'MARKMONITOR INC', 'CSC Corporate '
                                                                                                    'Domains, '
                                                                                                    'Inc [Tag = '
                                                                                                    'CSC-CORP-DOMAINS]',
                    'Aruba s.p.a.', '北京新网互联科技有限公司', 'CSC Corporate Domains, Inc.', 'CSC CORPORATE DOMAINS, INC.',
                    'EUROIX SP. Z O.O.', 'IDC Frontier Inc.', 'NameScout Corp.', 'DropCatch.com 1240 LLC',
                    'Open Contact, Ltd', 'CSC Corporate Domains, Inc. ( https://nic.at/registrar/533 )', 'NAMECHEAP',
                    'SPIE CLOUD SERVICES', 'MarkMonitor, Inc.', 'Domainming', 'NOM-IQ Ltd dba Com Laude',
                    'EPAG Domainservices GmbH', 'Xiamen 35.Com Technology Co., Ltd', 'ALMIC OÜ', 'Loopia Group AB',
                    'Digital Transformation Agency – WA', 'Register SPA', 'Safenames Ltd [Tag = SAFENAMES]',
                    'Regional Network Information Center, JSC dba RU-CENTER', 'Internic.ca Inc.', 'BEIJING SANFRONT '
                                                                                                    'INFORMATION '
                                                                                                    'TECHNOLOGY CO., '
                                                                                                    'LTD', 'Papaki Ltd',
                    'NIXI Holding Account', 'MarkMonitor International Limited', 'Zhuimi Inc', 'Stanco d.o.o.',
                    'TLD Registrar Solutions Ltd.', 'Ascio Technologies Inc. Danmark - filial af Ascio Technologies '
                                                    'Inc. USA', 'Corporation Service Company (Aust) Pty Ltd',
                    'INAMES CO., LTD.', 'Libyan Spider Network (int)', 'CSC Corporate Domains (Canada) Company',
                    'RU-CENTER-RU', 'EuroDNS S.A.', 'SNAPNAMES 46, LLC', 'Spot Domain LLC dba Domainsite.com',
                    'PDR Ltd. d/b/a PublicDomainRegistry.com', 'Dynadot, LLC', 'Web Address Registration Pty Ltd',
                    'CSL Computer Service Langenbach GmbH d/b/a joker.com', 'WEBCC', 'Unified Servers, Inc',
                    'LINUXWARES(http://www.mailplug.co.kr)', '易介集团北京有限公司', 'Deutsche Telekom AG', 'DropCatch.com 903 '
                                                                                                    'LLC',
                    'DOMAINADMINISTRATION.COM, LLC', 'PT. Web Commerce Communications', 'Rupert Hunt [Tag = '
                                                                                        'PAGEDEVELOPERS]',
                    'SAFEBRANDS', 'APA-IT Informations Technologie GmbH ( https://nic.at/registrar/658 )',
                    'NameVolcano.com LLC', 'Media Elite Holdings Limited', 'Compuglobalhypermega.com LLC',
                    'Alibaba Cloud Computing (Beijing) Co., Ltd.', 'mCloud doo', 'Synergy Wholesale Pty Ltd',
                    'DomainQuadrat Marketing GmbH ( https://nic.at/registrar/581 )', 'Communi Gal Communications Ltd.',
                    'DropCatch.com 559 LLC', 'Gransy s.r.o.', 'Deluxe Small Business Sales, Inc. d/b/a Aplus.net',
                    'Hosting Ukraine LLC.', 'Blacknight.ie', 'TurnCommerce, Inc. DBA NameBright.com',
                    'ПрАТ "ДАТАГРУП"', 'NetArt Registrar Sp. z o.o.', 'Go Montenegro Domains, LLC')
        try:
            whois_info = whois.whois(domain_name)
            to_find = whois_info.registrar
            # if to_find in registrars:
            #     return True
            for x in registrars:
                if str(to_find) == x:
                    return True

            # print("Phishing URL Feature: registrar not found")
            return False
        except Exception:
            print("<<<------------------------Exception is registrar well known-------------------------->>>")
            print(Exception)
            return False


    def __tell_is_https_used(self, url_to_check):
        if url_to_check.find("https", 0, 5) != -1:
            return True
        else:
            return False


    def __tell_is_domain_registered_time_enough(self, url_to_check):
        try:
            is_registered = __tell_is_domain_registered(url_to_check)
            if is_registered is True:
                whois_info = whois.whois(url_to_check)
                # print(whois_info)
                # get registration date of domain and store values
                domain_registration_date = whois_info.creation_date[0]

                # get expiration date of domain and store values
                domain_expiration_date = whois_info.expiration_date[0]

                # get domain update date
                domain_update_date = whois_info.updated_date[0]

                # get current date for comparison
                curr_date = datetime.datetime.now()
                curr_year = curr_date.year
                curr_month = curr_date.month
                curr_day = curr_date.day

                my_registration_date = datetime.date(domain_registration_date.year, domain_registration_date.month,
                                                    domain_registration_date.day)
                my_expiration_date = datetime.date(domain_expiration_date.year, domain_expiration_date.month,
                                                domain_expiration_date.day)
                my_update_date = datetime.date(
                    domain_update_date.year, domain_update_date.month, domain_update_date.day)

                my_current_date = datetime.date(curr_year, curr_month, curr_day)

                # comparing values for output
                if (my_current_date - my_registration_date).days > 365:
                    if (my_expiration_date - my_current_date).days > 1:
                        print(
                            "Legitimate Domain Feature: registration date old, not expired yet")
                        return 1
                    else:
                        print("Phishing Domain Feature: registration date old, but expired")
                        return -1
                else:
                    print(
                        "Phishing Domain Feature: registration date is new, not expired yet")
                    return -1
            else:
                print("Phishing Domain Feature: Domain not registered. Date not checked")
                return -1
        except Exception:
            print("<<<------------------------Exception Feature: registration time enough-------------------------->>>")
            return 0


    def __is_https_and_ssl_good(self, url_to_check):  # not complete
        # currently 1.1.8 feature is not complete
        # age of certificate is remaining to find
        is_https_used = self.__tell_is_https_used(url_to_check)
        is_domain_registered = self.__tell_is_domain_registered(url_to_check)
        try:
            headers_temp = {"Accept-Language": "en,en-gb;q=0.5"}
            my_r = requests.get(url_to_check, headers=headers_temp,
                                allow_redirects=True, verify=True, timeout=10)
        except requests.exceptions.SSLError as ssl_error:
            print("<<<------------------------Exception Feature: is https and ssl good-------------------------->>>")
            # print(ssl_error)
            SSL_good = False
            return -1
        else:
            # print("ssl no issue")
            SSL_good = True
            # my_r.close()
            if is_domain_registered is True:
                is_registrar_valid = self.__tell_is_registrar_well_known(url_to_check)
            else:
                is_registrar_valid = False
            print(is_https_used, SSL_good, is_domain_registered, is_registrar_valid)
            if is_https_used is True and SSL_good is True and is_domain_registered is True and is_registrar_valid is True:
                print(
                    "Legitimate Domain Feature: https used, SSL good, domain registered, registrar known")
                return 1
            elif SSL_good is False and is_domain_registered is False and is_registrar_valid is False:
                print(
                    "Phishing Domain Feature: SSL error and domain registration issue and registrar unknown")
                return -1
            elif is_https_used is False or SSL_good is False or is_domain_registered is False or is_registrar_valid is False:
                print("Suspicious Domain Feature: any one of them is not valid")
                return 0


    def __is_ip_address_valid(self, url_to_check):  # to check whether url is
        try:
            # print(IP(url_to_check).version())
            # first check if it is an ip address simple
            IP(url_to_check)
            its_ip_address = True
        except ValueError:
            # print("<<<------------------------Exception is ip address valid-------------------------->>>")
            its_ip_address = False

        # now check if the ip is in hex code
        check_hex_code = self.__is_ip_address_hex_coded(url_to_check)
        if check_hex_code >= 1:
            its_hex_coded = True
        else:
            its_hex_coded = False
        if its_ip_address is True or its_hex_coded is True:
            print("Phishing URL feature: 'IP address used'")
            return -1
        else:
            print("Legitimate URL feature: 'IP address not used'")
            return 1


    def __tell_if_favicon_belongs_to_domain(self, url_to_check):
        domain_received = self.__give_domain_part_of_website(url_to_check)
        try:
            icon_urls = favicon.get(url_to_check, timeout=10)
            for icon_url_obj in icon_urls:
                icon_url = icon_url_obj.url
                if str(icon_url).find("favicon.ico") != -1:
                    # curr_res = get_tld(icon_url, as_object=True)
                    # curr_domain = curr_res.domain
                    curr_domain = self.__give_domain_part_of_website(icon_url)
                    # print(icon_url)
                    if curr_domain != domain_received:
                        print("Phisihing favicon feature: Domains not matched")
                        return -1
                    else:
                        print("Legitimate favicon feature: Domains matched")
                        return 1
            print("Phishing favicon feature: Favicon not present")
            return -1
        except Exception as fav_ex:
            print("<<<------------------------Exception favicon-------------------------->>>")
            # print(fav_ex)
            print("Exception feature: Favicon error: Suspicious")
            return 0


    def __tell_if_https_in_domain(self, url_to_check):
        domain_received = self.__give_domain_part_of_website(url_to_check)
        if domain_received.find("https") == -1:
            print("Legitimate URL feature: https not in domain part of URL")
            return 1
        else:
            print("Phishing URL feature: https in domain part of URL")
            return -1


    # not complete yet
    def __tell_request_urls_percentage(self, soup_obj, main_url_of_website):
        received_url_list = self.__get_all_urls_of_website(soup_obj, main_url_of_website)
        if len(received_url_list) != 0:
            urls_from_domain = 0.0
            urls_from_outsource = 0.0
            domain_of_main_url = self.__give_domain_part_of_website(main_url_of_website)
            total_urls = len(received_url_list)

            for received_url in received_url_list:
                # print(received_url)
                temp_url_domain = self.__give_domain_part_of_website(received_url)
                # print(temp_url_domain, domain_of_main_url)
                if temp_url_domain == domain_of_main_url:
                    urls_from_domain += 1
                else:
                    urls_from_outsource += 1
            # percentage_inner_urls = (urls_from_domain/total_urls) * 100
            percentage_outer_urls = (urls_from_outsource/total_urls) * 100

            if percentage_outer_urls < 22:
                print("Legitimate Request URL feature: Request from outer sources is ",
                    percentage_outer_urls, "%")
                return 1
            elif 22 <= percentage_outer_urls < 61:
                print("Suspicious Request URL feature: Request from outer sources is a lot",
                    percentage_outer_urls, "%")
                return 0
            else:
                print("Phishing Request URL feature: Almost all requests from outer sources",
                    percentage_outer_urls, "%")
                return -1
        else:
            print("Legitimate Request URL feature: No url exists")
            return 1


    def __get_all_urls_of_website(self, my_soup, url_to_check):
        urls_list = []
        a_tag = my_soup.findAll("a")
        # print("printing all the tags")
        # print(a_tag)

        for a_tag in a_tag:
            href = a_tag.attrs.get("href")
            # print(href)
            if href == "" or href is None:
                # href empty tag
                continue
            elif (href != "" or href is not None) and str(href).find("http") == -1:
                made_url = str(url_to_check) + str(href)
                href = made_url
                urls_list.append(href)
            else:
                urls_list.append(href)
        return urls_list


    def __get_text_of_sfh_urls(self, soup_obj, url_to_check):
        # getting list of a tags
        urls_list_to_check = []
        all_urls_list = []
        all_urls_text_list = []
        my_tags = soup_obj.findAll("a")
        for my_tag in my_tags:
            href = my_tag.attrs.get("href")
            if (href != "" or href is not None) and str(href).find("http") == -1:
                made_url = str(url_to_check) + str(href)
                href = made_url
                all_urls_list.append(href)
            else:
                all_urls_list.append(href)
        # print(all_urls_list)

        i = 0
        a_tags = soup_obj.findAll("a")
        ragex_for_privacy = "[Pp][Rr][Ii][Vv][Aa][Cc][Yy]"
        ragex_for_policies = "[Pp][Oo][Ll][Ii][Cc][Ii][Ee][Ss]|[Pp][Oo][Ll][Ii][Cc][Yy]"
        ragex_for_terms = "[Tt][Ee][Rr][Mm][Ss]|[Cc][Oo][Nn][Dd][Ii][Tt][Ii][Oo][Nn]"
        ragex_for_about = "[Aa][Bb][Oo][Uu][Tt]"
        ragex_for_contacts = "[Cc][Oo][Nn][Tt][Aa][Cc][Tt]"
        ragex_for_connect_us = "[Cc][Oo][Nn][Nn][Ee][Cc][Tt]"
        ragex_for_support_us = "[Ss][Uu][Pp][Pp][Oo][Rr][Tt]"
        ragex_for_user_agreement = "[Aa][Gg][Rr][Ee][Ee][Mm][Ee][Nn][Tt]"
        ragex_for_legal = "[Ll][Ee][Gg][Aa][Ll]"
        # print("printing all the tags")
        # print(a_tags)
        for a_url in a_tags:
            # print(a_url.string)
            curr_text = str(a_url.string)
            if re.search(ragex_for_privacy, curr_text):
                urls_list_to_check.append(all_urls_list[i])
                # print("Privacy link found", all_urls_list[i])
            if re.search(ragex_for_terms, curr_text):
                # print("Terms link found", all_urls_list[i])
                urls_list_to_check.append(all_urls_list[i])
            if re.search(ragex_for_about, curr_text):
                # print("About link found", all_urls_list[i])
                urls_list_to_check.append(all_urls_list[i])
            if re.search(ragex_for_policies, curr_text):
                # print("Policies link found", all_urls_list[i])
                urls_list_to_check.append(all_urls_list[i])
            if re.search(ragex_for_contacts, curr_text):
                # print("Contact link found", all_urls_list[i])
                urls_list_to_check.append(all_urls_list[i])
            if re.search(ragex_for_connect_us, curr_text):
                # print("Connect Us link found", all_urls_list[i])
                urls_list_to_check.append(all_urls_list[i])
            if re.search(ragex_for_support_us, curr_text):
                # print("Support Us link found", all_urls_list[i])
                urls_list_to_check.append(all_urls_list[i])
            if re.search(ragex_for_user_agreement, curr_text):
                # print("User Agreement link found", all_urls_list[i])
                urls_list_to_check.append(all_urls_list[i])
            if re.search(ragex_for_legal, curr_text):
                # print("Legal link found", all_urls_list[i])
                urls_list_to_check.append(all_urls_list[i])
            i += 1
        # print(urls_list_to_check)

        domain_of_given_url = self.__give_domain_part_of_website(url_to_check)
        for curr_url in urls_list_to_check:
            curr_domain = self.__give_domain_part_of_website(curr_url)
            if curr_domain == "":
                print("Phishing SFH feature: empty domain error")
                return -1
            elif curr_domain.find("blank") != -1:
                print("Phishing SFH feature: BLANK in domain")
                return -1
            elif curr_domain != domain_of_given_url:
                print("Suspicious SFH feature: Domains not matched")
                return 0
        print("Legitimate SFH feature: Nothing phishy")
        return 1


    def __url_of_anchor(self, soup_obj, url_to_check):
        bad_url = 0.0
        ragex_for_only_hash = "[#]{1}[A-Za-z0-9-_]+"
        ragex_for_javascript = "[Jj]{1}[Aa]{1}[Vv]{1}[Aa]{1}[Ss]{1}[Cc]{1}[Rr]{1}[Ii]{1}[Pp]{1}[Tt]{1}[:]{2}"
        all_urls = self.__get_all_urls_of_website(soup_obj, url_to_check)
        total_urls = len(all_urls)
        if len(all_urls) != 0:
            for curr_url in all_urls:
                if curr_url == "":
                    bad_url += 1
                elif re.search(ragex_for_only_hash, curr_url) is not None:
                    bad_url += 1
                elif re.search(ragex_for_javascript, curr_url) is not None:
                    bad_url += 1
            percentage = (bad_url/total_urls) * 100
            # print("percentage is ", percentage)
            if percentage < 31:
                print("Legitimate URL feature: URL of Anchor")
                return 1
            elif 31 <= percentage <= 67:
                print("Suspicious URL feature: URL of Anchor")
                return 0
            else:
                print("Phishing URL feature: URL of Anchor")
                return -1
        else:
            print("Legitimate URL feature: URL of Anchor")
            return 1


    def __tell_mail_to(self, my_soup):
        a_tags = my_soup.findAll("a")
        # print(a_tags)
        for my_tag in a_tags:
            href = my_tag.attrs.get("href")
            temp_str = str(href)
            if temp_str.find("mailto") != -1:
                print("Phishing Feature: sending info using mail to:")
                return -1
        print("Legitimate Feature: No use of mailto:")
        return 1


    def __is_right_click_disabled(self, my_soup):
        # just find context menu in the code
        ragex_for_context_menu = "contextmenu"
        all_web_data = str(my_soup)
        x = re.search(ragex_for_context_menu, all_web_data)
        if x is None:
            print("Legitimate Feature: Right Click not tempered")
            return 1
        else:
            print("Phishing Feature: Right click tempered")
            return -1


    def __tell_response_redirection_times(self, my_r):
        count = 0
        for item in my_r.history:
            code = item.status_code
            # print(code)
            if code == 301 or code == 302:
                count += 1
        if count <= 1:
            print("Legitimate Feature: Redirects max 1")
            return 1
        elif 2 <= count <= 4:
            print("Suspicious Feature: Redirects from 2 to 4")
            return 0
        else:
            print("Phishing Feature: Redirects more than 4")
            return -1


    # by Ali
    def __age_of_domain(self, url_to_check):
        """ this will tell you the difference btw the creation date and current time it its > 6 month
        then phishing
        """
        # print('\nCalling age_of_domain(url_to_check):///////////////////////')
        today = date.today()
        # print("Today's date:", today)
        try:
            w = whois.whois(url_to_check)
            # print("Creation date is ")
            # iso 8061 format
            # print(w.creation_date)
            try:
                length = len(w.creation_date)
            except:
                length = 1

            if length == 1:
                string = str(w.creation_date)

            else:
                string = str(w.creation_date[0])
            # x = datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
            x = datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
            # diff = datetime.now() - x
            diff = datetime.datetime.now() - x
            # print("Difference btw creation date and today is " + str(diff))
            extract_days = diff.days
            # print(extract_days)
            if extract_days < 190:
                print("Phishing Feature: age of domain")
                return -1  # phishing
            else:
                print("Legitimate Feature: age of domain")
                return 1  # Not phishing

        except:
            print("Nothing is found in whois therefore difference btw creation date and today is 0 it must be phishing")
            return -1  # Malicious


    # by ali
    def __whois_dns_server_value(self, url_to_check):
        """ this will tell you the whether the whois_server value is
        empty or not if empty then phishing
        """
        # print("\nCalling whois_dns_server_value(url):///////////////////////")
        # print("Checking Whois server value:")
        try:
            w = whois.whois(url_to_check)

            # iso 8061 format
            # print(w.whois_server)
            if w.whois_server:
                # print('Record found') i.e not phishing
                print("Legitimate Feature: whois server info")
                return 1
            else:
                print("Phishing Feature: whois server info")
                # print("No Record Found")  i.e  phishing
                return -1
        except:
            print("<<<------------------------Exception whois server info-------------------------->>>")
            print("Exception Feature: whois server info")
            # print("Error occurred") i.e malicious
            return -1


    def __check_iframes2(self, url_to_check_for_feature):
        num_apperances_of_tag = [0] * 1
        try:
            elements = ['iframe']
            page = requests.get(url_to_check_for_feature)
            soup = BeautifulSoup(page.content, 'html.parser')
            count = 0
            for x in elements:
                num_apperances_of_tag[count] = len(soup.find_all(elements[count]))
                count = + 1

            for x in num_apperances_of_tag:
                if x > 0:
                    print("Phishing Feature: iframe element exist")
                    return -1  # phishing
            print("Legitimate Feature: iframe element not exist")
            return 1  # Not phishing

        except():
            return 0
            # print("Error iframe element ")

    # by ali
    def __check_double_document_elements(self, url_to_check):
        num_appearance_of_tag = [0] * 4
        try:
            elements = ['html', 'head', 'title', 'body']
            # elements = ['html', 'head', 'p', 'body', 'script', 'button']
            headers_temp = {"Accept-Language": "en,en-gb;q=0.5"}
            page = requests.get(url_to_check, headers=headers_temp,
                                allow_redirects=True, timeout=10)
            soup = BeautifulSoup(page.content, 'html.parser')
            # soup = BeautifulSoup(open('assignment-2.html'), "html.parser")
            i = 0
            for x in elements:
                num_appearance_of_tag[i] = len(soup.find_all(elements[i]))
                i = i + 1
            # print(num_appearance_of_tag)
            for x in num_appearance_of_tag:
                if x > 1:
                    print("Phishing Feature: double document elements")
                    return -1  # phishing
            print("Legitimate Feature: double document elements")
            return 1  # Not phishing
        except:
            print(
                "<<<------------------------Exception double doc-------------------------->>>")
            # print(num_appearance_of_tag)
            return 0  # cant say


    # by ali
    def __check_is_document_has_form(self, soup_obj):
        num_appearance_of_tag = [0] * 2
        try:
            elements = ['input', 'form']
            # elements = ['html', 'head', 'p', 'body', 'script', 'button']
            # page = requests.get(url)
            # soup = BeautifulSoup(page.content, 'html.parser')
            # soup = BeautifulSoup(open('assignment-2.html'), "html.parser")
            i = 0
            for x in elements:
                num_appearance_of_tag[i] = len(soup_obj.find_all(elements[i]))
                i = i + 1
            # print(num_appearance_of_tag)
            for x in num_appearance_of_tag:
                if x > 0:
                    return 0  # Malacious

            return 1  # not malicious

        except:
            print("<<<<---------------------Exception: Chesck if forms---------------------------->>>>")
            return 0  # cant say


    def isUrlPhishing(self, url_to_check):
        return_abuseIP = self.__isGenuineABUSEIP(url_to_check)
        return_phishtank = self.__isGenuinePhishTank(url_to_check)

        if return_abuseIP == -1 or return_phishtank == -1:
            return "Phishing URL"
        elif return_abuseIP == 0:
            return "Suspicious URL"
        else:
            # request to get content related to URL
            try:
                headers = {"Accept-Language": "en,en-gb;q=0.5"}
                r = requests.get(url_to_check, headers=headers,
                                    allow_redirects=True, timeout=10)
                soup = BeautifulSoup(r.content, 'html.parser')

                feature_values = np.arange(21).reshape(1, 21)

                # "FEATURE 1"
                feature_values[0][0] = self.__is_ip_address_valid(r.url)

                # "FEATURE 2"
                feature_values[0][1] = self.__is_url_length_friendly(r.url)

                # "FEATURE 3"
                feature_values[0][2] = self.__is_url_shortening_service_used(url_to_check, r.url)

                # "FEATURE 4"
                feature_values[0][3] = self.__is_url_having_at_the_rate_symbol(r.url)

                # "FEATURE 5"
                feature_values[0][4] = self.__is_position_double_slash_good(r.url)

                # "FEATURE 6"
                feature_values[0][5] = self.__tell_if_dash_symbol_present(r.url)

                # "FEATURE 8"
                feature_values[0][6] = self.__tell_sub_domain_and_multilevel_domain(r.url)

                # "FEATURE 8"
                feature_values[0][7] = self.__is_https_and_ssl_good(r.url)

                # "FEATURE 10"
                feature_values[0][8] = self.__tell_if_favicon_belongs_to_domain(r.url)

                # "FEATURE 12"
                feature_values[0][9] = self.__tell_if_https_in_domain(r.url)

                # "FEATURE 1.2.1. Request URL"
                feature_values[0][10] = self.__tell_request_urls_percentage(soup, r.url)

                # Feature 1.2.2 URL of anchor
                feature_values[0][11] = self.__url_of_anchor(soup, r.url)

                # Feature 1.2.4 SFH
                feature_values[0][12] = self.__get_text_of_sfh_urls(soup, r.url)

                # feature 1.2.5 mail_to()
                feature_values[0][13] = self.__tell_mail_to(soup)

                # feature 1.3.1 website forwading
                feature_values[0][14] = self.__tell_response_redirection_times(r)

                # feature 1.3.3
                feature_values[0][15] = self.__is_right_click_disabled(soup)

                # feature by ali 1.4.1
                feature_values[0][16] = self.__age_of_domain(r.url)

                # feature by ali 1.4.2
                feature_values[0][17] = self.__whois_dns_server_value(r.url)

                # feature by ali 1.3.5
                feature_values[0][18] = self.__check_iframes2(r.url)

                # feature random by ali
                feature_values[0][19] = self.__check_double_document_elements(r.url)

                # by ali
                feature_values[0][20] = self.__check_is_document_has_form(soup)
                
                # print(feature_values)
                # load the model from disk
                try:
                    this_dir, this_filename = os.path.split(__file__)  # Get path of data.pkl
                    data_path = os.path.join(this_dir, 'trained_model', 'finalized_model.sav')
                    data = pickle.load(open(data_path, 'rb'))
                    # loaded_model = pickle.load(open("trained_model/finalized_model.sav", 'rb'))
                    # result_prob = loaded_model.predict_proba(feature_values)
                    result_prob = data.predict_proba(feature_values)
                    percentage_phishing = result_prob[0][0]
                    if percentage_phishing <= 0.35:
                        return "URL categorized as 'Benign URL'"
                    elif 0.36 < percentage_phishing <= 0.70:
                        return "URL is categorized as 'Suspicious Url'"
                    else:
                        return "URL is categorized as 'Phishing Url'"
                except Exception as e:
                    # print(e)
                    return "Error: Could not check using model"
            except Exception as e:
                # print(e)
                return "Error: Could not connect to Website"