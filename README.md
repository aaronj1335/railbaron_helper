# Rail Baron helper

## One time setup

This project uses http://streamlit.io for displaying the information, so you'll
need to install that in your Python environment.

```shell
pip install streamlit
```

## Running the app

```shell
streamlit run railbaron/railbaron.py
```

And then open http://localhost:8501/ in a web browser.

## More info

### Streamlit execution model

Each time you load the webpage, the `railbaron/railbaron.py` file will run in
the Python interpreter.

Calls to `write('some string')` will display "some string". The formatting uses
something called [Markdown](https://www.markdownguide.org/getting-started/). If
you want to show a heading that (larger text, more space around it), you can add
a leading hashmark, i.e. `write('# My Heading')`. If you want to make something
bold, you can surround it in asterisks, i.e. `write('make it *bold*')`. If you'd
like to use even more formatting, you can use HTML, but you need to specify a
special parameter to disable extra security features, like this:

```
from streamlit import write

write('<span style="color: red">This text will be red</span>',
      unsafe_allow_html=True)
```

Calls to elements like `button()` and `selectbox()` will display the button or
checkbox.  `selectbox()` will return the first item in its list.

### Interacting with the app

When you interact with the page (click a button, select an item from a select
box, etc), the `railbaron/railbaron.py` will run top-to-bottom again, however
some things will be different. For example the `button()` function will return
true, and instead of `selectbox()` returning the default, it'll return the
latest selection.

You can use the return value of the interaction components to decide what to
display. For example, imagine an app where the user selects the current action
(roll dice, calculate payoff, etc). We want the user to select their action,
then show the right thing. First add a "radio" selection (i.e. 2 buttons and you
have to select one):

```
from streamlit import radio, write

current_action = radio('Current action', ['Roll dice', 'Calculate payoff'])

if current_action == 'Roll dice':
    write('## Roll dice')
    # Show input to roll dice, etc.
elif current_action == 'Calculate payoff':
    write('## Calculate payoff')
    from_city = selectbox(...)
    to_city = selectbox(...)
```

### Saving data between re-runs

You may need to save data between interactions (which re-run the script). You
do so by creating the data in a function, and adding `@cache_data` above the
function (a Python "decorator"). A common example of this might be reading a
file:

```
from streamlit import cache_data

@cache_data
def read_payoff_data():
    data = # ... read information from a file ...
    return data

payoff_data = read_payoff_data()
```

This way, when the user interacts with the page, Streamlit will re-run the file,
but because `read_payoff_data()` is decorated with `@cache_data`, it will not
actually re-run the function body.

Streamlit will only re-run a `@cache_data` function if the function's arguments
change. Since `read_payoff_data()` has no arguments, it will only ever read the
file once.

### Session state

Sometimes we need to keep track of things between re-runs. Consider an interface
where we have a button to roll the dice, and show the user what was rolled.
Remember `button()` returns true on a re-run if the user just clicked it:

```
from streamlit import button, write

current_roll = None
if button('Roll dice'):
    current_roll = roll_dice()

# current_roll starts as None, so in this case the user didn't click the button.
if current_roll is None:
    write('Click the button above to roll dice.')

# If the user did click the button, we'd have set the current_roll variable, so
# we get here:
else:
    write(f'Last dice roll: {current_roll}')
```

But since we re-run the entire file for _any_ interaction, we need a way to
store the previous result. We can do this by simply replacing the `current_roll`
variable with `session_state['current_roll']`:

```
from streamlit import button, session_state, write

if button('Roll dice'):
    session_state['current_roll'] = roll_dice()

if 'current_roll' not in session_state:
    write('Click the button above to roll dice.')
else:
    write(f'Last dice roll: {session_state[current_roll]}')
```

### Full Streamlit docs

Streamlit documentation can be found at https://docs.streamlit.io.