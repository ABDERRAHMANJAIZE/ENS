

from flask import abort, jsonify, request
from flask import Flask, flash
import json ,os
from itertools import permutations
import numpy as np
import math
import ast


def dist_robot_task(rb_x, rb_y, task_x, task_y):
    return math.sqrt((rb_x - task_x)**2 + (rb_y - task_y)**2)


def dist_between_tasks(task_x1, task_y1, task_x2, task_y2):
    return math.sqrt((task_x1 - task_x2)**2 + (task_y1 - task_y2)**2)


def abs_robot_task(rb_x, rb_y, task_x, task_y):
    return abs(rb_x - task_x) + abs(rb_y - task_y)


def abs_between_tasks(task_x1, task_y1, task_x2, task_y2):
    return abs(task_x1 - task_x2) + abs(task_y1 - task_y2)


def main(rb1_x,rb1_y,rb2_x,rb2_y,listOfTask):
    data = {}
    numberOfTasks = len(listOfTask)

    allPossibilities = []

    for p in permutations(listOfTask):
        # print(p)
        allPossibilities.append(p)

    #print(allPossibilities)

    Possibilities = np.array(allPossibilities)


    #print(Possibilities)

    firstPosib = 1
    minR1Tasks = []
    minR2Tasks = []
    # parcourir les lignes
    for i in Possibilities:
        # pour avoir le nombre de tache a chaque iteration
        # print(i)
        for j in range(numberOfTasks):
            sumR1 = 0  # distance de r1
            sumR2 = 0  # distance de r2
            i1 = 0  # compteur de r1
            i2 = 0  # compteur de r2
            r1Tasks = []  # tableaux des tasks de r1
            r2Tasks = []  # tableaux des tasks de r2
            # pour manipuler le groupe de r1 a chaque
            for R1i in range(j, numberOfTasks):
                if i1 == 0:
                    sumR1 += abs_robot_task(rb1_x, rb1_y, i[R1i][0], i[R1i][1])
                    i1 += 1
                else:
                    sumR1 += abs_between_tasks(i[R1i-1][0],
                                            i[R1i-1][1], i[R1i][0], i[R1i][1])
                r1Tasks.append(i[R1i])
            #print("la distances de r1 est : {}".format(sumR1))
            # pour manipuler le groupe de r2 a chaque
            for R2i in range(0, j):
                if i2 == 0:
                    sumR2 += abs_robot_task(rb2_x, rb2_y, i[R2i][0], i[R2i][1])
                    i2 += 1
                else:
                    sumR2 += abs_between_tasks(i[R2i-1][0],
                                            i[R2i-1][1], i[R2i][0], i[R2i][1])
                r2Tasks.append(i[R2i])
            #print("la distances de r2 est : {}".format(sumR2))
            if firstPosib == 1:
                minSum = max(sumR1, sumR2)
                minR1Tasks = r1Tasks
                minR2Tasks = r2Tasks
                firstPosib += 1

            elif max(sumR1, sumR2) < minSum:
                minSum = max(sumR1, sumR2)
                minR1Tasks = r1Tasks
                minR2Tasks = r2Tasks

    rr1 = []
    for it in minR1Tasks:
        rr1.append(it.tolist())

    rr2 = []
    for it2 in minR1Tasks:
        rr2.append(it2.tolist())

    data['r1'] = rr1
    data['r2'] = rr2

    #print("tasks for R1 : {}".format(minR1Tasks))
    #print("tasks for R2 : {}".format(minR2Tasks))
    json_data = json.dumps(data)
    return json_data

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        rb1x = int(request.form['rb1x'])
        rb1y = int(request.form['rb1y'])
        rb2x = int(request.form['rb2x'])
        rb2y = int(request.form['rb2y'])
        lst1 = request.form['list']

        #new = "['3, 2', '3, 3', '4, 1', '2, 1','2, 1']"
        ll = ast.literal_eval(lst1)
        test_list = ll
        #list1 = [(3, 2), (3, 3), (4, 1), (2, 1), (2, 1)]
        res = [tuple(map(int, sub.split(', '))) for sub in test_list]
        #print(res)

        try:
            return main(rb1x,rb1y,rb2x,rb2y,res)
            #main(0,0,1,1,res)
        except Exception as e:
            print(e)

        return "process is finished"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)






