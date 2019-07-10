from flask import Flask, request, render_template, redirect, url_for, session
import psycopg2
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

app = Flask(__name__)
app.secret_key = 'monApp'
 
@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		cnx = psycopg2.connect(database="Ecole", user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432")
		cur = cnx.cursor()
		cur.execute("SELECT * FROM profs")
		data = cur.fetchall()
		for d in data:
			if request.form['login'] == d[0] and request.form['passe'] == d[1]:
				msg = ''
				session['username'] = request.form['login']
				return redirect(url_for('index'))
			else:
				msg = 'Login ou mot de passe incorrecte'

	return render_template('login.html', erreur = msg)

@app.route('/', methods=['GET', 'POST'])
def index():
	if 'username' in session:
		return render_template('accueil.html')
	return redirect(url_for('login'))

@app.route('/deconnexion', methods=['GET'])
def deconnexion():
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/licence/algorithmique', methods=['GET', 'POST'])
def historique_algo():
	global cours
	con = psycopg2.connect(database="Ecole", user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute("SELECT * FROM cours_algo")
	rows = cur.fetchall()
	con.close()
	if request.method == 'POST':
		cours = 'Algorithmique'
		return redirect(url_for('emargement'))
	return render_template('historique_algo.html', ligne = rows)

@app.route('/licence/robotique', methods=['GET', 'POST'])
def historique_robot():
	global cours
	con = psycopg2.connect(database="Ecole", user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute("SELECT * FROM cours_robot")
	rows = cur.fetchall()
	con.close()
	if request.method == 'POST':
		cours = 'Robotique'
		return redirect(url_for('emargement'))
	return render_template('historique_robot.html', ligne = rows)

@app.route('/licence/programmationpython', methods=['GET', 'POST'])
def historique_progpy():
	global cours
	con = psycopg2.connect(database="Ecole", user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS cours_progpy (dates VARCHAR(15) NOT NULL, lecons VARCHAR(100) NOT NULL, absents VARCHAR(100) NOT NULL)''')
	cur.execute("SELECT * FROM cours_progpy")
	rows = cur.fetchall()
	con.close()
	if request.method == 'POST':
		cours = 'Programmation Python'
		return redirect(url_for('emargement'))
	return render_template('historique_progpy.html', ligne = rows)

@app.route('/licence/designinterfacelogiciel', methods=['GET', 'POST'])
def historique_dil():
	global cours
	con = psycopg2.connect(database="Ecole", user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432")
	cur = con.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS cours_dil (dates VARCHAR(15) NOT NULL, lecons VARCHAR(100) NOT NULL, absents VARCHAR(100) NOT NULL)''')
	cur.execute("SELECT * FROM cours_dil")
	rows = cur.fetchall()
	con.close()
	if request.method == 'POST':
		cours = 'Design d\'Interface Logiciel'
		return redirect(url_for('emargement'))
	return render_template('historique_dil.html', ligne = rows)
	

@app.route('/licence/emargement', methods=['GET', 'POST'])
def emargement():
	if request.method == 'POST':
		dates = request.form['dates']
		lecon = request.form['lecons']
		absent = request.form['absents']
		conn = psycopg2.connect(database="Ecole", user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432")
		cur = conn.cursor()

		if cours == 'Algorithmique':
			if dates == '' or lecon == '':
				return render_template('emargement.html', cour = cours)
			else:
				cur.execute('''CREATE TABLE IF NOT EXISTS cours_algo (dates VARCHAR(15) NOT NULL, lecons VARCHAR(100) NOT NULL, absents VARCHAR(100) NOT NULL)''')
				cur.execute("INSERT INTO cours_algo VALUES (%s,%s,%s)", (dates,lecon,absent))
				conn.commit()
				return redirect(url_for('historique_algo'))
		elif cours == 'Robotique':
			if dates == '' or lecon == '':
				return render_template('emargement.html', cour = cours)
			else:
				cur.execute('''CREATE TABLE IF NOT EXISTS cours_robot (dates VARCHAR(15) NOT NULL, lecons VARCHAR(100) NOT NULL, absents VARCHAR(100) NOT NULL)''')
				cur.execute("INSERT INTO cours_robot VALUES (%s,%s,%s)", (dates,lecon,absent))
				conn.commit()
				return redirect(url_for('historique_robot'))
		elif cours == 'Programmation Python':
			if dates == '' or lecon == '':
				return render_template('emargement.html', cour = cours)
			else:
				cur.execute('''CREATE TABLE IF NOT EXISTS cours_progpy (dates VARCHAR(15) NOT NULL, lecons VARCHAR(100) NOT NULL, absents VARCHAR(100) NOT NULL)''')
				cur.execute("INSERT INTO cours_progpy VALUES (%s,%s,%s)", (dates,lecon,absent))
				conn.commit()			
				return redirect(url_for('historique_progpy'))
		elif cours == 'Design d\'Interface Logiciel':
			if dates == '' or lecon == '':
				return render_template('emargement.html', cour = cours)
			else:
				cur.execute('''CREATE TABLE IF NOT EXISTS cours_dil (dates VARCHAR(15) NOT NULL, lecons VARCHAR(100) NOT NULL, absents VARCHAR(100) NOT NULL)''')
				cur.execute("INSERT INTO cours_dil VALUES (%s,%s,%s)", (dates,lecon,absent))
				conn.commit()			
				return redirect(url_for('historique_dil'))
		conn.close()
	return render_template('emargement.html', cour = cours)

@app.route('/enregistrement', methods=['GET', 'POST'])
def enregistrement():
	if request.method == 'POST':
		user = request.form['user']
		passw = request.form['passw']
		confir = request.form['confirmation']

		erruser = 'Veuillez renseigner le nom d\'utilisateur !'
		errpass = 'Veuillez renseigner le mot de passe !'
		errconf = 'Confirmation non similaire !'

		if user == '' and passw == '' and confir == '':
			return render_template('enregistrement.html', msgpass = errpass, msguser = erruser, msgconf = errconf)
		elif user == '':
			errpass = ''
			errconf = ''
			return render_template('enregistrement.html', msguser = erruser, msgpass = errpass, msgconf = errconf)
		elif passw == '':
			erruser = ''
			errconf = ''
			return render_template('enregistrement.html', msgpass = errpass, msguser = erruser, msgconf = errconf)
		elif confir != passw:
			erruser = ''
			errpass = ''
			return render_template('enregistrement.html', msgconf = errconf, msguser = erruser, msgpass = errpass)
		else:
			cnx = psycopg2.connect(database="Ecole", user = "postgres", password = "123456789", host = "127.0.0.1", port = "5432")
			cur = cnx.cursor()
			cur.execute("SELECT * FROM profs")
			data = cur.fetchall()
			for d in data:
				if request.form['user'] == d[0] and request.form['confirmation'] == d[1]:
					msg = 'Cet utilisateur existe deja'
					return render_template('enregistrement.html', err = msg)
			msg = ''
			cur.execute("INSERT INTO profs VALUES (%s, %s)", (user, passw))
			cnx.commit()
			cnx.close()
			return redirect(url_for('login'))
	return render_template('enregistrement.html')

if __name__ == '__main__':
	app.run(debug=True)
