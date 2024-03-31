# One time you'll need to install the streamlit package:
#
#     python -m pip install streamlit
#
# And make sure this file is in the same directory as a `payoffs.csv` file with
# the payoffs from city to city. Then run the streamlit server:
#
#    streamlit run railbaron.py
#
# And then open http://localhost:8501/.
import csv
from random import random

from streamlit import button, selectbox, session_state, write

# This program is run top-to-bottom in two cases:
# 
# 1. When the page loads 2. After every interaction (i.e. button click, change
# of selectbox, etc.)
# 
# So it will run just like you read it, top-to-bottom. We'll start by writing a
# heading:
write('# Rail Baron helper')


write('## Current roll')

# The button() function returns true if it was clicked, so `if button():` will
# only be true on re-runs immediately after a click.
if button('Roll dice'):
    session_state['roll'] = int(random() * 7), int(random() * 7), int(random() * 7)

# The `session_state` keeps it's value between re-runs. So it's empty on first
# page load (first run), and then after every interaction, it has the same
# values from the previous run, so it's a way of keeping data between runs.
if 'roll' not in session_state:
    write('Click the button above to roll the dice!')
else:
    dice = session_state['roll']
    write(f'The current dice roll is {dice[0]}, {dice[1]}, and {dice[2]}')


write('## Payoff calculator')

# read_payoffs() returns a mapping for each city for the payoff from that city
# to every other one. So, for example:
#
#     payoffs['Albany'] -> {
#         'Albany': 0,
#         'Atlanta': 23,
#         ...
#     }
#     payoffs['Atlanta'] -> {
#         'Albany': 23,
#         'Atlanta': 0,
#         ...
#     }
def read_payoffs():
    cities = []
    payoffs = {}
    with open('payoffs.csv') as input:
        for row in csv.reader(input):
            # First row just has the list of cities.
            if row[0] == '':
                cities = row[1:]
                continue
            payoffs[row[0]] = {cities[i]: payoff for i, payoff in enumerate(row[1:])}
    return payoffs

if 'payoffs' not in session_state:
    session_state['payoffs'] = read_payoffs()
cities = sorted(session_state['payoffs'].keys())

from_city = selectbox(label="Payoff from city...", options=cities)
to_city = selectbox(label='To city...', options=cities)

payoff = session_state['payoffs'][from_city][to_city]
write(f'Payoff is: **{payoff}**')
