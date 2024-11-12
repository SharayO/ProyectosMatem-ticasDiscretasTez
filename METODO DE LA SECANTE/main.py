from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

# Función para calcular la raíz usando el Método de la Secante y generar la tabla de iteraciones
def metodo_secante(funcion_str, x0, x1, tolerancia, max_iter=50):
    x = sp.symbols('x')
    f = sp.sympify(funcion_str)  # Convierte el string en una función simbólica

    iteraciones = []
    iteracion = 0

    while iteracion < max_iter:
        fx0 = f.subs(x, x0)
        fx1 = f.subs(x, x1)

        if fx1 - fx0 == 0:  # Evitar división por cero
            break

        # Fórmula del Método de la Secante
        x2 = x1 - (fx1 * (x1 - x0)) / (fx1 - fx0)

        # Calcular el error relativo
        error = abs((x2 - x1) / x2) if x2 != 0 else float('inf')

        # Guardar los valores en la lista de iteraciones
        iteraciones.append({'x0': x0, 'x1': x1, 'raiz': x2, 'error': error})

        if error < tolerancia:
            return x2, error, iteraciones

        x0 = x1
        x1 = x2
        iteracion += 1

    return None, None, iteraciones  # No se encontró la raíz dentro de la tolerancia

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            funcion = request.form['funcion']
            x0 = float(request.form['limite_inferior'])
            x1 = float(request.form['limite_superior'])
            tolerancia = float(request.form['tolerancia'])

            # Llamar al método de la secante
            raiz, error, iteraciones = metodo_secante(funcion, x0, x1, tolerancia)

            if raiz is not None:
                resultado = f"Raíz aproximada: {raiz:.6f}, con un error de: {error:.6f}."
            else:
                resultado = "No se pudo encontrar una raíz dentro del límite de iteraciones."

            return render_template('index.html', resultado=resultado, iteraciones=iteraciones, 
                                   funcion=funcion, limite_inferior=x0, 
                                   limite_superior=x1, tolerancia=tolerancia)

        except ValueError:
            resultado = "Error: entrada no válida. Asegúrate de que los valores sean correctos."
            return render_template('index.html', resultado=resultado, iteraciones=None, 
                                   funcion=request.form.get('funcion', ''), 
                                   limite_inferior=request.form.get('limite_inferior', ''), 
                                   limite_superior=request.form.get('limite_superior', ''), 
                                   tolerancia=request.form.get('tolerancia', ''))

    return render_template('index.html', resultado=None, iteraciones=None, 
                           funcion='', limite_inferior='', limite_superior='', tolerancia='')

if __name__ == '__main__':
    app.run(port=8003)