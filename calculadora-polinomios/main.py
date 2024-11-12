from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import re
from matplotlib.ticker import MaxNLocator

app = Flask(__name__)

def process_polynomial(polinomio):
    polinomio = re.sub(r'(\d)(x)', r'\1*\2', polinomio)
    polinomio = re.sub(r'(x)\^(\d+)', r'\1**\2', polinomio)

    # Reemplazar cualquier cosa dentro de paréntesis elevada a (1/2) por np.sqrt(...)
    polinomio = re.sub(r'\(([^)]+)\)\*\*\(1/2\)', r'np.sqrt(\1)', polinomio)  # Raíz cuadrada de binomios u otras expresiones

    return polinomio

def get_coefficients(polinomio):
    p = np.poly1d(eval(polinomio.replace('x', 'np.poly1d([1,0])')))
    return p.coeffs

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calculate():
    polinomio = request.form["polinomio"]
    polinomio_procesado = process_polynomial(polinomio)
    x = np.linspace(-10, 10, 400)
    y = eval(polinomio_procesado)

    # Obtener los coeficientes del polinomio y calcular raíces
    coeffs = get_coefficients(polinomio_procesado)
    roots = np.roots(coeffs)
    real_roots = [r.real for r in roots if np.isreal(r)]

    # Crear el gráfico
    plt.figure()
    plt.plot(x, y, color="#ff000c")
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Gráfico del polinomio: {polinomio}')

    plt.xlim([-10, 10])
    plt.ylim([-10, 10])

    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=21))  # Eje X
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=21))  # Eje Y

    plt.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', graph_url='data:image/png;base64,{}'.format(graph_url), roots=real_roots)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
