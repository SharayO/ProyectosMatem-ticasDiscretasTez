from flask import Flask, render_template, request, redirect, url_for
import numpy as np

app = Flask(__name__)

def ajuste_minimos_cuadrados(x, y, grado):
    # Calcula los coeficientes del polinomio de ajuste
    coeficientes = np.polyfit(x, y, grado)
    # Calcula los valores predichos usando el polinomio
    y_pred = np.polyval(coeficientes, x)
    # Calcula el coeficiente de correlación R^2
    ss_res = np.sum((y - y_pred) ** 2)  # Suma de los residuos al cuadrado
    ss_tot = np.sum((y - np.mean(y)) ** 2)  # Suma total de los cuadrados
    r2 = 1 - (ss_res / ss_tot)
    return coeficientes.tolist(), r2

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Recibimos los puntos x e y del formulario
            x = list(map(float, request.form.get("x").split(",")))
            y = list(map(float, request.form.get("y").split(",")))

            # Validamos que el número de puntos x e y coincidan
            if len(x) != len(y):
                return "El número de valores de x e y deben coincidir", 400

            # Calculamos los ajustes para los grados 1 a 6
            ajustes = {}
            for grado in range(1, 7):
                coeficientes, r2 = ajuste_minimos_cuadrados(x, y, grado)
                ajustes[f"grado_{grado}"] = {
                    "coeficientes": coeficientes,
                    "r2": r2
                }

            return render_template("index.html", ajustes=ajustes)

        except Exception as e:
            return f"Error: {str(e)}", 400
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=8061)
