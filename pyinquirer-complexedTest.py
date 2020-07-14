# Command line decorator code
import click
import six
from PyInquirer import (Token, print_json, prompt, style_from_dict, Separator)
from pyfiglet import figlet_format

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None
# # # #


""" Commandline Decorataion Line """

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})


def log(string, color, font="block", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)


def getContentType(answer, conttype):
    return answer.get("content_type").lower() == conttype.lower()


def pyir_execute():

    questions = [
        {
            'type': 'list',
            'name': 'content_type',
            'message': 'MAIN PAGE >> ',
            'choices': [
                'create',
                'search',
                {
                    'name': 'update',
                    'disabled': 'Unavailable yet'
                },
                {
                    'name': 'delete',
                    'disabled': 'Unavailable yet'
                },
                Separator(),
                'excel-processing',
                Separator(),
                'exit'
            ],
            'filter': lambda val: val.lower()
        },
        {
            'type': 'input',
            'name': 'content',
            'message': 'Enter plain text:',
            'when': lambda answers: getContentType(answers, "text"),
        },
        {
            'type': 'confirm',
            'name': 'exit_confirm',
            'message': 'Do you want to exit from ETRI PYIR Client?',
            'when': lambda answers: getContentType(answers, "exit")
        },
    ]

    answers = prompt(questions, style=style)
    return answers


@click.command()
def main():
    flag = True
    while(flag):
        print(u"{}[2J{}[;H".format(chr(27), chr(27)), end="")
        log("ETRI PYIR", color="blue", figlet=True)
        log("fhir clients by python. (dev PresentJay, 20.07)", "green")
        pyir = pyir_execute()

        if pyir.get("exit_confirm"):
            break


# Execute Main Function
if __name__ == "__main__":
    main()
