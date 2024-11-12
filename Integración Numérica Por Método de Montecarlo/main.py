from flask import Flask, render_template, request
import random
import sympy as sp

app = Flask(__name__)

# Función para integrar usando el método de Montecarlo
def montecarlo_integration(fx, a, b, N):
    x = sp.symbols('x')  # Definir la variable simbólica
    f = sp.sympify(fx)  # Convertir la función de string a expresión simbólica
    f_lambda = sp.lambdify(x, f)  # Convertir la expresión en función numérica

    total_area = 0
    for _ in range(N):
        # Generar un punto aleatorio en el intervalo [a, b]
        random_x = random.uniform(a, b)
        total_area += f_lambda(random_x)

    # Calcular el valor aproximado de la integral
    integral_value = (b - a) * total_area / N
    return integral_value, N

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        # Obtener los datos del formulario
        fx = request.form['fx']
        a = float(request.form['a'])
        b = float(request.form['b'])
        N = int(request.form['N'])

        # Calcular la integral usando Montecarlo
        integral_value, puntos_contados = montecarlo_integration(fx, a, b, N)

        return render_template('index.html', fx=fx, a=a, b=b, N=N,
                               puntos_contados=puntos_contados, resultado=integral_value)
    except Exception as e:
        return render_template('index.html', error=str(e))
    
if __name__ == '__main__':
    app.run(debug=True, port=81)
