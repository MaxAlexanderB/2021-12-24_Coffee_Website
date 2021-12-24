from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import os

#------Startup Flask and Flaskbootstrap------#
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

#------Generate coffeecorm with WTForm-------#
class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Location Link on Google-Maps', validators=[DataRequired(), URL(message='Please enter a true URL')])
    opening_time = StringField(label='Opening Time', validators=[DataRequired()])
    closing_time = StringField(label='Closing Time', validators=[DataRequired()])
    cafe_rating = SelectField(label='Coffee Rating', choices=['✘', '☕', '☕☕', '☕☕☕'], validators=[DataRequired()])
    wifi_strength = SelectField(label='Wifi Strength', choices=['✘', '💪', '💪💪', '💪💪💪'],validators=[DataRequired()])
    power_socket = SelectField(label='Power Socket Avalability', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField(label='Submit')


#-------Flask routes-------#
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    #-------Check if the form is correct on submission-------#
    if form.validate_on_submit():
        data = request.form
        #------Tedious way to get data in correct format for comma delim csv file without comma at the end--------#
        dummy_list = []
        data_entry = "\n"
        for item in data:
            print(data[f"{item}"])
            dummy_list.append(data[f"{item}"])
        for i in range(1,len(dummy_list)-1):
            if i < (len(dummy_list)-2):
                data_entry += str(dummy_list[i]) + ","
            elif i == (len(dummy_list)-2):
                data_entry += str(dummy_list[i])
        print(data_entry)
        with open("cafe-data.csv", "a", encoding='utf8') as file:
            file.write(data_entry)
    return render_template('add.html', form=form)



@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
