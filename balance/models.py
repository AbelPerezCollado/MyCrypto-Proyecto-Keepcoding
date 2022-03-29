import sqlite3
import requests
from config import API_KEY, HEADERS, RUTA_BBDD, URL_CONSULTA
from errors import APIError

class ValorCriptoMonedas():
    def __init__(self,origen="",destino="") -> None:
        self.origen = origen
        self.destino = destino
        self.tasa = 0.0
    def obtener_tasa(self):
        self.respuesta = requests.get(URL_CONSULTA.format(self.origen,self.destino), headers=HEADERS)
        if self.respuesta.status_code == 401:
           raise APIError("Unauthorized -- Your API key is wrong")
            
        elif self.respuesta.status_code != 200:
            raise APIError(self.respuesta.json()["error"])

        #self.tasa = round(self.respuesta.json()["rate"], 2)

        return self.respuesta.json()


class ConsultasSql():

    def select_movimientos(self):
        con = sqlite3.connect(RUTA_BBDD)
        cur = con.cursor()
        cur.execute("""
                    SELECT *
                    FROM movimientos
                    ORDER BY date
        
        """)
        return cur.fetchall()