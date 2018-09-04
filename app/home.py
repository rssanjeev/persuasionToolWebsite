import os
import tool
import sqlite3
import csv
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory

app = Flask(__name__)
app.config.from_envvar('TOOL_SETTINGS', silent = True)
# secret key for flask
app.secret_key = "V\x827\\k,\xc1W\x91r\x1a\xcdw\x03\x83\xcd"
# username and password for admin
app.config['USERNAME'] = 'BITSLAB'
app.config['PASSWORD'] = 'bitslabpersuasion'
# PASSWORD = 'bitslabpersuasion'

# local database
DATABASE = 'app/feedbacks.db'
# used to get the abbr for model names
abbrDict = {"Gaussian Naive Bayes": "GNB", "Linear Discriminant Analysis": "LDA", "Logistic Regression": "LR", "Support Vector Machine": "SVM"}

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.before_request
def before_request():
    g.db = get_db()

# function used to create the database file
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('app/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    return render_template('homepage.html')

# handle events for the homepage, choose function check or compare
@app.route('/switch', methods = ['POST'])
def switch():
    if (request.form['switch'] == "Check a statement"):
        return render_template('check.html')
    elif (request.form['switch'] == "Compare two statements"):
        return render_template('compare.html', statement1="", statement2="")
    return redirect(url_for('index'))

# handle evens for the check page
@app.route('/check', methods = ['POST'])
def check():
    # empty statement, return a waring
    if (len(request.form['text']) == 0):
        flash("Please enter a statement")
        return render_template('check.html')
    # save the model names which consider the statement is persuasive
    pers = []
    # save the model names which consider the statement is nonpersuasive
    nonpers = []
    session['features'] = []
    str1 = ""
    str2 = ""
    result = tool.textCheck(request.form['text'], request.form.getlist('models'))
    session['features'] = tool.gettingFeatures(request.form['text'])
    if len(result) == 0:
        return redirect(url_for('nonmodels'))
    # (1.0, array([[0.06497868, 0.93502132]]), 'GaussianNB')
    for res in result:
        # flash(str(res))
        if res[0] >= 1:
            pers.append(res[2])
        else:
            nonpers.append(res[2])
    if len(pers) != 0:
        for p in pers:
            str1 += " " + p + ","
        flash("The statement is persuasive using:" + str1[:len(str1) - 1])
    if len(nonpers) != 0:
        for np in nonpers:
            str2 += " " + np + ","
        flash("The statement is nonpersuasive using:" + str2[:len(str2) - 1])

    # add model names and statement to seesion, which would be used by the feedback part
    session['checkPersModels'] = []
    session['checkNpersModels'] = []
    session['checkStatement'] = request.form['text']
    nonpersAbbr = []
    for model in pers:
        session['checkPersModels'].append(abbrDict[model])
    for model in nonpers:
        session['checkNpersModels'].append(abbrDict[model])

    return render_template('feedback.html', feedbackText=session['checkStatement'])

# warning message for no models choosed
@app.route('/nonmodels', methods = ['POST', 'GET'])
def nonmodels():
    flash("Please choose at least one model.")
    return render_template('check.html')

@app.route('/nonmodels2', methods = ['POST', 'GET'])
def nonmodels2():
    flash("Please choose at least one model.")
    return render_template('compare.html')

# handle event for compare page
@app.route('/compare', methods = ['POST'])
def compare():
    # warning message for no statement entered
    if (len(request.form['text1']) == 0 or len(request.form['text2']) == 0):
        flash("Please enter two statements.")
        return render_template('compare.html')
    models = request.form.getlist('models');
    # save the models indicate which statement is persuasive
    st1 = []
    st2 = []
    str1 = ""
    str2 = ""
    # add features, model names to session, which would be used in the feedback part
    session['featureSt1'] = []
    session['featureSt1'] = []
    session['persModSt1'] = []
    session['nperModSt1'] = []
    session['persModSt2'] = []
    session['nperModSt2'] = []
    if len(models) == 0:
        return redirect(url_for('nonmodels2'))
    result1 = tool.textCheck(request.form['text1'], models)
    result2 = tool.textCheck(request.form['text2'], models)

    for i in range(len(models)):
        tup1 = result1[i]
        tup2 = result2[i]

        if tup1[0] == 1:
            st1.append(tup1[2])
            session['persModSt1'].append(abbrDict[tup1[2]])
        if (tup1[0] < 1):
            session['nperModSt1'].append(abbrDict[tup1[2]])
        if tup2[0] == 1:
            st2.append(tup2[2])
            session['persModSt2'].append(abbrDict[tup2[2]])
        if tup2[0] < 1:
            session['nperModSt2'].append(abbrDict[tup2[2]])

    if len(st1) != 0:
        for s in st1:
            str1 += " " + s + ","
        flash("The first statement is persuasive using:" + str1[:len(str1) - 1])
    if len(st2) != 0:
        for s in st2:
            str2 += " " + s + ","
        flash("The second statement is persuasive using:" + str2[:len(str2) - 1])
    if len(st1) > len(st2):
        flash("Based on above results, the first statement is more persuasive.")
    elif len(st2) > len(st1):
        flash("Based on above results, the second statement is more persuasive.")
    else:
        flash("Based on above results, the two statements are equally persuasive.")

    # add statemnt to session, which would be used in the feedbback part
    session['statement1'] = request.form['text1']
    session['statement2'] = request.form['text2']
    session['featureSt1'] = tool.gettingFeatures(request.form['text1'])
    session['featureSt2'] = tool.gettingFeatures(request.form['text2'])

    return render_template('feedbackCompare1.html', feedbackText=session['statement1'])

# add feedbacks for check to local databse
@app.route('/feedback', methods = ['POST'])
def feedback():
    pers = ", ".join(session['checkPersModels'])
    nonpers = ", ".join(session['checkNpersModels'])
    feedbackList = [request.form['textFeedback'], session['checkStatement'], pers, nonpers, request.form['persuasive']]
    feedbackList.extend(session['features'])
    # features = [wordCount, readabilityScore, ReadabilityGrade, DiractionCount, WPS, Sixltr, pronoun, ppron, i, you, ipron, prep, auxverb, negate, number, focuspast, focuspresent, AllPunc, Comma, QMark, Exemplify]
    g.db.execute('insert into feedbacks (textFeedback, textInput, persModels, nonpersModels, persuasive, wordCount, readabilityScore, ReadabilityGrade, DiractionCount, WPS, Sixltr, pronoun, ppron, i, you, ipron, prep, auxverb, negate, numbers, focuspast, focuspresent, AllPunc, Comma, QMark, Exemplify) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', feedbackList)
    g.db.commit()
    flash('Thank you for your feedback!')
    return redirect(url_for('index'))

# add feedbacks for compare to local database
@app.route('/feedbackCompare1', methods = ['POST', 'GET'])
def feedbackCompare1():
    pers = ", ".join(session['persModSt1'])
    nonpers = ", ".join(session['nperModSt1'])
    feedbackList = [request.form['textFeedback'], session['statement1'], pers, nonpers, request.form['persuasive']]
    feedbackList.extend(session['featureSt1'])
    g.db.execute('insert into feedbacks (textFeedback, textInput, persModels, nonpersModels, persuasive, wordCount, readabilityScore, ReadabilityGrade, DiractionCount, WPS, Sixltr, pronoun, ppron, i, you, ipron, prep, auxverb, negate, numbers, focuspast, focuspresent, AllPunc, Comma, QMark, Exemplify) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', feedbackList)
    g.db.commit()
    return render_template('feedbackCompare2.html', feedbackText=session['statement2'])

# add feedbacks for compare to local database
@app.route('/feedbackCompare2', methods = ['POST', 'GET'])
def feedbackCompare2():
    pers = ", ".join(session['persModSt2'])
    nonpers = ", ".join(session['nperModSt2'])
    feedbackList = [request.form['textFeedback'], session['statement2'], pers, nonpers, request.form['persuasive']]
    feedbackList.extend(session['featureSt2'])
    g.db.execute('insert into feedbacks (textFeedback, textInput, persModels, nonpersModels, persuasive, wordCount, readabilityScore, ReadabilityGrade, DiractionCount, WPS, Sixltr, pronoun, ppron, i, you, ipron, prep, auxverb, negate, numbers, focuspast, focuspresent, AllPunc, Comma, QMark, Exemplify) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', feedbackList)
    g.db.commit()
    flash('Thank you for your feedback!')
    return redirect(url_for('index'))

# handle the admin login event
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('admin'))
    return render_template('login.html', error=error)

# get all the information needed in the database to display on the admin page
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.execute('select textFeedback, textInput, persModels, nonpersModels, persuasive from feedbacks order by id desc')
    # feedbacks = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    feedbacks = [[row[0], row[1], row[2], row[3], row[4]] for row in cur.fetchall()]
    return render_template('admin.html', feedbacks=feedbacks)

# clear all entries in the databse
@app.route('/admin/init', methods = ['POST'])
def init():
    init_db();
    flash("Initiated the database successfully!")
    return redirect(url_for('admin'))

# export data in local database to persuasiveClassification.csv and npersuasiveClassification.csv
@app.route('/admin/export', methods = ['POST'])
def export():
    persPath = os.path.join("app", "persuasiveClassification.csv")
    npersPath = os.path.join("app", "npersuasiveClassification.csv")
    dirPath = os.path.join("app", "download")
    filename = "persuasiveClassification.csv"
    pers = open(persPath, "a")
    npers = open(npersPath, "a")
    cur = g.db.execute('select textFeedback, textInput, persModels, nonpersModels, persuasive, wordCount, readabilityScore, ReadabilityGrade, DiractionCount, WPS, Sixltr, pronoun, ppron, i, you, ipron, prep, auxverb, negate, numbers, focuspast, focuspresent, AllPunc, Comma, QMark, Exemplify from feedbacks order by id desc')
    data = [row[:] for row in cur.fetchall()]
    # there is no readabilityGrade in the sheet
    for p in data:
        if str(p[4]) == "Persuasive":
            rowList = ["N/A"] * 128
            input1 = str(p[1])
            input1 = input1.replace("\"", "\"\"")
            input1 = "\"" + input1 + "\""
            rowList[1] = input1 # input B
            rowList[4] = "1" # result E
            rowList[35] = str(p[5]) # wordCount AJ
            rowList[10] = str(p[6]) # readabilityScore K
            rowList[18] = str(p[8]) # diractionCount S
            rowList[40] = str(p[9]) # WPS AO
            rowList[41] = str(p[10]) # sixltr AP
            rowList[44] = str(p[11]) # pronoun AS
            rowList[45] = str(p[12]) # ppron AT
            rowList[46] = str(p[13]) # i AU
            rowList[48] = str(p[14]) # you AW
            rowList[51] = str(p[15]) # ipron AZ
            rowList[53] = str(p[16]) # prep BB
            rowList[54] = str(p[17]) # auxverb BC
            rowList[57] = str(p[18]) # negate BF
            rowList[62] = str(p[19]) # numbers BK
            rowList[97] = str(p[20]) # focuspast CT
            rowList[98] = str(p[21]) # focuspresent CU
            rowList[116] = str(p[22]) # allPunc DM
            rowList[118] = str(p[23]) # comma DO
            rowList[121] = str(p[24]) # qMark DR
            rowList[22] = str(p[25]) # exemplify W
            row = ','.join(rowList)
            row = "\n" + row
            pers.write(row)
        if str(p[4]) == "Nonpersuasive":
            rowList = ["N/A"] * 128
            input2 = str(p[1])
            input2 = input2.replace("\"", "\"\"")
            input2 = "\"" + input2 + "\""
            rowList[1] = input2 # input B
            rowList[4] = "0" # result E
            rowList[35] = str(p[5]) # wordCount AJ
            rowList[10] = str(p[6]) # readabilityScore K
            rowList[18] = str(p[8]) # diractionCount S
            rowList[40] = str(p[9]) # WPS AO
            rowList[41] = str(p[10]) # sixltr AP
            rowList[44] = str(p[11]) # pronoun AS
            rowList[45] = str(p[12]) # ppron AT
            rowList[46] = str(p[13]) # i AU
            rowList[48] = str(p[14]) # you AW
            rowList[51] = str(p[15]) # ipron AZ
            rowList[53] = str(p[16]) # prep BB
            rowList[54] = str(p[17]) # auxverb BC
            rowList[57] = str(p[18]) # negate BF
            rowList[62] = str(p[19]) # numbers BK
            rowList[97] = str(p[20]) # focuspast CT
            rowList[98] = str(p[21]) # focuspresent CU
            rowList[116] = str(p[22]) # allPunc DM
            rowList[118] = str(p[23]) # comma DO
            rowList[121] = str(p[24]) # qMark DR
            rowList[22] = str(p[25]) # exemplify W
            row = ','.join(rowList)
            row = "\n" + row
            npers.write(row)

    flash("Exported " + str(len(data)) + " records successfully!")
    return send_from_directory(dirPath, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
