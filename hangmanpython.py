from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

# List of words for the game
WORDS = ["PYTHON", "FLASK", "DEVELOPER", "HANGMAN", "PROGRAMMING", "ARTIFICIALINTELIGENCE", "CHALLENGE", "HACKATHON", "HACKCLUB", "JAVA", "JAVASCRIPT", "SCRAPYARD", "COMPUTERSCIENCE", "CODING"]

# Insult Hangman Responses
INSULTS = [
    "I'm losing braincells from your incomprehension.",
    "Are you trying to lose? Because it’s working!",
    "Even a braindead person is better at this.",
    "I’m starting to think you don’t know the alphabet...",
    "Wrong again! You sure you’re not just pressing random keys?",
    "What the f*ck are you doing?",
    "So...there's something called common sense...are you sure you're not lacking any?",
    "Aim for the stars so I can watch you burn in them!",
    "Keep yourself safe. You know what I meant.",
    "Install aimlabs IRL so you know to aim for the right key next time."
]

# Rage Mode Responses
RAGE_MODE = [
    "SERIOUSLY? YOU HAD ONE JOB!",
    "BRO, IT'S NOT THAT HARD!",
    "DO YOU EVEN KNOW THE ALPHABET?!",
    "I CAN'T WATCH THIS ANYMORE!"
]

# Sarcastic Compliments for Correct Guesses
SARCASTIC_COMPLIMENTS = [
    "Finally, your brain started working.",
    "About time you got one right!",
    "I was losing hope... but here we are.",
    "See? You CAN do it!",
    "One small step for you, one giant leap for intelligence."
]

# Function to start a new game
def start_new_game():
    session["word"] = random.choice(WORDS)
    session["display_word"] = ["_" if letter.isalpha() else letter for letter in session["word"]]
    session["attempts"] = 6
    session["guessed_letters"] = []
    session["wrong_streak"] = 0  # Tracks consecutive wrong guesses
    session["message"] = ""

@app.before_request
def ensure_new_game():
    """ Ensures a new game starts if session is empty """
    if "word" not in session:
        start_new_game()

@app.route("/", methods=["GET", "POST"])
def index():
    word = session["word"]
    display_word = session["display_word"]
    guessed_letters = session["guessed_letters"]

    if request.method == "POST":
        guess = request.form.get("guess", "").upper()

        if guess and guess not in guessed_letters and guess.isalpha():
            guessed_letters.append(guess)

            if guess in word:
                for i, letter in enumerate(word):
                    if letter == guess:
                        display_word[i] = guess  # Reveal correct letters
                session["message"] = random.choice(SARCASTIC_COMPLIMENTS)  # Sarcastic compliment
                session["wrong_streak"] = 0  # Reset wrong streak
            else:
                session["attempts"] -= 1  # Wrong guess reduces attempts
                session["wrong_streak"] += 1  # Increase wrong streak

                # Program randomly guesses a letter for the user
                available_letters = [l for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if l not in guessed_letters]
                if available_letters:
                    random_guess = random.choice(available_letters)
                    guessed_letters.append(random_guess)

                    if random_guess in word:
                        for i, letter in enumerate(word):
                            if letter == random_guess:
                                display_word[i] = random_guess  # Reveal correct letters
                        session["message"] = "You're welcome. I guess programs are smarter than you stupid humans."
                    else:
                        session["message"] = "Suck it up, dumbass!"

                # Rage mode if 3 wrong guesses in a row
                if session["wrong_streak"] >= 3:
                    session["message"] = random.choice(RAGE_MODE)
                else:
                    session["message"] = random.choice(INSULTS)  # Regular insult

        # Ensure session data is updated
        session["display_word"] = display_word
        session["guessed_letters"] = guessed_letters

    game_over = "_" not in display_word or session["attempts"] <= 0
    final_message = ""

    if "_" not in display_word:
        final_message = "🎉 You won! The word was: " + word
    elif session["attempts"] <= 0:
        final_message = "💀 You lost! The word was: " + word

    return render_template("hangmanindex.html",
                           display_word=" ".join(display_word),
                           attempts=session["attempts"],
                           guessed_letters=session["guessed_letters"],
                           game_over=game_over,
                           message=session["message"],
                           final_message=final_message)

@app.route("/reset-game", methods=["POST"])  
def reset_game():
    """ Route to manually reset the game """
    session.clear()  
    start_new_game()
    return index()

if __name__ == "__main__":
    app.run(debug=True)
