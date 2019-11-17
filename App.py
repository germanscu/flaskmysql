from flask import Flask, render_template, request, redirect , url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
# conexion
app.config['MYSQL_HOST'] = '162.255.84.219'
app.config['MYSQL_USER'] = 'german'
app.config['MYSQL_PASSWORD'] = 'Scu@2019'
app.config['MYSQL_DB'] = 'agenda'
mysql = MySQL(app)

#configurar sesion
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM agenda.contactos')
    data = cur.fetchall()    
    return render_template('index.html', contactos = data)    

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
      fullname = request.form['fullname']  
      phone = request.form['phone']
      emial = request.form['email']
      cur = mysql.connection.cursor()
      cur.execute('INSERT INTO CONTACTOS (FULLNAME, PHONE, EMAIL) VALUES (%s, %s, %s)',(fullname,phone,emial))      
      mysql.connection.commit()
      flash('Agregado')      
      return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = {0}'.format(id))
    data = cur.fetchall()
    #cur.close()
    #print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
  if request.method == 'POST':
    fullname = request.form['fullname']
    phone = request.form['phone']
    email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE contactos
        set fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s    
    """, (fullname,email,phone,id))
    mysql.connection.commit()    
    flash('Cambio efectuado')    
    return redirect(url_for('Index'))

@app.route('/delete/<id>')
def delete_contact(id):    
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM CONTACTOS WHERE id = {0}'.format(id))    
    mysql.connection.commit()
    flash('Eliminado')      
    return redirect(url_for('Index'))
    

if __name__ == '__main__':    
 app.run(port = 3000, debug = True)

