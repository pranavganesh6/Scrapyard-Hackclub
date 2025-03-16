from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "supersecretkey"

# List of words for the game
WORDS = ["PYTHON", "FLASK", "DEVELOPER", "HANGMAN", "PROGRAMMING", "OPENAI", "CHALLENGE", "COMPUTERSCIENCE", "CODING", "JAVA", "HTML", "COMPUTERS", "STACKOVERFLOW", "GOOGLE"]

# Function to start a new game
def start_new_game():
    session.clear()  # Reset everything
    session["word"] = random.choice(WORDS)  # Pick a new random word
    session["display_word"] = ["_" if letter.isalpha() else letter for letter in session["word"]]  # Preserve spaces
    session["attempts"] = 6  # Reset attempts
    session["guessed_letters"] = []  # Reset guessed letters

@app.route("/", methods=["GET", "POST"])
def index():
    if "word" not in session:
        start_new_game()  # Ensure a word exists

    word = session["word"]
    display_word = session["display_word"][:]
    guessed_letters = session["guessed_letters"][:]
    attempts = session["attempts"]

    if request.method == "POST":
        guess = request.form.get("guess", "").upper()

        if guess and guess not in guessed_letters and guess.isalpha():
            guessed_letters.append(guess)

            if guess in word:
                for i, letter in enumerate(word):
                    if letter == guess:
                        display_word[i] = guess  # Reveal correct letters
            else:
                attempts -= 1  # Reduce attempts for wrong guess

        # Update session state
        session["display_word"] = display_word
        session["guessed_letters"] = guessed_letters
        session["attempts"] = attempts  # Ensure attempts are saved correctly

    game_over = "_" not in display_word or session["attempts"] <= 0
    message = ""

    if "_" not in display_word:
        message = "🎉 You won! The word was: " + word
    elif session["attempts"] <= 0:
        message = "💀 You lost! The word was: " + word

    return render_template("hangmanindex.html",
                           display_word=" ".join(display_word),
                           attempts=session["attempts"],
                           guessed_letters=session["guessed_letters"],
                           game_over=game_over,
                           message=message)

@app.route("/reset-game", methods=["POST"])
def reset_game():
    """ Resets the game when Play Again is clicked """
    start_new_game()
    return index()

if __name__ == "__main__":
    app.run(debug=True)
