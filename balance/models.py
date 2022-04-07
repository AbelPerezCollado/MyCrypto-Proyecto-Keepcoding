import sqlite3
import requests
from config import API_KEY, HEADERS, RUTA_BBDD, URL_CONSULTA
from errors import APIError
from datetime import datetime

now = datetime.now()

def convertir_en_dict(self,param):
    clave= []
    valor = []
    for lista in param:
        clave.append(lista[0])
        valor.append(lista[1])
        return dict(zip(clave,valor))

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
        con.commit()
        
        return cur.fetchall()

    def insert_compra(self,params):
        con = sqlite3.connect(RUTA_BBDD)
        cur = con.cursor()
        sql_query = "INSERT INTO movimientos (date,time,moneda_from,cantidad_from,moneda_to,cantidad_to) VALUES(?,?,?,?,?,?)"
        con.execute(sql_query,params)
        con.commit()
        

    def fecha_actual(self):
        return str(now.date())

    def hora_actual(self):
        return str(now.time())

    def total_euros_invertidos(self):
        con = sqlite3.connect(RUTA_BBDD)
        cur = con.cursor()
        cur.execute("""
                    SELECT SUM(cantidad_from)
                    FROM movimientos
                    WHERE moneda_from ='EUR'
        
        """)
        con.commit()
                                               
        return cur.fetchone()

    def saldo_euros_invertidos(self):
        con = sqlite3.connect(RUTA_BBDD)
        cur = con.cursor()
        cur.execute("""
                    SELECT ifnull(SUM(cantidad_from),0)
                    FROM movimientos
                    WHERE moneda_from ='EUR' 

                    UNION
                    SELECT ifnull(SUM(cantidad_to),0)
                    FROM movimientos
                    WHERE moneda_to ='EUR' 
        
        """)
        con.commit()        
        return cur.fetchall()


    def criptos_to(self):
        con = sqlite3.connect(RUTA_BBDD)
        cur = con.cursor()
        cur.execute("""
                    SELECT moneda_to,sum(cantidad_to)
                    FROM movimientos
                    WHERE movimientos.moneda_to !='EUR'
                    GROUP BY moneda_to
                    HAVING count() >=1 
                    """)
        con.commit() 
        return cur.fetchall()


    def criptos_from(self):
        con = sqlite3.connect(RUTA_BBDD)
        cur = con.cursor()
        cur.execute("""
                    SELECT moneda_from,sum(cantidad_from)
                    FROM movimientos
                    WHERE movimientos.moneda_from !='EUR'
                    GROUP BY moneda_from
                    HAVING count() >=1 
                    """)
        con.commit()
        return cur.fetchall()