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
        if self.respuesta.status_code == 400:
            raise APIError("Algo ha fallado en la consulta, vuelva a intentarlo más tarde.")
        
        elif self.respuesta.status_code == 401:
           raise APIError("Sin autorización -- Revise si su API KEY es correcta.")

        elif self.respuesta.status_code == 403:
            raise APIError("No tienes suficientes privilegios para realizar la consulta.")

        elif self.respuesta.status_code == 429:
            raise APIError("Has excedido el número de consultas para tu API KEY. Pónganse en contacto en www.coinapi.io.")

        elif self.respuesta.status_code == 550:
            raise APIError("No hay información para la consulta realizada. Inténtelo más tarde.")                                   
            
        elif self.respuesta.status_code != 200:
            raise APIError(self.respuesta.json()["error"])
        self.tasa = self.respuesta.json()["rate"]
        return self.tasa

    def obtener_cantidad_to(self,cantidad_from):
        return self.obtener_tasa() * cantidad_from        
        
        


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

    def insert_compra(self):
        con = sqlite3.connect(RUTA_BBDD)
        cur = con.cursor()
        
        con.commit()
        con.close()        