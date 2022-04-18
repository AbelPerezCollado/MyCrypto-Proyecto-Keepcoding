import sqlite3
from tkinter import DISABLED
from flask import redirect, render_template, flash,request, url_for
from balance import app
from balance.models import ConsultasSql, ValorCriptoMonedas, convertir_en_dict, obtiene_euros_decriptos, obtienevalor_criptos_actual, puedo_comprar_esta_moneda
from errors import APIError
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
    form = ComprasForm()

     
    if request.method == "GET":
        
        return render_template("compra.html",clase_compra = "disabled-link",formulario = form )

    elif request.method == "POST":
        
        if form.validate():
            if form.calcular.data:
                
                llamada_api = ValorCriptoMonedas(form.moneda_from.data,form.moneda_to.data)
                try:
                    
                    todas_las_monedas_compradas =convertir_en_dict(db.criptos_to())
                    if not puedo_comprar_esta_moneda(form.moneda_from.data,form.cantidad_from.data,todas_las_monedas_compradas):
                        flash(f"No tienes suficientes {form.moneda_from.data}.")
                        return render_template("compra.html",clase_compra = "disabled-link",formulario = form) 

                    cantidad_convertida = llamada_api.obtener_cantidad_to(form.cantidad_from.data)
                    form.cantidad_convertida.data = cantidad_convertida
                    form.cantidad_convertida_h.data = cantidad_convertida
                    pu = float(form.cantidad_from.data) / cantidad_convertida
                    form.pu.data = pu
                    form.pu_h.data = pu
                    
                    
                    
                    return render_template("compra.html",clase_compra = "disabled-link",formulario = form)
                except APIError as err:
                    flash(err)
                    return render_template("compra.html",clase_compra = "disabled-link",formulario = form )

            elif form.comprar.data:
                
                
                form.cantidad_convertida.data = form.cantidad_convertida_h.data 
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
def estado():
    form = EstadoForm()
    
    total_euros_invertidos = db.total_euros_invertidos()
    form.invertido.data = total_euros_invertidos
    
    saldo_euros_invertidos = db.saldo_euros_invertidos()
        
    dict_criptos_to = convertir_en_dict(db.criptos_to())
    dict_criptos_from = convertir_en_dict(db.criptos_from())
    cantidad_actual_cripto = obtienevalor_criptos_actual(dict_criptos_to,dict_criptos_from)
    valor_euros_decriptos = obtiene_euros_decriptos(cantidad_actual_cripto)


    form.valor_actual.data = total_euros_invertidos + saldo_euros_invertidos + valor_euros_decriptos

    return render_template("estado.html",clase_estado = "disabled-link",formulario = form)

    



    
    




                   

          
          