from flask import redirect, render_template, flash,request
from balance import app
from balance.models import ValorCriptoMonedas

@app.route("/")
def inicio():
    consulta = ValorCriptoMonedas("EUR","BTC")
    
    return consulta.obtener_tasa()


@app.route("/purchase")
def purchase():
    return "Muestro formulario en el que realizar compra,venta o intercambio de monedas"


@app.route("/status")
def status():
    return "Muestro estado de la inversión, euros gastados en comprar BTC y el valor actual del total de criptomonedas que existan en el stock del usuario según sus movimientos"