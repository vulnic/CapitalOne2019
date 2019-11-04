from flask import Flask, render_template, url_for, flash, redirect, request
#from flask_api import FlaskAPI
from forms import RegistrationForm, LoginForm, ApiForm, SearchCategoryForm, QuestionForm
from tables import ClueTable, Clue, CategoryTable, Category, JeopardyBoard, JeopardyTile
from test_api import display_clue, get_categories
import json
import requests
import datetime

app = Flask(__name__)
#api = FlaskAPI(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#-------------------------------------------------------
#
#            STUFF FOR JEOPARDY BOARD
# 
#-------------------------------------------------------


cat_ids = [21, 42, 136, 306, 780]
data_big = [[0]]*5 # initializing 5x5 array for boards

with open('data_for_now.json', 'r') as f:
    l = json.load(f)
    data_big = l 

f.close()

#-------------------------------------------------------
@app.route("/", methods=['GET', 'POST'])
@app.route("/start", methods=['GET', 'POST'])
def start(): #After searching, redirect to list of options
    form = ApiForm()

    if request.method == 'POST':
        cat_name = form.category.data
        #value = form.value_dropdown.data
        print("RAN")
        return redirect(url_for('searchCategory', board=True)) #?
    
    return render_template('start.html', form=form)

#-------------------------------------------------------

@app.route("/searchCategory", methods=['GET', 'POST'])
def searchCategory(): #After searching, redirect to list of options
    form = SearchCategoryForm()
    board = request.args.get('board') #this is a string!!

    if form.validate_on_submit():
        category_name = form.category.data

        if board == 'True':
            return redirect(url_for('chooseCategoryBoard', cat_name = category_name)) 
        elif board == 'False':
            return redirect(url_for('chooseCategory', cat_name = category_name))
    
    return render_template('searchCategories.html', form=form)

#-------------------------------------------------------

@app.route("/chooseCategory",methods=['GET', 'POST'])
def chooseCategory():
    cat_name = request.args.get('cat_name')
    form = ApiForm()
    cat_list = []

    #make a table for the category entered
    with open('categories.json', 'r') as f:
        all_categories = json.load(f)
        for item in all_categories:
            if item['title'] and cat_name in item['title']:
                cat_list.append(item)
        
    return render_template('chooseCategory.html', form=form, cat_list=cat_list) 


#-------------------------------------------------------


@app.route("/chooseCategoryBoard",methods=['GET', 'POST'])
def chooseCategoryBoard():
    cat_name = request.args.get('cat_name')
    form = ApiForm()
    cat_list = []

    keys = list(request.form.keys())
    allCatTableItems = []
    tableCat = []

    #print(keys)

    #make a table for the category entered
    with open('categories.json', 'r') as f:
        all_categories = json.load(f)
        for item in all_categories:
            if item['title'] and cat_name in item['title']:
                cat_list.append(item)

    if form.validate_on_submit:
        cat_id = 123 #number obatined from clicking the table

        for item in cat_list: # find the dictionary for the category inputed
            if item['id'] and id == item['id']:
                tableCat.append(item)
                break

        for item in cat_list:
            allCatTableItems.append(Category(item['title'],item['clues_count']))
        
        table = CategoryTable(allCatTableItems) 
        
    return render_template('chooseCategoryBoard.html', table = table, form=form, cat_list=cat_list) 

#-------------------------------------------------------

@app.route("/question",methods=['GET', 'POST'])
def question():
    cat_id = request.args.get('cat_id')
    form = QuestionForm()
    clues = display_clue(cat_id)
    filtered_clues = clues

    if form.validate_on_submit():
        value = form.value_dropdown.data
        filtered_clues = []

        for clue in clues:
            print(type(clue['value']),type(value))
            if clue['value'] == int(value):
                filtered_clues.append(clue)

        if len(filtered_clues) == 0:
            flash("No clues of value: " + value,'danger')

    return render_template('question.html',clues=filtered_clues, form=form)

#-------------------------------------------------------

@app.route("/jeopardy", methods=['GET', 'POST'])
def jeopardy():
    form = ApiForm()
    question = ""
    answer = ""

    jeopardy_data = data_big

    if request.method == 'POST':

        keys = list(request.form.keys()) # which button was pressed

        if(len(keys) > 0):
            which_button = keys[len(keys) - 1]
            #print("submit button name: " + request.form['submit_button'])
            row = int(which_button[7])
            col = int(which_button[9])

            print(which_button, jeopardy_data[row][col])

            question = jeopardy_data[row][col]['question']
            answer = jeopardy_data[row][col]['answer']

            flash("Question: " + question,"danger")
            flash("Answer: " + answer,"success")


    return render_template("jeopardy.html", form=form, question=question, answer=answer) #table=table

#-------------------------------------------------------

@app.route("/lookup", methods=['GET', 'POST'])
def lookup():
    form = ApiForm()
    if form.validate_on_submit:
        num_cat = form.count.data

        data = get_categories(num_cat) #list of dicts
        tableItems = []
        
        for cat in data:
            tableItems.append(Category(cat['title'],cat['clues_count'])) 

        table = CategoryTable(tableItems)

    return render_template('lookup.html', title='Lookup ', table=table, form=form)


#-------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
