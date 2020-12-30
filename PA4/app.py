from flask import Flask, request, render_template, session, url_for, session, redirect, flash 
from status import Status       # Remember to import status and priority from the provided files
from priority import Priority
import datetime
# task lists

tasklists = {
    1: {
        "name": "Python list",
        "last_updated": "2012-04-23T18:25:43.511Z",
        "created_at": "2012-04-23T18:25:43.511Z",
        "tasks": [
            1,
            2,
            3
        ],
        "tags": ['python', 'programming', 'fullstack']
        },
    2: {
        "name": "Home list",
        "last_updated": "2012-04-23T18:25:43.511Z",
        "created_at": "2012-04-23T18:25:43.511Z",
        "tasks": [
            4,
            5
        ],
        "tags": ['python', 'programming', 'fullstack']
    }
}

# tasks

tasks = {
    1: {
        "name": "learn flask blueprints",
        "last_updated": "2020-04-23T18:25:43.511Z",
        "created_at": "2020-04-23T18:25:43.511Z",
        "status": Status.DONE,
        "priority": Priority.HIGH,
        "description": "Etiam sit amet massa nec urna hendrerit gravida et sed ipsum."
    },
    2: {
        "name": "learn Python enums",
        "last_updated": "2012-04-20T18:25:43.511Z",
        "created_at": "2012-04-20T18:25:43.511Z",
        "status": Status.IN_PROGRESS,
        "priority": Priority.MEDIUM,
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

    },
    3:  {
        "name": "revise OOP concepts",
        "last_updated": "2020-04-25T18:25:43.511Z",
        "created_at": "2020-04-25T18:25:43.511Z",
        "status": Status.DONE,
        "priority": Priority.HIGH,
        "description": "Ut eget elit interdum neque faucibus viverra."
    },
    4:  {
        "name": "clean keyboard",
        "last_updated": "2020-04-25T18:25:43.511Z",
        "created_at": "2020-04-25T18:25:43.511Z",
        "status": Status.DONE,
        "priority": Priority.HIGH,
        "description": "Donec fermentum lacus ultrices mauris pretium, sit amet placerat felis dictum."
    },
    5:  {
        "name": "water plants",
        "last_updated": "2020-04-25T18:25:43.511Z",
        "created_at": "2020-04-25T18:25:43.511Z",
        "status": Status.DONE,
        "priority": Priority.HIGH,
        "description": "Nam imperdiet ligula quis ligula rhoncus, et vehicula sem consectetur."
    }
}
myapp = Flask(__name__)

@myapp.route("/")
def index():
    return render_template("home.html",tasklists=tasklists)


def get_task_name(task):
    return tasks[task]["name"]

myapp.jinja_env.globals.update(get_task_name=get_task_name) #to allow jinja to use python function 

@myapp.route('/edit/<int:index>', methods=['GET','POST'])
def edit(index):
    if request.method == 'GET':
        view_task = tasklists[index]
        return render_template('edit.html', task = view_task ,index=index,taskname=view_task["name"])
    else:
        new_task = request.form['taskname']
        tasklists[index].update({'name':new_task})
        tasklists[index].update({'last_updated':datetime.datetime.now()})
        

        return redirect(url_for('index'))

@myapp.route('/creat_task_list/', methods=['GET','POST'])
def creat_task_list():
    new_key =max(tasklists.keys())+1
    if request.method == 'GET':
        return render_template('creat_task_list.html', key = new_key )
    else:
        tasklists[new_key]={"name": request.form['taskname'],
                    "last_updated": datetime.datetime.now(),
                      "created_at": datetime.datetime.now(),
                           "tasks": [],
                            "tags": []

        }
            

        return redirect(url_for('index'))

@myapp.route('/delete/<int:index>')
def delete(index):
    tasklists.pop(index)
    return redirect(url_for('index'))

@myapp.route("/tasks")
def mytasks():
    return render_template("tasks.html",tasks=tasks)

@myapp.route('/creat_task/', methods=['GET','POST'])
def creat_task():
    new_key =max(tasks.keys())+1
    if request.method == 'GET':
        statuses1={Status.DONE:"DONE",Status.IN_PROGRESS:"IN_PROGRESS",Status.NEW:"NEW"}
        Prioritis={Priority.LOW:"LOW",Priority.MEDIUM:'MEDIUM',Priority.HIGH:'HIGH'}
        return render_template('creat_task.html', key = new_key ,statuses=statuses1 ,Prioritis=Prioritis)
    else:
        tasks[new_key]={"name": request.form['taskname'],
                    "last_updated": datetime.datetime.now(),
                      "created_at": datetime.datetime.now(),
                          "status": request.form['status'],
                        "priority": request.form['priority'],
                     "description": request.form['description']
        }
            

        return redirect(url_for('mytasks'))

@myapp.route('/edit_task/<int:index>', methods=['GET','POST'])
def edit_task(index):
    if request.method == 'GET':
        view_task = tasks[index]
        statuses1={Status.DONE:"DONE",Status.IN_PROGRESS:"IN_PROGRESS",Status.NEW:"NEW"}
        Prioritis={Priority.LOW:"LOW",Priority.MEDIUM:'MEDIUM',Priority.HIGH:'HIGH'}
        return render_template('edit_task.html', task = view_task ,index=index ,statuses=statuses1 ,Prioritis=Prioritis)
    else:
        tasks[index].update({'name':request.form['taskname']})
        tasks[index].update({'last_updated':datetime.datetime.now()})
        tasks[index].update({'status':request.form['status']})
        tasks[index].update({'priority':request.form['priority']})
        tasks[index].update({'description':request.form['description']})
        

        return redirect(url_for('mytasks'))

@myapp.route('/delete_task/<int:index>')
def delete_task(index):
    tasks.pop(index)
    return redirect(url_for('mytasks'))

@myapp.route('/assign/<int:index>', methods=['GET','POST'])
def assign(index):
    if request.method == 'GET':
        view_task = tasks[index]
        return render_template('assign.html', task = view_task ,index=index ,task_list=tasklists)
    else:
        for list in request.form.getlist("tlist"):
            if index not in tasklists[int(list)]["tasks"]:
               
                tasklists[int(list)]["tasks"].append(int(request.form['task_no']))
            

    return redirect(url_for('mytasks'))
