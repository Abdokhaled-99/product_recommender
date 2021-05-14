import flask
from flask import request, jsonify
import  pandas as pd
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.

original=pd.read_csv('user_rating.csv')

#set first column to index
df = pd.read_csv('result.csv', index_col=0,low_memory=False)
#set columns and index names
df.columns.name = df.index.name
df.index.name = df.index[0]
#remove first row of data
df = df.iloc[1:]



@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/antique/api/user', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    if int(id) not in original['userId']:
        return ('user not found',404)

    w = original[original['userId'] == int(id)]['title'].to_list()
    r = df.loc[id].sort_values(ascending=False).index
    r_filtered = [i for i in r if i not in w][:3]

    return jsonify(r_filtered)
app.run()


