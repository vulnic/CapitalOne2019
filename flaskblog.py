from flask import Flask, render_template, url_for, flash, redirect, request
#from flask_api import FlaskAPI
from forms import RegistrationForm, LoginForm, ApiForm
from tables import ClueTable, Clue, CategoryTable, Category, JeopardyBoard, JeopardyTile
from test_api import display_clue, get_categories
import json
import requests

app = Flask(__name__)
#api = FlaskAPI(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]
#-------------------------------------------------------
#
#            STUFF FOR JEOPARDY BOARD
# 
#-------------------------------------------------------


cat_ids = [21, 42, 136, 306, 780]
data = [[0]]*5 # initializing 5x5 array for boards

output = []
""" 
for i in range(5):
    output = []
    for a in range(5):
        # i => value
        # a => category
        all_clues = display_clue((i+1)*100,cat_ids[a])
        output += all_clues

        #print(len(all_clues))
         #list of dicts 

    data[i] = output
    #with open('data_for_now_' + str(i) + '.json', 'w') as f:
    #        json.dump(data,f)
    #f.close()

    

with open('data_for_now.json', 'w') as f:
    json.dump(data,f)

tableItems = []

for i in range(5):
    tableItems.append(JeopardyTile(data[i][0][0]['question'],data[i][1][0]['question'],\
                                data[i][2][0]['question'],data[i][3][0]['question'],\
                                data[i][4][0]['question']))

table = JeopardyBoard(tableItems) """


with open('data_for_now.json', 'r') as f:
    l = json.load(f)
    data = l 

f.close()



#-------------------------------------------------------

@app.route("/start", methods=['GET', 'POST'])
def start(): #After searching, redirect to list of options
    form = ApiForm()

    if form.validate_on_submit():
        cat_name = form.category.data
        #value = form.value_dropdown.data
        return redirect(url_for('searchCategory')) #?
    
    return render_template('searchCategories.html', form=form)

#-------------------------------------------------------

@app.route("/start/searchCategory", methods=['GET', 'POST'])
def searchCategory(): #After searching, redirect to list of options
    form = ApiForm()
    if form.validate_on_submit():
        cat_name = form.category.data
        #value = form.value_dropdown.data
        return redirect(url_for('chooseCategory')) #pass in cat_name... somehow
    
    return render_template('searchCategories.html', form=form)

@app.route("/chooseCategory")
def chooseCategory():
    form = ApiForm()
    cat_list = []
    cat_name = 'animals'

    if form.validate_on_submit:
        keys = list(request.form.keys())
        allCatTableItems = []
        selectedCat = []

        #make a table for the category entered
        with open('categories.json', 'r') as f:
            all_categories = json.load(f)
            for item in all_categories:
                if item['title'] and cat_name in item['title']:
                    cat_list.append(item)

        for cat in cat_list:
            allCatTableItems.append(Category(cat['title'],cat['clues_count'])) 

        tableAll = CategoryTable(allCatTableItems)

        if form.validate_on_submit:
            cat_id = 123 #number obatined from clicking the table

            for item in cat_list: # find the dictionary for the category inputed
                if item['id'] and id == item['id']:
                    selectedCat.append(item)
                    break

            for item in selectedCat:
                allCatTableItems.append(Category(item['title'],item['clues_count']))
            
            table = CategoryTable(allCatTableItems)
        
    return render_template('chooseCategory.html', table=table, tableAll=tableAll, form=form)

#-------------------------------------------------------

def from_cat_get_data(cat_ids):
    jeopardy_data = [[0]*5]*5

    for i in range(5):
        output = []
        for a in range(5):
            jeopardy_data[i][a] = display_clue((i+1)*100,cat_ids[a])
    return jeopardy_data

@app.route("/jeopardy", methods=['GET', 'POST'])
def jeopardy(cat_ids):
    form = ApiForm()
    question = ""
    answer = ""

    jeopardy_data = from_cat_get_data(cat_ids)

    if form.validate_on_submit:

        keys = list(request.form.keys()) # which button was pressed

        if(len(keys) > 0):
            which_button = keys[len(keys) - 1]
            #print("submit button name: " + request.form['submit_button'])
            row = int(which_button[7])
            col = int(which_button[9])

            print(which_button, data[row][col])

            question = data[row][col]['question']
            answer = data[row][col]['answer']

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

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

#-------------------------------------------------------

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash('Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)
    
#-------------------------------------------------------

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#-------------------------------------------------------

@app.route("/test", methods=['GET', 'POST'])
def test():
    form = ApiForm()
    if form.validate_on_submit():
        user_val = form.value.data
        user_cat = form.category.data

        output = display_clue(user_val=user_val,user_cat=user_cat) 
            
        flash('Question: \"' + output[0]['question'] + '\"','success')
        flash('Answer: \"' + output[0]['answer'] + '\"','danger')

    return render_template("test.html",form=form)

 
#-------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
