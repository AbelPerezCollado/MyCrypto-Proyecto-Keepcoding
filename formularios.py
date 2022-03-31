from datetime import datetime
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms   import DateTimeField,StringField,SelectField,FloatField,SubmitField,DateField,TimeField
from wtforms.validators import DataRequired,Length,NumberRange
from datetime import datetime

from config import MONEDAS
now = datetime.now()

class ComprasForm(FlaskForm):
    moneda_from = SelectField('De', choices= MONEDAS)
    moneda_to = SelectField('A', choices= MONEDAS)

    cantidad_from = FloatField("Cantidad",validators=[DataRequired(),
                    NumberRange(message="Debe ser una cantidad positiva",min=0.01)])

    cantidad_to = FloatField("Cambio",validators=[DataRequired(),
                NumberRange(message="Debe ser una cantidad positiva",min=0.01)],render_kw={'readonly':True})

    pu =FloatField("Total",validators=[DataRequired(),
        NumberRange(message="Debe ser una cantidad positiva",min=0.01)],render_kw={'readonly':True})             

    fecha = now.date()
    hora = now.time()


    comprar = SubmitField("Comprar")



class EstadoForm(FlaskForm):
    invertido = FloatField("Invertido",render_kw={'readonly':True})
    valor_actual = FloatField("Valor actual",render_kw={'readonly':True})

    