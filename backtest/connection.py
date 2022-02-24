from ibapi.client import EClient

from ibapi.wrapper import EWrapper


'''
For testing establishing a connection with TWS API.

1. Make sure you're logged into TWS (This might not be necessary when we switch to the light weight version)
2. Make sure to check "Enable ActiveX and Socket Clients"
3. If you don't have ibapi library, run: pip3 install ibapi

You should get output like "ERROR -1 2158 Sec-def data farm connection is OK:secdefil"
'''

# Find this port in file -> global config. -> API -> settings
PORT = 7497
LOCAL_HOST = '127.0.0.1'
TOTAL_CLIENTS_ALLOWED = 32

class TradingSystem(EWrapper, EClient):

    def __init__(self, client_id):
        self.client_id = client_id

        # Establishing a connection TWS
        EClient.__init__(self, self)

    def connect_to_tws(self):
        app.connect(LOCAL_HOST, PORT, clientId=self.client_id)  # TWS supports up to 32 clients
        app.run()

if __name__ == '__main__':
    app = TradingSystem(1)
    app.connect_to_tws()
