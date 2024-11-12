from flask import Flask, render_template, request
import numpy as np
import sympy as sp

app = Flask(__name__)

# Función para calcular la integral por el método de Simpson 3/8
def simpson_38(fx, a, b, n):
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

    # Aplicar la fórmula de Simpson 3/8
    integral = fi[0] + fi[-1]
    for i in range(1, n):
        if i % 3 == 0:
            integral += 2 * fi[i]
        else:
            integral += 3 * fi[i]

    integral *= (3 * h) / 8
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

        # Verificar si el número de particiones es múltiplo de 3 (Simpson 3/8 requiere que n sea múltiplo de 3)
        if n % 3 != 0:
            error = "El número de particiones debe ser múltiplo de 3."
            return render_template('index.html', error=error, fx=fx, a=a, b=b, n=n)

        # Calcular la integral
        resultado = simpson_38(fx, a, b, n)

        return render_template('index.html', resultado=resultado, fx=fx, a=a, b=b, n=n)

    except Exception as e:
        return render_template('index.html', error=str(e), fx=fx, a=request.form['a'], b=request.form['b'], n=request.form['n'])


if __name__ == '__main__':
    app.run(debug=True, port=8017)
