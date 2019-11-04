from flask_table import Table, Col, create_table

class ClueTable(Table):
    question = Col('Question')
    answer = Col('Answer')
    value = Col('Value')
    airdate = Col('Airdate')

class Clue():
    def __init__(self,question,answer,value,airdate):
        self.question = question
        self.answer = answer
        self.value = value
        self.airdate = airdate

class CategoryTable(Table):
    classes = ['fl-table']

    title = Col('Title')
    clue_count = Col('Clue Count')

class Category():
    def __init__(self,title,clue_count):
        self.title = title
        self.clue_count = clue_count

class JeopardyBoard(Table):
    jBoard = create_table('JeopardyBoard')
    for i in range(4):
        jBoard.add_column("question" + str(i), Col("Header_" + str(i)))

class JeopardyTile(Table):
    def __init__(self,question1,question2,question3,question4,question5):
        self.question1 = question1
        self.question2 = question2
        self.question3 = question3
        self.question4 = question4
        self.question5 = question5
        

    