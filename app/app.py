import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import PyPDF2
import re
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from flask_mail import Mail, Message

path = os.getcwd()

UPLOAD_FOLDER = os.path.join(path, 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'aathiraprcse2019@thejusengg.com'
app.config['MAIL_PASSWORD'] = 'thejusnewacc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)


database={'aathira':'123','abhirami':'ari','amal':'amallu','jewelna':'jo'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_email(email_content):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    email_pattern_compile = re.compile(pattern)
    email_extracted_result = email_pattern_compile.search(email_content)
    email_extracted = email_extracted_result.group()
<<<<<<< HEAD
=======

>>>>>>> origin
    return email_extracted

@app.route('/')
def hello_world():
<<<<<<< HEAD
    return render_template("home.html")
=======
    return render_template("login.html")

@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
	    return render_template('login.html',info='Invalid User')
    else:
        if database[name1]!=pwd:
            return render_template('login.html',info='Invalid Password', username=name1)
        else:
	         return render_template('index.html',name=name1)
        
@app.route('/index')     
def index():
    return render_template('base.html', messages=messages)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title': title, 'content': content})
            return redirect(url_for('index'))

    return render_template('create.html')
>>>>>>> origin

@app.route('/file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
    
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('screening', name=filename))
    return render_template("screening.html")

@app.route('/screening/<name>', methods=['GET', 'POST'])
def screening(name):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            pdfFileObj = open('uploads/{}'.format(filename), 'rb')
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            num_pages = len(pdfReader.pages)
            count = 0
            text = ""
            while count < num_pages:
                pageObj = pdfReader.pages[count]
                count += 1
                text += pageObj.extract_text()

                extracted_email = extract_email(text)
                print(extracted_email)

            def cleanResume(resumeText):
                resumeText = re.sub('http\S+\s*', ' ', resumeText)
                resumeText = re.sub('RT|cc', ' ', resumeText)
                resumeText = re.sub('#\S+', '', resumeText) 
                resumeText = re.sub('@\S+', '  ', resumeText)
                resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ',
                                    resumeText)
                resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
                resumeText = re.sub('\s+', ' ', resumeText)
                return resumeText.lower()

            text = cleanResume(text)

            bidang = {
                'Project Management': ['administration', 'agile', 'feasibility analysis', 'finance', 'leader', 'leadership',
                                       'management', 'milestones', 'planning', 'project', 'risk management', 'schedule',
                                       'stakeholders', 'teamwork', 'communication', 'organization', 'research',
                                       'public speaking', 'problem solving', 'negotiation', 'team management',
                                       'time management', 'adaptability', 'policy knowledge', 'reporting', 'technical',
                                       'motivation'],

                'Backend': ['flask', 'laravel', 'django', 'ruby on rails', 'express.js', 'codeigniter', 'golang', 'mysql',
                            'postgres', 'mongodb', 'relational database', 'non relational database', 'nosql',
                            'application programming interface', 'object oriented programming'],

                'Frontend': ['react', 'angular', 'vue.js', 'svelte', 'jquery', 'backbone.js ', 'ember.js', 'semantic-ui',
                             'html', 'css', 'bootstrap', 'javascript', 'jquery', 'xml', 'dom manipulation', 'json'],

                'Data Science': ['math', 'statistic', 'probability', 'preprocessing', 'machine learning',
                                 'data visualization',
                                 'python', 'r programming', 'tableau', 'natural language processing', 'data modeling',
                                 'big data', 'deep learning', 'relational database management', 'clustering', 'data mining',
                                 'text mining', 'jupyter', 'neural networks', 'deep neural network', 'pandas', 'scipy',
                                 'matplotlib', 'numpy', 'tensorflow', 'scikit learn', 'data analysis', 'data privacy',
                                 'enterprise resource planning', 'oracle', 'sybase', 'decision making', 'microsoft excel',
                                 'data collection', 'data cleaning', 'pattern recognition', 'google analytics'],

                'Devops': ['networking', 'tcp' 'udp', 'microsoft azure', 'amazon web services', 'alibaba cloud',
                           'google cloud',
                           'docker', 'kubernetes', 'virtual machine', 'cloud computing', 'security', 'linux', 'ubuntu',
                           'debian', 'arch linux', 'kali linux', 'automation', 'containers', 'operations', 'security',
                           'testing', 'troubleshooting']
            }

            project = 0
            backend = 0
            frontend = 0
            data = 0
            devops = 0

            project_list = []
            backend_list = []
            frontend_list = []
            data_list = []
            devops_list = []

            scores = []

            for area in bidang.keys():
                if area == 'Project Management':
                    for word_project in bidang['Project Management']:
                        if word_project in text:
                            project += 1
                            project_list.append(word_project)
                    scores.append(project)

                elif area == 'Backend':
                    for word_backend in bidang['Backend']:
                        if word_backend in text:
                            backend += 1
                            backend_list.append(word_backend)
                    scores.append(backend)

                elif area == 'Frontend':
                    for word_frontend in bidang['Frontend']:
                        if word_frontend in text:
                            frontend += 1
                            frontend_list.append(word_frontend)
                    scores.append(frontend)

                elif area == 'Data Science':
                    for word_data in bidang['Data Science']:
                        if word_data in text:
                            data += 1
                            data_list.append(word_data)
                    scores.append(data)

                elif area == 'Devops':
                    for word_devops in bidang['Devops']:
                        if word_devops in text:
                            devops += 1
                            devops_list.append(word_devops)
                    scores.append(devops)

            data_all_list = {'Project Management': project_list, 'Backend': backend_list, 'Frontend': frontend_list,
                             'Data Science': data_list, 'DevOps': devops_list}

            summary = pd.DataFrame(scores, index=bidang.keys(), columns=['score']).sort_values(by='score', ascending=False).loc[
                lambda df: df['score'] > 0]

            fig, ax = plt.subplots(figsize=(10, 10))
            ax.pie(summary['score'], labels=summary.index, autopct='%1.1f%%', startangle=90, shadow=True)
            ax.set_aspect('equal')
            ax.set_title("Scores")
            buf = BytesIO()
            ax.figure.savefig(buf, format="png")
            data = base64.b64encode(buf.getbuffer()).decode("ascii")

        if summary['score']['Project Management'] > 1:
            subject="Congratulations!"
            msg = Message(subject, sender="aathiraprcse2019@thejusengg.com", recipients=[extracted_email])
            msg.body = "Hi, \n\t Heres you technical test link below: \n https://forms.gle/HBoYroSjY2CT84o26 "
            mail.send(msg)

    else:
        pdfFileObj = open('uploads/{}'.format(name), 'rb')
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
        num_pages = len(pdfReader.pages)
        count = 0
        text = ""
        while count < num_pages:
            pageObj = pdfReader.pages[count]
            count += 1
            text += pageObj.extract_text()

        def cleanResume(resumeText):
            resumeText = re.sub('http\S+\s*', ' ', resumeText)
            resumeText = re.sub('RT|cc', ' ', resumeText) 
            resumeText = re.sub('#\S+', '', resumeText) 
            resumeText = re.sub('@\S+', '  ', resumeText)
            resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ',
                                resumeText)
            resumeText = re.sub(r'[^\x00-\x7f]', r' ', resumeText)
            resumeText = re.sub('\s+', ' ', resumeText) 
            return resumeText.lower()
        
        extracted_email = extract_email(text)
        print(extracted_email)

        text = cleanResume(text)

        bidang = {
            'Project Management': ['administration', 'agile', 'feasibility analysis', 'finance', 'leader', 'leadership',
                                   'management', 'milestones', 'planning', 'project', 'risk management', 'schedule',
                                   'stakeholders', 'teamwork', 'communication', 'organization', 'research',
                                   'public speaking', 'problem solving', 'negotiation', 'team management',
                                   'time management', 'adaptability', 'policy knowledge', 'reporting', 'technical',
                                   'motivation'],

            'Backend': ['flask', 'laravel', 'django', 'ruby on rails', 'express.js', 'codeigniter', 'golang', 'mysql',
                        'postgres', 'mongodb', 'relational database', 'non relational database', 'nosql',
                        'application programming interface', 'object oriented programming'],

            'Frontend': ['react', 'angular', 'vue.js', 'svelte', 'jquery', 'backbone.js ', 'ember.js', 'semantic-ui',
                         'html', 'css', 'bootstrap', 'javascript', 'jquery', 'xml', 'dom manipulation', 'json'],

            'Data Science': ['math', 'statistic', 'probability', 'preprocessing', 'machine learning', 'data visualization',
                             'python', 'r programming', 'tableau', 'natural language processing', 'data modeling',
                             'big data', 'deep learning', 'relational database management', 'clustering', 'data mining',
                             'text mining', 'jupyter', 'neural networks', 'deep neural network', 'pandas', 'scipy',
                             'matplotlib', 'numpy', 'tensorflow', 'scikit learn', 'data analysis', 'data privacy',
                             'enterprise resource planning', 'oracle', 'sybase', 'decision making', 'microsoft excel',
                             'data collection', 'data cleaning', 'pattern recognition', 'google analytics'],

            'Devops': ['networking', 'tcp' 'udp', 'microsoft azure', 'amazon web services', 'alibaba cloud', 'google cloud',
                       'docker', 'kubernetes', 'virtual machine', 'cloud computing', 'security', 'linux', 'ubuntu',
                       'debian', 'arch linux', 'kali linux', 'automation', 'containers', 'operations', 'security',
                       'testing', 'troubleshooting']
        }

        project = 0
        backend = 0
        frontend = 0
        data = 0
        devops = 0

        project_list = []
        backend_list = []
        frontend_list = []
        data_list = []
        devops_list = []

        scores = []

        for area in bidang.keys():
            if area == 'Project Management':
                for word_project in bidang['Project Management']:
                    if word_project in text:
                        project += 1
                        project_list.append(word_project)
                scores.append(project)

            elif area == 'Backend':
                for word_backend in bidang['Backend']:
                    if word_backend in text:
                        backend += 1
                        backend_list.append(word_backend)
                scores.append(backend)

            elif area == 'Frontend':
                for word_frontend in bidang['Frontend']:
                    if word_frontend in text:
                        frontend += 1
                        frontend_list.append(word_frontend)
                scores.append(frontend)

            elif area == 'Data Science':
                for word_data in bidang['Data Science']:
                    if word_data in text:
                        data += 1
                        data_list.append(word_data)
                scores.append(data)

            elif area == 'Devops':
                for word_devops in bidang['Devops']:
                    if word_devops in text:
                        devops += 1
                        devops_list.append(word_devops)
                scores.append(devops)

        data_all_list = {'Project Management': project_list, 'Backend': backend_list, 'Frontend': frontend_list,
                         'Data Science': data_list, 'DevOps': devops_list}

        summary = pd.DataFrame(scores, index=bidang.keys(), columns=['score']).sort_values(by='score', ascending=False).loc[
            lambda df: df['score'] > 0]

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.pie(summary['score'], labels=summary.index, autopct='%1.1f%%', startangle=90, shadow=True)
        ax.set_aspect('equal')
        ax.set_title("Scores")
        buf = BytesIO()
        ax.figure.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        if summary['score']['Project Management'] > 0:
            subject="Congratulations!"
            msg = Message(subject, sender="aathiraprcse2019@thejusengg.com", recipients=[extracted_email])
            msg.body = "Hi, \n\t Heres you technical test link below: \n https://forms.gle/HBoYroSjY2CT84o26 "
            mail.send(msg)
        

    return render_template('screening.html', data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)