import sqlite3
import requests
from config import HEADERS, RUTA_BBDD, URL_CONSULTA
from errors import APIError
from datetime import datetime




def convertir_en_dict(param):
    clave= []
    valor = []
    for lista in param:
        clave.append(lista[0])
        valor.append(lista[1])
    return dict(zip(clave,valor))

def obtienevalor_criptos_actual(dict1,dict2):
    criptos_actual = {}
    for key in dict1:
        if key in dict2:
            criptos_actual[key] = dict1[key] - dict2[key]
        else:
            criptos_actual[key] = dict1[key]
    return criptos_actual

def obtiene_euros_decriptos(dict):
    total = 0
    for key in dict:
        vc = ValorCriptoMonedas(origen = key ,destino = 'EUR')
        total += vc.obtener_cantidad_to(dict[key])

    return total

def puedo_comprar_esta_moneda(moneda,cantidad,dic):
    if moneda != 'EUR':
        if moneda in dic and cantidad <= dic[moneda]:
            return True
        else:
            return False            
    else:
        return True

def estadoinversion(invertido,actual):
    if actual > invertido:
        return 'color:green'    
    else:
        return 'color:red'
                


class ValorCriptoMonedas():
    def __init__(self,origen="",destino="") -> None:
        self.origen = origen
        self.destino = destino
        self.tasa = 0.0
    def obtener_tasa(self):
        self.respuesta = requests.get(URL_CONSULTA.format(self.origen,self.destino), headers=HEADERS)
        if self.respuesta.status_code != 200:
            raise APIError(self.respuesta.status_code)
                                 
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
        sql_query = "INSERT INTO movimientos (date,time,moneda_from,cantidad_from,moneda_to,cantidad_to) VALUES(?,?,?,?,?,?)"
        con.execute(sql_query,params)
        con.commit()
        

    def fecha_actual(self):
        now = datetime.now()
        return str(now.date())

    def hora_actual(self):
        now = datetime.now()
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
        lista = cur.fetchone()
        if lista:
            return lista[0]
        else:
            return 0                
                                               
        

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
        lista = cur.fetchall()
        if lista and len(lista) == 2:
            return lista[0][0] - lista[1][0]        
        else:
            return 0


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


            