import time

from flask import render_template, jsonify, redirect, url_for, Blueprint

from app import db
from app.models import BoggleBoard

bp = Blueprint("routes", __name__)


@bp.app_errorhandler(404)
def not_found_error(error):
    return redirect(url_for("routes.index"))


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route("/generate_board", methods=["POST"])
def generate_board():
    board = BoggleBoard()

    db.session.add(board)
    db.session.commit()

    start = time.time()
    words = board.generate_words()
    time_taken = f"{(time.time() - start) * 1000:.4f}"

    return jsonify({"game_id": board.id, "board": board.generate_board(),
                    "words": sorted(words), "time_taken": time_taken}), 200


@bp.route('/join/<game_id>')
def boggle_board(game_id):
    board = BoggleBoard.query.filter_by(id=game_id).first()

    if not board:
        return redirect(url_for("routes.index"))

    start = time.time()
    words = board.generate_words()
    time_taken = f"{(time.time() - start) * 1000:.4f}"

    return render_template("index.html", game_id=board.id, dice=board.generate_board(),
                           words=sorted(words), time_taken=time_taken)
