import sqlite3
from flask import redirect, render_template, flash,request
from balance import app
from balance.models import ConsultasSql, ValorCriptoMonedas

@app.route("/")
def inicio():
    db = ConsultasSql()
    try:
        datos = db.select_movimientos()
        print(datos)
        if len(datos):
            return render_template("movimientos.html",clase_inicio = "disabled-link",movimientos = datos)
        else:
            return render_template("movimientos.html",clase_inicio = "disabled-link",movimientos = '')            
    except sqlite3.Error as e:
        
        flash("Error de la BBDD, inténtelo más tarde")
        return render_template("movimientos.html",clase_inicio = "disabled-link",movimientos = '')


@app.route("/compra")
def purchase():
    return render_template("base.html",clase_compra = "disabled-link" )


@app.route("/estado")
def status():
    return render_template("base.html",clase_estado = "disabled-link")