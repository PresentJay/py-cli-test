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


EXCEL_SHEETNAME = {
    "AllergyIntolerance": "table_allergies",
    "Immunization": "table_immunizations",
    "Observation": "table_observations",
    "Procedure": "table_procedures",
    "Medication": "table_medications",
    "Condition": "table_conditions",
    "Encounter": "table_encounters",
    "Patient": "table_patients",
    "CBNU_lifelog": "table_CBNU_lifelog(2)",
    "CBNU_environment": "table_CBNU_environment (2)",
    "Feature": "Tables_features",
}

# CBNU_Data
CNBU_SCHEMA = {
    "AllergyIntolerance": [
        "START",  # 알러지 진단일 : onsetDateTime
        "STOP",  # 알러지 종료일 : lastOccurrence
        "PATIENT",  # 환자 ID : patient
        "ENCOUNTER",  # 의료기관 방문 ID : encounter
        "CODE",  # SNOMED-CT 알러지 코드 : code
        "DESCRIPTION",  # 알러지 기술 : note
    ],
    "Immunization": [
        "DATE",  # 예방접종 이루어진 날짜 :
        "PATIENT",  # 환자 ID :
        "ENCOUNTER",  # 의료기관 방문 ID :
        "CODE",  # CVX 예방접종 코드 :
        "DESCRIPTION",  # 예방접종 기술 :
    ],
    "Observation": [
        "DATE",  # 검사일 : effectiveDateTime
        "PATIENT",  # 환자 ID : identifier
        "ENCOUNTER",  # 의료기관 방문 ID : identifier
        "CODE",  # LOINC 관찰 및 진단검사 코드 : code
        "DESCRIPTION",  # 관찰 및 진단검사 기술 : code
        "VALUE",  # 관찰 및 진단검사 수치 : valueQuantity
        "UNITS",  # 관찰 및 진단검사 단위 : valueQuantity
        "REMARK",  # 비고 : note
    ],
    "Procedure": [
        "PATIENT",  # :
        "ENCOUNTER",  # :
        "CODE",  # :
        "DESCRIPTION",  # :
        "REASONCODE",  # :
        "REASONDESCRIPTION",  # :
        "REMARK",  # :
    ],
    "Medication": [
        "START",  # :
        "STOP",  # :
        "PATIENT",  # :
        "ENCOUNTER",  # :
        "CODE",  # :
        "DESCRIPTION",  # :
        "REASONCODE",  # :
        "REASONDESCRIPTION",  # :
    ],
    "Condition": [
        "START",  # :
        "STOP",  # :
        "PATIENT",  # :
        "ENCOUNTER",  # :
        "CODE",  # :
        "DESCRIPTION",  # :
        "REMARK",  # :
    ],
    "Encounter": [
        "ID",  # 의료기관 방문 ID : identifier
        "DATE",  # 의료기관 방문일 : period - start
        "PATIENT",  # 환자 ID : identifier

        # 200713 14:61 / PresentJay
        # (?) 외래/응급 등 코드는 class에서 등장하는데, SNOMED-CT 코드가 아님
        # 결론 : 주어진 Resource로는 모든 SNOMED-CT 코드를 표현할 수 없음.
        #        따라서 extension - valueCodableConcept를 이용하여 표현

        # SNOMED-CT 의료기관 방문 코드(예, 외래, 응급) : extension - valueCodeableConcept
        "CODE",
        "DESCRIPTION",  # 의료기관 종류 기술 : extension - valueCodeableConcept
        "REASONCODE",  # SNOMED-CT 진단 코드 : extension - valueCodeableConcept
        "REASONDESCRIPTION",  # 진단코드 기술 : extension - valueCodeableConcept
    ],
    "Patient": [
        "ID",  # 환자 ID : identifier
        "BIRTHDATE",  # 생년월일 : birthDate
        "DEATHDATE",  # 사망년월일 : deceasedDateTime
        "Age",  # 만 나이 : extension - valueCodeableConcept
        "Name",  # 성명 : name - text
        "GENDER",  # 성별 : gender
        "ADDRESS",  # 주소 : address
        "Patient_registration_ID",  # 환자등록번호 : identifier
        "SSN",  # 사회보장번호 : identifier
        "DRIVERS",  # 운전면허번호 : identifier
        "PASSPORT",  # 여권 : identifier
        "PREFIX",  # 칭호 : name - prefix
        "FIRST",  # 이름 : name - given
        "LAST",  # 성 : name - family
        "SUFFIX",  # 학위 : name - suffix
        "MAIDEN",  # 결혼전 이름 : name - maiden
        "MARITAL",  # 결혼 여부 : maritalStatus
        "RACE",  # 인종 : extension - valueCodeableConcept
        "ETHNICITY",  # 민족 : extension - valueCodeableConcept
        "BIRTHPLACE",  # 출생지 : extension - valueCodeableConcept
    ],
    "CBNU_lifelog": [
        "Serial_No",  # :
        "DATE_TIME",  # :
        "PATIENT",  # :
        "CODE",  # :
        "DESCRIPTION",  # :
        "VALUE",  # :
        "UNITS",  # :
        "REMARK",  # :
    ],
    "CBNU_environment": [
        "Serial_No",  # :
        "DATE_TIME",  # :
        "PATIENT",  # :
        "CODE",  # :
        "DESCRIPTION",  # :
        "VALUE",  # :
        "UNITS",  # :
    ],
}


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


def log(string, color, font="slant", figlet=False):
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
                Separator("\n * * * * * * * * * \n"),
                'excel-processing',
                Separator("\n * * * * * * * * * \n"),
                'exit'
            ],
            'filter': lambda val: val.lower()
        },
        {
            'type': 'list',
            'name': 'resource_type',
            'message': 'Select FHIR-Resource Type',
            'choices': list(EXCEL_SHEETNAME.keys()),
            'when': lambda answers: getContentType(answers, "create") or getContentType(answers, "search"),
        },
        {
            'type': 'list',
            'name': 'resource_type',
            'message': 'Select FHIR-Resource Type',
            'choices': list(EXCEL_SHEETNAME.values()),
            'when': lambda answers: getContentType(answers, "excel-processing"),
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


def retn_properties(doc):
    nametable = []
    for name in doc:
        nametable.append({'name': name})
    return nametable


def create_question(resource):
    questions = [
        {
            'type': 'checkbox',
            'qmark': '😃',
            'message': 'Select PATIENT Properties',
            'name': 'PATIENT',
            'choices': retn_properties(CNBU_SCHEMA[resource]),
            'validate': lambda answer: 'You must choose at least one topping.'
            if len(answer) == 0 else True
        },
    ]
    answers = prompt(questions, style=style)

    return answers


@click.command()
def main():
    flag = True
    while(flag):
        # clear terminal code
        print(u"{}[2J{}[;H".format(chr(27), chr(27)), end="")

        log("ETRI PYIR", color="blue", figlet=True)
        log("\t\tfhir clients by python.", "green")
        log("\t\t\t-dev PresentJay, 20.07, ETRI", "yellow")
        print("\n")

        pyir = pyir_execute()
        if getContentType(pyir, "create"):
            create_question(pyir["resource_type"])
        elif pyir["exit_confirm"]:
            break


# Execute Main Function
if __name__ == "__main__":
    main()
