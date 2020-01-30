#!/usr/bin/python3
"""Minimal flask app"""
import re
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City
from collections import OrderedDict

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.route('/states_list/', strict_slashes=False)
def states_list():
    all_states = storage.all('State')
    return render_template('7-states_list.html', states=all_states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    all_states = storage.all('State')
    return render_template('8-cities_by_states.html', states=all_states)


@app.route('/states', strict_slashes=False)
def states():
    all_states = storage.all('State')
    return render_template('9-states.html', states=all_states, type=0)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id=None):
    x = 0
    all_states = storage.all('State')
    for state_id, state in all_states.items():
        if state.id == id:
            x = state
            return render_template('9-states.html', states_id=x)
    return render_template('9-states.html')


if __name__ == '__main__':
    app.run()