from flask import Flask
from airium import Airium
from pathlib import Path
from colorama import Fore
from gbwog.website.Utils import clear_screen, games
import os
import json

app = Flask(__name__)
app.env = "development"
app.debug = True
home_dir = f"{Path.home()}"
SCORES_FILE_NAME = Path(f"{home_dir}/wog/score.json")


def start_flask():
    print(f"{Fore.LIGHTYELLOW_EX}To access score site, enter web on http://127.0.0.1:5000/scores {Fore.LIGHTRED_EX}")

    @app.route('/scores')
    def present_scores():
        file_path = os.path.dirname(__file__)
        if file_path != "":
            os.chdir(file_path)
        page = Airium()
        try:
            with open(f"{SCORES_FILE_NAME}", "r") as file:
                scores = json.loads(file.read())
        except Exception as excep:
            scores = f"Exception: {excep}"
        page('<!DOCTYPE html>')
        with page.html():
            with page.head():
                page.meta(charset="utf-8")
                page.title(_t="Games Score")
                with page.body():
                    for game in games:
                        game_name = games[game]
                        if not scores.__contains__("Exception"):
                            game_score = scores['games'][game_name]
                        else:
                            game_score = "FileNotLoaded"
                        with page.h1(id=f"{game_name}_scores", klass='main_header'):
                            page(f"{game_name} scores: ")
                            if str(game_score).isdigit():
                                with page.div(id="scores"):
                                    page(game_score)
                            else:
                                with page.div(id="scores", style="color:red"):
                                    page(scores)
                    with page.button(onClick="window.location.reload();"):
                        page("Refresh scores")
        html = str(page)
        return html

    app.run(use_reloader=False)


clear_screen()
start_flask()
