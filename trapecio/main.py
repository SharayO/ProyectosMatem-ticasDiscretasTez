from flask import Flask, render_template, request
import sympy as sp
import numpy as np

app = Flask(__name__)

# Función de integración por trapecios usando sympy y numpy para la generación de puntos
def trapecios(f, a, b, n):
    x = sp.Symbol('x')
    f_lambdified = sp.lambdify(x, f, 'numpy')  # Convertir la expresión simbólica a una función de numpy
    x_vals = np.linspace(a, b, n + 1)  # Generar puntos equidistantes entre a y b usando numpy
    y_vals = f_lambdified(x_vals)  # Evaluar la función en esos puntos
    h = (b - a) / n
    integral = (h / 2) * (y_vals[0] + 2 * sum(y_vals[1:-1]) + y_vals[-1])
    return integral

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    a = None
    b = None
    funcion = ""
    n = None

    if request.method == "POST":
        try:
            # Obtener los valores del formulario
            funcion = request.form["funcion"]

            # Crear una expresión simbólica utilizando sympy
            x = sp.Symbol('x')
            f = sp.sympify(funcion)  # Convertir la cadena de texto en una expresión simbólica

            # Obtener los límites de integración y el número de subintervalos
            a = float(request.form["a"])
            b = float(request.form["b"])
            n = int(request.form["n"])

            # Calcular la integral usando el método de los trapecios
            result = trapecios(f, a, b, n)

            # Calcular error estimado comparando con n/2 particiones
            result_n2 = trapecios(f, a, b, n // 2)
            error = abs(result - result_n2)

        except Exception as e:
            error = f"Error: {str(e)}"

    # Enviar los valores de entrada y resultados a la plantilla
    return render_template("index.html", result=result, error=error, funcion=funcion, a=a, b=b, n=n)

if __name__ == '__main__':
    app.run(debug=True, port=8011)
