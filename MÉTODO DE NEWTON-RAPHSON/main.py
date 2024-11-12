from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

# Definir la variable simbólica
x = sp.symbols('x')

# Definir la función y su derivada utilizando solo SymPy
f = sp.exp(x * sp.log(2)) + x**2 - 4
f_prime = sp.diff(f, x)

# Método de Newton-Raphson utilizando SymPy
def newton_raphson(f, f_prime, x0, tol, max_iter=100):
    iteraciones = []
    for i in range(max_iter):
        f_x0 = f.subs(x, x0).evalf()  # Evaluar numéricamente
        f_prime_x0 = f_prime.subs(x, x0).evalf()  # Evaluar numéricamente

        if f_prime_x0 == 0:
            return None, iteraciones, "La derivada es cero. No se puede continuar."

        x1 = x0 - f_x0 / f_prime_x0  # Método de Newton-Raphson
        error = abs(x1 - x0).evalf()  # Evaluar numéricamente
        iteraciones.append({
            'x0': x0,
            'raiz': x1,
            'error': error
        })

        if error < tol:
            return x1.evalf(), iteraciones, None  # Devolver valor evaluado

        x0 = x1

    return None, iteraciones, "Número máximo de iteraciones alcanzado."

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    iteraciones = []
    error = None
    if request.method == 'POST':
        funcion = request.form['funcion']
        punto_inicial = float(request.form['punto_inicial'])
        tolerancia = float(request.form['tolerancia'])

        # Usar Newton-Raphson para encontrar la raíz
        raiz, iteraciones, error = newton_raphson(f, f_prime, punto_inicial, tolerancia)

        if raiz is not None:
            resultado = {'raiz': raiz, 'error': iteraciones[-1]['error']}

    return render_template('index.html', resultado=resultado, iteraciones=iteraciones, error=error)


if __name__ == '__main__':
    app.run(debug=True, port=8001)

