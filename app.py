from flask import Flask, render_template, request, redirect
import mysql.connector
import time
import os

app = Flask(__name__)


def obtener_conexion():

    while True:
        try:
            conexion = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=3306,
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            return conexion

        except:
            print("Esperando MySQL...")
            time.sleep(3)


# Crear la tabla si no existe
conexion = obtener_conexion()
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS aprendices(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    numero_documento VARCHAR(20) NOT NULL,
    ficha VARCHAR(20) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conexion.commit()
conexion.close()


@app.route("/")
def inicio():

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM aprendices ORDER BY id DESC")
    aprendices = cursor.fetchall()

    conexion.close()

    return render_template(
        "index.html",
        aprendices=aprendices
    )


@app.route("/registrar", methods=["POST"])
def registrar():

    nombre = request.form["nombre"]
    documento = request.form["documento"]
    ficha = request.form["ficha"]

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        INSERT INTO aprendices
        (nombre_completo, numero_documento, ficha)
        VALUES (%s, %s, %s)
        """,
        (nombre, documento, ficha)
    )

    conexion.commit()
    conexion.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)