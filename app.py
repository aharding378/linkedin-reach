#Word guessing game for Linkedin REACH apprenticeship
#By Alex Harding
#Created 11/14/18

from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_moment import Moment
import urllib.request, random

#App configurations and initis
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#init database
db = SQLAlchemy(app)

#init flask moment
moment = Moment(app)

#Create database table for leaderboard
class User(db.Model):
    __tablename__ = 'leaderboard'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime,index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

#encryp function
def encrypt_word(word, key):
    #Using a list comprehension to convert letters to ascii
    asc_word = [ord(letter) + key for letter in word]

    #Converting the ascii to string for ajax request from front end
    asc_word = ''.join(str(letter) + ','  for letter in asc_word)

    return asc_word

#decrypt functio
def decrypt_word(word, key):
    #decrypt and convert ascii to string
    chr_word = ''.join(chr(int(letter) - key)  for letter in word)

    return chr_word

#cryptography keys
keys = [13, 43, 54, 27, 63, 47, 78, 83, 49, 23]

@app.route('/')
def word_guessing():

    #get difficulty level
    level = request.args.get('level')

    #get game level btw 1 - 10 and also check for errors
    try:
        if not level:
            difficulty = '1'
        elif int(level) > 10 or int(level) < 1:
            difficulty = '1'
        else:
            difficulty = level
    except:
        difficulty = '1'

    #Get words from linkedin url
    try:
        url = "http://app.linkedin-reach.io/words?difficulty=" + difficulty

        with urllib.request.urlopen(url) as response:
            words = response.read()

        #Check if response fails - TODO

        #Sonverts words into an array of words
        words = str(words).split('\\n')

        #pick a random word from the array
        word = random.choice(words)

        #Get length of word to display dashes
        length = len(word)

        #Get length of word recording multiple occurrences a 1
        letters = ''
        occurrence_length = 0
        for letter in word:
            if letter not in letters:
                letters += letter
                occurrence_length += 1

        #Get random encryption key
        key = random.choice(keys)

        #Encrypt word
        word = encrypt_word(word, key)

        #change original key for frontend
        key = key + 13
    except:
        word = None
        key = None
        occurrence_length = 0
        length = 0


    #get players for leaderboard in descending order
    players = User.query.order_by(User.score.desc()).all()

    return render_template('index.html', word=word, length=length, difficulty=int(difficulty),
                           occurrence_length=occurrence_length, key=key, players=players)


@app.route('/guess', methods=['GET'])
def guess():
    #Get request data
    word = request.args.get('hangman')
    guessing = request.args.get('guessing')
    key = request.args.get('key')

    #converting word to list of ascii values
    word = word.split(',')

    #Delete trailing '' from list
    word.pop()

    #Decrypt word
    word = decrypt_word(word, int(key) - 13)

    if guessing:
        #get guessed value
        guess = request.args.get('value')

        #Initialize index to compare with position of dashes in frontend
        index = 0
        indexes = ''

        #iterate through word to find letters that match the guess
        for letter in word:
            index += 1
            if letter == guess.lower():
                indexes += str(index) + ','
            else:
                continue

        #If match, return index of letter in word
        if indexes != '':
            return indexes
        else:
            return 'no match'

    return 'ok'


@app.route('/won', methods=['GET'])
def won():

    #get values from request
    username = request.args.get('username')
    level = request.args.get('level')

    #check if user exists
    user = User.query.filter_by(username=username).first()

    #if exists update score and time last played, else create new user
    if user:
        user.score += int(level)
        user.timestamp = datetime.utcnow()
    else:
        new_user = User(username=username.lower(), score=int(level))
        db.session.add(new_user)

    #commit changes to database
    db.session.commit()

    return 'ok'

#Thanks for looking at my app :)

if __name__ == '__main__':
    app.run(debug=True)
