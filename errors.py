
class APIError(Exception):
    def __init__(self,code):
        if code == 400:
            msg = "Algo ha fallado en la consulta, vuelva a intentarlo más tarde."
        elif code == 401:
            msg = "Sin autorización -- Revise si su API KEY es correcta."
        elif code == 403:
            msg = "No tienes suficientes privilegios para realizar la consulta."
        elif code == 429:
            msg = "Has excedido el número de consultas para tu API KEY. Pónganse en contacto en www.coinapi.io."
        elif code == 550:
            msg = "No hay información para la consulta realizada. Inténtelo más tarde."                                                
        super().__init__(msg)
          