"""
Various sample usages of the Alliance for Open Chatbot client utilities

Authors:
    - Amédée Potier (amedee.potier@konverso.ai) from Konverso

History:
    - 2020/11/02: Amédée: Initial version.

"""

import time
import requests

if __name__ == '__main__':

    from openchatbotclient import client

    for host in (#'https://veolia-dev.konverso.ai',
                 #'https://veolia-preprod.konverso.ai',
                 #'https://poleemploi.konverso.ai',
                 'https://poleemploi-dev.konverso.ai',
                 #'https://poleemploiformation.konverso.ai'
                 ):

        start_time = time.time()
        bot_konverso = client(host, port=443, path='/api/ask')
        try:
            response = bot_konverso.ask("monitor_test_329482938492839428349", "hello 3", lang="en", timeout=3)
        except requests.exceptions.ReadTimeout:
            print ("%s: TIMEOUT" % host)
        except Exception as e:
            print ("%s: ERROR: %s" % (host, str(e)))
        else:
            end_time = time.time()
            print ("%s: RESPONSE in %f seconds" % (host, (end_time - start_time)))
            print("=> Actual response:", response)
