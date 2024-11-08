from project.todo import database_bp
from ..db import mysql
from flask import request, jsonify,redirect,url_for,render_template


@database_bp.route("/")
def students_page():
    cur = mysql.connection.cursor()
    cur.execute("select * from studentdata")

    student_data = cur.fetchall()
    cur.close()

    return str(student_data)

@database_bp.route('/new_student')
def new_student_form():
    return render_template('create_student.html')

@database_bp.route('/delete_student')
def delete_student_form():
    return render_template('delete_student.html')

@database_bp.route('/update_student')
def update_student_form():
    return render_template('update_student.html')

@database_bp.route("/", methods=['POST'])
def insert_data():
    if request.is_json:
        data = request.json
        id = data['id']
        username = data['username']
    else :
        id = request.form['id']
        username = request.form['username']

    cur = mysql.connection.cursor()
    cur.execute("insert into studentdata (id, username) values (%s, %s);",
                 (id, username))
    mysql.connection.commit()
    cur.close()

    if request.is_json:
        return jsonify({"message": "Student created successfully"}), 201
    else:
        return redirect(url_for('database_bp.students_page'))
    
@database_bp.route("/delete_student", methods=['POST'])
def delete_entry():
    print("delete function called")
    if request.is_json:
        data = request.json
        id_delete = data['id']

    else :
        id_delete = request.form['id']

    cur = mysql.connection.cursor()
    cur.execute("select username from studentdata where id = %s" , (id_delete))
    
    username_delete = cur.fetchall()

    cur.execute("delete from studentdata where id = %s;",
                (id_delete))
    mysql.connection.commit()
    cur.close()
    print(f"Student name {username_delete} deleted successfully")
    if request.is_json:
        return jsonify({"message": f"Student name {username_delete} deleted successfully"}), 201
    else:
        return redirect(url_for('database_bp.students_page'))
    

@database_bp.route("/update_student", methods=['POST'])
def update_entry():
    print("update fubction called")
    if request.is_json:
        data = request.json
        id_update = data['id']
        old_username = data['id']
        username_update = data.get('username', 'None')


    else :
        id_update = request.form['id']
        old_username_form = request.form['oldUsername']
        username_update = request.form.get('updatedUsername', 'None')

    cur = mysql.connection.cursor()

    cur.execute("select username from studentdata where id = %s" , (id_update))
    old_username = cur.fetchall()[0][0]

    if old_username == old_username_form : 
        cur.execute("UPDATE studentdata SET username = %s WHERE id = %s ;" , (username_update , id_update))
        print(f"Student name {old_username} updated to {old_username_form} successfully")
    else :
        print("id and student_name doesn't match!")

    mysql.connection.commit()
    cur.close()
    
    if request.is_json:
        return jsonify({"message": f""}), 201
    else:
        return redirect(url_for('database_bp.students_page'))