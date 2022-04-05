import sqlite3
from flask import redirect, render_template, flash,request, url_for
from balance import app
from balance.models import ConsultasSql, ValorCriptoMonedas
from formularios import ComprasForm, EstadoForm

db = ConsultasSql()

@app.route("/")
def inicio():
    db = ConsultasSql()
    try:
        datos = db.select_movimientos()
        
        if len(datos):
            return render_template("movimientos.html",clase_inicio = "disabled-link",movimientos = datos)
        else:
            return render_template("movimientos.html",clase_inicio = "disabled-link",movimientos = '')            
    except sqlite3.Error as e:
        
        flash("Error de la BBDD, inténtelo más tarde")
        return render_template("movimientos.html",clase_inicio = "disabled-link",movimientos = '')


@app.route("/compra",methods= ["GET","POST"])
def compra():
    form = ComprasForm(request.form)
    
    if request.method == "GET":

        return render_template("compra.html",clase_compra = "disabled-link",formulario = form )

    elif request.method == "POST":
        if form.validate():
            if form.calcular.data:
                
                llamada_api = ValorCriptoMonedas(form.moneda_from.data,form.moneda_to.data)
                cantidad_convertida = llamada_api.obtener_cantidad_to(form.cantidad_from.data)
                pu = float(form.cantidad_from.data) / cantidad_convertida
                form.cantidad_convertida.data = cantidad_convertida
                form.cantidad_convertida._value = cantidad_convertida
                form.pu.data = pu
                form.pu._value = pu
                return render_template("compra.html",clase_compra = "disabled-link",formulario = form,
                                        cantidad_convertida = round(cantidad_convertida,2), pu = round(pu,2)  )
            elif form.comprar.data:
                
                llamada_api = ValorCriptoMonedas(form.moneda_from.data,form.moneda_to.data)
                form.cantidad_convertida.data = llamada_api.obtener_cantidad_to(form.cantidad_from.data)
                pu = float(form.cantidad_from.data) / form.cantidad_convertida.data 
                lista_datos = (db.fecha_actual(),db.hora_actual(),form.moneda_from.data,form.cantidad_from.data,
                               form.moneda_to.data,form.cantidad_convertida.data)                               
                try:
                    db.insert_compra(lista_datos)
                    return redirect("/")
                except sqlite3.Error as e:
                    flash("Error al modificar la BBDD, inténtelo más tarde")
                    return render_template("compra.html",clase_compra = "disabled-link",formulario = form,
                                        cantidad_convertida = round(form.cantidad_convertida.data,2), pu = round(pu,2))                        
                                
        else:
            
            return render_template("compra.html",clase_compra = "disabled-link",formulario = form)            



@app.route("/estado")
def status():
    form = EstadoForm()
    return render_template("estado.html",clase_estado = "disabled-link",formulario = form)



    
    




                   

          
          