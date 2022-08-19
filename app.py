from flask import Flask, render_template, redirect, url_for, request, g,json,session
from functions import validate,listfiles,deletefile
import docker,os
from werkzeug.utils import secure_filename

client = docker.from_env()

app = Flask(__name__)
app.secret_key = "!T?..KdPcnmh$xE5!(8-SS:N(=[dytdmh*Z9?H/.Aijz]?KN]2n[/cU_.cCYK5Bv"
app.config['UPLOAD_FOLDER']='uploads/'
app.config['MAX_CONTENT_PATH']=16 * 1024 * 1024

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion==False:
            error = 'Invalid Credentials. Please try again.'
        else:
            messages = json.dumps({"user":username})
            session['messages'] = messages
            return redirect(url_for('container'))
    return render_template('login.html', error=error)

@app.route('/container', methods=['GET'])
def container():
    containerslist=client.containers.list(all)
    return render_template('containers.html', containerslist=containerslist)

@app.route('/container/<id>', methods = ['GET','POST'])
def startcntr(id):
    if request.method=='GET':
        dict = client.api.inspect_container(id)
        ip = dict['NetworkSettings']['IPAddress']
        if ip == '':
            ip = "Not Online"
        return render_template('containerip.html', ip=ip)

    if request.method=='POST':
        cntr=client.containers.get(id)
        cntr.remove(force=True)
        return redirect(url_for('container'))   
    

@app.route('/files', methods=['GET', 'POST'])
def files():
    if request.method == 'GET':
        filelist=listfiles()

        return render_template('files.html', filelist=filelist)
    
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))) 
        return redirect(url_for('files'))   

@app.route('/file/<name>', methods=['GET', 'POST'])
def delfile(name):
    deletefile(name)
    return redirect(url_for('files')) 


@app.route('/program', methods=['GET'])
def program():
    programlist=client.images.list()
    return render_template('programs.html', programlist=programlist)

@app.route('/program/<tag>', methods=['GET'])
def startprogram(tag):
    name=tag.split(':')[0][2:]
    path=os.path.abspath('uploads/')
    mounts=[path+':/mnt/vol1']
    container = client.containers.run(name,detach=True,volumes=mounts)
    return redirect(url_for('container'))


if __name__ == '__main__':
    app.run(debug=True)