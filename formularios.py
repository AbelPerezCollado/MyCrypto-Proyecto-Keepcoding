from curses.ascii import isdigit
from datetime import datetime
from email import message
from flask_wtf import FlaskForm
from wtforms   import DateTimeField,StringField,SelectField,FloatField,SubmitField,DateField,TimeField
from wtforms.validators import DataRequired,Length,NumberRange,InputRequired,ValidationError
from wtforms.widgets import Select
from datetime import datetime

from config import MONEDAS
now = datetime.now()

def validar_cantidad_from(form,cantidad_from):
    try:
        float(cantidad_from.data)
    except:
        raise ValidationError("La cantidad debe ser un número")        
           


def validar_moneda(form,field):
    if field.data == form.moneda_from.data:
        raise ValidationError("Debes elegir tipos de monedas distintos")
                   

class ComprasForm(FlaskForm):
    moneda_from = SelectField('De', choices= MONEDAS, validators=[DataRequired()])
    moneda_to = SelectField('A', choices= MONEDAS,validators=[DataRequired(),validar_moneda])
    
    cantidad_from = FloatField("Cantidad",validators=[DataRequired(),validar_cantidad_from,
                    NumberRange(min=0.00001,max = 99999999,message = "La cantidad debe ser un número positivo")])
                    
    cantidad_convertida =  FloatField()
    pu = FloatField()          

    fecha = now.date()
    hora = now.time()

    
    calcular = SubmitField("CALCULAR")
    comprar = SubmitField("Comprar")



class EstadoForm(FlaskForm):
    invertido = FloatField("Invertido",render_kw={'readonly':True})
    valor_actual = FloatField("Valor actual",render_kw={'readonly':True})

    