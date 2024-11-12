from flask import Flask, render_template, request
import numpy as np
import sympy as sp

app = Flask(__name__)

# Función para calcular la integral por el método de Simpson 1/3
def simpson(fx, a, b, n):
    x = sp.symbols('x')
    f = sp.sympify(fx)  # Convertir la cadena de texto en una función simbólica de SymPy

    # Convertir a y b a float
    a = float(a)
    b = float(b)

    # Calcular h (el tamaño de los subintervalos)
    h = (b - a) / n

    # Definir los puntos x
    xi = np.linspace(a, b, n+1)

    # Evaluar la función en los puntos xi
    fi = [f.subs(x, val) for val in xi]

    # Aplicar la fórmula de Simpson 1/3
    integral = fi[0] + fi[-1]
    for i in range(1, n):
        if i % 2 == 0:
            integral += 2 * fi[i]
        else:
            integral += 4 * fi[i]

    integral *= h / 3
    return float(integral)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        # Obtener datos del formulario
        fx = request.form['fx']
        a = request.form['a']
        b = request.form['b']
        n = request.form['n']

        # Convertir a y b a float y n a int
        a = float(a)
        b = float(b)
        n = int(n)

        # Verificar si el número de particiones es par (Simpson 1/3 requiere que n sea par)
        if n % 2 != 0:
            error = "El número de particiones debe ser par."
            return render_template('index.html', error=error, fx=fx, a=a, b=b, n=n)

        # Calcular la integral
        resultado = simpson(fx, a, b, n)

        return render_template('index.html', resultado=resultado, fx=fx, a=a, b=b, n=n)

    except Exception as e:
        return render_template('index.html', error=str(e), fx=fx, a=request.form['a'], b=request.form['b'], n=request.form['n'])


if __name__ == '__main__':
    app.run(debug=True, port=80)
