from . import db

# define the database models in this file
class Feedbacks(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    textFeedback = db.Column('textFeedback', db.Text, nullable=False)
    textInput = db.Column('textInput', db.Text, nullable=False)
    persModels = db.Column('persModels', db.String(100), nullable=False)
    nonpersModels = db.Column('nonpersModels', db.String(100), nullable=False)
    persuasive = db.Column('persuasive', db.String(100), nullable=False)
    wordCount = db.Column('wordCount', db.String(100), nullable=False)
    readabilityScore = db.Column('readabilityScore', db.String(100), nullable=False)
    ReadabilityGrade = db.Column('ReadabilityGrade', db.String(100), nullable=False)
    DiractionCount = db.Column('DiractionCount', db.String(100), nullable=False)
    WPS = db.Column('WPS', db.String(100), nullable=False)
    Sixltr = db.Column('Sixltr', db.String(100), nullable=False)
    pronoun = db.Column('pronoun', db.String(100), nullable=False)
    ppron = db.Column('ppron', db.String(100), nullable=False)
    i = db.Column('i', db.String(100), nullable=False)
    you = db.Column('you', db.String(100), nullable=False)
    ipron = db.Column('ipron', db.String(100), nullable=False)
    prep = db.Column('prep', db.String(100), nullable=False)
    auxverb = db.Column('auxverb', db.String(100), nullable=False)
    negate = db.Column('negate', db.String(100), nullable=False)
    numbers = db.Column('numbers', db.String(100), nullable=False)
    focuspast = db.Column('focuspast', db.String(100), nullable=False)
    focuspresent = db.Column('focuspresent', db.String(100), nullable=False)
    AllPunc = db.Column('AllPunc', db.String(100), nullable=False)
    Comma = db.Column('Comma', db.String(100), nullable=False)
    QMark = db.Column('QMark', db.String(100), nullable=False)
    Exemplify = db.Column('Exemplify', db.String(100), nullable=False)

    def __init__(self, textFeedback, textInput, persModels, nonpersModels, persuasive, wordCount,
                readabilityScore, ReadabilityGrade, DiractionCount, WPS, Sixltr, pronoun, ppron,
                i, you, ipron, prep, auxverb, negate, numbers, focuspast, focuspresent, AllPunc,
                Comma, QMark, Exemplify):
        self.textFeedback = textFeedback
        self.textInput = textInput
        self.persModels = persModels
        self.nonpersModels = nonpersModels
        self.persuasive = persuasive
        self.wordCount = wordCount
        self.readabilityScore = readabilityScore
        self.ReadabilityGrade = ReadabilityGrade
        self.DiractionCount = DiractionCount
        self.WPS = WPS
        self.Sixltr = Sixltr
        self.pronoun = pronoun
        self.ppron = ppron
        self.i = i
        self.you = you
        self.ipron = ipron
        self.prep = prep
        self.auxverb = auxverb
        self.negate = negate
        self.numbers = numbers
        self.focuspast = focuspast
        self.focuspresent = focuspresent
        self.AllPunc = AllPunc
        self.Comma = Comma
        self.QMark = QMark
        self.Exemplify = Exemplify

    def __repr__(self):
        return '<id {}>' % self.id
