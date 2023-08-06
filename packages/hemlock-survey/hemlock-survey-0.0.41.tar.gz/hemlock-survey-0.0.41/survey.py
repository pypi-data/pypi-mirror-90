from hemlock import Branch, Page, Label, Input, Compile as C, route
from hemlock.tools import consent_page, completion_page
from hemlock_demographics import demographics
from hemlock_berlin import berlin

@route('/survey')
def start():
    name_input = Input(
        'What is your name?'
    )
    return Branch(
        # consent_page(
        #     'This is a consent form'
        # ),
        # berlin(),
        Page(
            name_input,
            delay_forward=1000
        ),
        Page(
            Label(compile=C.greet(name_input)),
            back=True
        ),
        demographics(
            'age',
            'race',
            'gender',
            page=True
        ),
        completion_page()
    )

@C.register
def greet(greeting, name_input):
    greeting.label = 'Hello, {}'.format(name_input.response)
