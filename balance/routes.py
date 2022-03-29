from flask import redirect, render_template, flash,request
from balance import app
from balance.models import ValorCriptoMonedas

@app.route("/")
def inicio():
    
    return render_template("movimientos.html",clase_inicio = "disabled-link",movimientos = '')
    


@app.route("/compra")
def purchase():
    return render_template("base.html",clase_compra = "disabled-link" )


@app.route("/estado")
def status():
    return render_template("base.html",clase_estado = "disabled-link")