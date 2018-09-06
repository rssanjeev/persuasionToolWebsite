import os
import csv
from . import tool
from . import main
from .. import db
from ..models import Feedbacks
# to access username and password for login
from flask import current_app as app
from flask import request, session, g, redirect, url_for, abort, \
                render_template, flash, send_from_directory


# used to get the abbr for model names
abbrDict = {"Gaussian Naive Bayes": "GNB", "Linear Discriminant Analysis": "LDA", "Logistic Regression": "LR", "Support Vector Machine": "SVM"}

@main.route('/')
def index():
    return render_template('homepage.html')

# handle events for the homepage, choose function check or compare
@main.route('/switch', methods = ['POST'])
def switch():
    if (request.form['switch'] == "Check a statement"):
        return render_template('check.html')
    elif (request.form['switch'] == "Compare two statements"):
        return render_template('compare.html', statement1="", statement2="")
    return redirect(url_for('main.index'))

# handle evens for the check page
@main.route('/check', methods = ['POST'])
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
        return redirect(url_for('main.nonmodels'))
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
@main.route('/nonmodels', methods = ['POST', 'GET'])
def nonmodels():
    flash("Please choose at least one model.")
    return render_template('check.html')

@main.route('/nonmodels2', methods = ['POST', 'GET'])
def nonmodels2():
    flash("Please choose at least one model.")
    return render_template('compare.html')

# handle event for compare page
@main.route('/compare', methods = ['POST'])
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
        return redirect(url_for('main.nonmodels2'))
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
@main.route('/feedback', methods = ['POST'])
def feedback():
    fea = session['features']
    pers = ", ".join(session['checkPersModels'])
    nonpers = ", ".join(session['checkNpersModels'])
    aFeedback = Feedbacks(textFeedback = request.form['textFeedback'], textInput = session['checkStatement'], persModels = pers, nonpersModels = nonpers, persuasive = request.form['persuasive'],
                wordCount = fea[0], readabilityScore = fea[1], ReadabilityGrade = fea[2], DiractionCount = fea[3],
                WPS = fea[4], Sixltr = fea[5], pronoun = fea[6], ppron = fea[7], i = fea[8], you = fea[9], ipron = fea[10], prep = fea[11],
                auxverb = fea[12], negate = fea[13], numbers = fea[14], focuspast = fea[15], focuspresent = fea[16], AllPunc = fea[17],
                Comma = fea[18], QMark = fea[19], Exemplify = fea[20])
    db.session.add(aFeedback)
    db.session.commit()
    flash('Thank you for your feedback!')
    return redirect(url_for('main.index'))

# add feedbacks for compare to local database
@main.route('/feedbackCompare1', methods = ['POST', 'GET'])
def feedbackCompare1():
    fea = session['featureSt1']
    pers = ", ".join(session['persModSt1'])
    nonpers = ", ".join(session['nperModSt1'])
    aFeedback = Feedbacks(textFeedback = request.form['textFeedback'], textInput = session['statement1'], persModels = pers, nonpersModels = nonpers, persuasive = request.form['persuasive'],
                wordCount = fea[0], readabilityScore = fea[1], ReadabilityGrade = fea[2], DiractionCount = fea[3],
                WPS = fea[4], Sixltr = fea[5], pronoun = fea[6], ppron = fea[7], i = fea[8], you = fea[9], ipron = fea[10], prep = fea[11],
                auxverb = fea[12], negate = fea[13], numbers = fea[14], focuspast = fea[15], focuspresent = fea[16], AllPunc = fea[17],
                Comma = fea[18], QMark = fea[19], Exemplify = fea[20])
    db.session.add(aFeedback)
    db.session.commit()
    return render_template('feedbackCompare2.html', feedbackText=session['statement2'])

# add feedbacks for compare to local database
@main.route('/feedbackCompare2', methods = ['POST', 'GET'])
def feedbackCompare2():
    fea = session['featureSt2']
    pers = ", ".join(session['persModSt2'])
    nonpers = ", ".join(session['nperModSt2'])
    aFeedback = Feedbacks(textFeedback = request.form['textFeedback'], textInput = session['statement2'], persModels = pers, nonpersModels = nonpers, persuasive = request.form['persuasive'],
                wordCount = fea[0], readabilityScore = fea[1], ReadabilityGrade = fea[2], DiractionCount = fea[3],
                WPS = fea[4], Sixltr = fea[5], pronoun = fea[6], ppron = fea[7], i = fea[8], you = fea[9], ipron = fea[10], prep = fea[11],
                auxverb = fea[12], negate = fea[13], numbers = fea[14], focuspast = fea[15], focuspresent = fea[16], AllPunc = fea[17],
                Comma = fea[18], QMark = fea[19], Exemplify = fea[20])
    db.session.add(aFeedback)
    db.session.commit()
    flash('Thank you for your feedback!')
    return redirect(url_for('main.index'))

# handle the admin login event
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('Wrong username/password')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('Wrong username/password')
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('main.admin'))
    return render_template('login.html')

# get all the information needed in the database to display on the admin page
@main.route('/admin')
def admin():
    if not session.get('logged_in'):
        abort(401)
    feedbackObjs = Feedbacks.query
    feedbacks = [[f.textFeedback, f.textInput, f.persModels, f.nonpersModels, f.persuasive] for f in feedbackObjs]
    return render_template('admin.html', feedbacks=feedbacks)

# clear all entries in the databse
@main.route('/admin/init', methods = ['POST'])
def init():
    Feedbacks.query.delete()
    db.session.commit()
    flash("Initiated the database successfully!")
    return redirect(url_for('main.admin'))

# export data in local database to persuasiveClassification.csv and npersuasiveClassification.csv
@main.route('/download/<filename>', methods = ['GET'])
def export(filename):
    if not session.get('logged_in'):
        abort(401)
    totalNum = Feedbacks.query.count();
    dirpath = os.path.join('app', 'static', 'download')
    filepath = os.path.join(dirpath, filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    with open(filepath, 'a') as csvfile:
        # !!!!!!!!!!!! DO NOT try to remove this part, this part can be used to create the head for the csv file
        rowHead = ["SID", "text", "id", "tfidf", "deltaAwarded", "created", "numComments",
                "existingComments", "differenceInSeconds", "differenceInDays", "readabilityScore",
                "words", "syllables", "sentences", "authorFlair", "additionCount", "conseqCount",
                "contrastCount", "directionCount", "diversionCount", "incidentallyCount", "exceptionCount",
                "exemplifyCount", "generalizingCount", "illustrationCount", "similarityCount",
                "restatementCount", "sequenceCount", "summerizingCount", "allTransitions",
                "lexicalOverlapScore", "lexicalDiversityScore", "relevanceRankMetric",
                "relevancerank", "temporalRankMetric", "WC", "Analytic", "Clout", "Authentic",
                "Tone", "WPS", "Sixltr", "Dic", "function", "pronoun", "ppron", "i", "we", "you",
                "shehe", "they", "ipron", "article", "prep", "auxverb", "adverb", "conj", "negate",
                "verb", "adj", "compare", "interrog", "number", "quant", "affect", "posemo", "negemo",
                "anx", "anger", "sad", "social", "family", "friend", "female", "male", "cogproc",
                "insight", "cause", "discrep", "tentat", "certain", "differ", "percept", "see", "hear",
                "feel", "bio", "body", "health", "sexual", "ingest", "drives", "affiliation", "achieve",
                "power", "reward", "risk", "focuspast", "focuspresent", "focusfuture", "relativ", "motion",
                "space", "time", "work", "leisure", "home", "money", "relig", "death", "informal", "swear",
                "netspeak", "assent", "nonflu", "filler", "AllPunc", "Period", "Comma", "Colon", "SemiC",
                "QMark", "Exclam", "Dash", "Quote", "Apostro", "Parenth", "OtherP"]
        firstRow = ','.join(rowHead)
        csvfile.write(firstRow)

        allFeedbacks = Feedbacks.query
        for f in allFeedbacks:
            rowList = [""] * 128
            input = f.textInput
            input = input.replace("\"", "\"\"")
            input = "\"" + input + "\""

            if f.persuasive == 'Persuasive': result = '1';
            else: result = '0';

            rowList[1] = input # input B
            rowList[4] = result # result E
            rowList[35] = f.wordCount # wordCount AJ
            rowList[10] = f.readabilityScore # readabilityScore K
            rowList[18] = f.DiractionCount # diractionCount S
            rowList[40] = f.WPS # WPS AO
            rowList[41] = f.Sixltr # sixltr AP
            rowList[44] = f.pronoun # pronoun AS
            rowList[45] = f.ppron # ppron AT
            rowList[46] = f.i # i AU
            rowList[48] = f.you # you AW
            rowList[51] = f.ipron # ipron AZ
            rowList[53] = f.prep # prep BB
            rowList[54] = f.auxverb # auxverb BC
            rowList[57] = f.negate # negate BF
            rowList[62] = f.numbers # numbers BK
            rowList[97] = f.focuspast # focuspast CT
            rowList[98] = f.focuspresent # focuspresent CU
            rowList[116] = f.AllPunc # allPunc DM
            rowList[118] = f.Comma # comma DO
            rowList[121] = f.QMark # qMark DR
            rowList[22] = f.Exemplify # exemplify W
            row = ','.join(rowList)
            row = "\n" + row
            csvfile.write(row)

    if os.path.isfile(os.path.join(dirpath, filename)):
        # flash("Exported " + str(totalNum) + " records successfully!")
        return send_from_directory(os.path.join('static', 'download'), filename, as_attachment=True)

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
