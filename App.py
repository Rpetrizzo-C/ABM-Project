from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin00'
app.config['MYSQL_DB'] = 'school'
mysql = MySQL(app)

app.secret_key = "mysecretkey"

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS alumnos ( `DNI` INT NOT NULL , `Nombre` TEXT NOT NULL , `Apellido` TEXT NOT NULL , PRIMARY KEY (`DNI`))')
    cur.execute('SELECT * FROM alumnos')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', alumnos=data)

@app.route('/add_alumnos', methods=['POST'])
def add_alumnos():
    if request.method == 'POST':
            DNI = request.form['DNI']
            Nombre = request.form['Nombre']
            Apellido = request.form['Apellido']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO alumnos (DNI, Nombre, Apellido) VALUES (%s, %s, %s)", (DNI, Nombre, Apellido))
            mysql.connection.commit()
            flash('Alumno agregado correctamente')
            return redirect(url_for('Index'))

@app.route('/edit/<DNI>', methods = ['POST','GET'])
def get_alumnos(DNI):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alumnos WHERE DNI = %s', [DNI])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-alumnos.html', alumnos = data[0])    

@app.route('/update/<DNI>', methods=['POST'])
def update_alumnos(DNI):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Apellido = request.form['Apellido']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE alumnos SET Nombre = %s, Apellido = %s WHERE DNI = %s""", (Nombre, Apellido, DNI))
        flash('Alumno Actualizado correctamente')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:DNI>', methods = ['POST','GET'])
def delete_alumnos(DNI):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM alumnos WHERE DNI = {0}'.format(DNI))
    mysql.connection.commit()
    flash('Alumno Eliminado correctamente')
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(port=3000, debug=True)