from flask import Flask,request
import spacy
from flask_ngrok import run_with_ngrok
import sys,fitz
# Create a Flask app instance
app = Flask(__name__)
run_with_ngrok(app)

# Define a route and a view function
@app.route('/')
def hello_world():
    return 'Hello, World! This is my Flask app.'

@app.route('/resume_parse',methods=['GET'])
def resume_parse():

    resume_path=request.args.get('path','')
    compelete_path = './Document/'+resume_path
    
    doc = fitz.open(compelete_path)

    text = ''
    for page in doc:
        text = text + str(page.get_text())
    text= text.strip()
    text= ' '.join(text.split())

    nlp = spacy.load('./content/output/model-best')

    doc = nlp(text)

    lst =[]
    for ent in doc.ents:
        print(ent.text ,"------>", ent.label_)
        lst.append((ent.text,ent.label_))

    return {"data":lst}    

        

# Run the app if this script is executed directly
if __name__ == '__main__':
    app.run()