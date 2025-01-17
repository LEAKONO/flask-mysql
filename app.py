from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Update with your Workbench credentials
app.config['MYSQL_HOST'] = '127.0.0.1'  # Or 'localhost'
app.config['MYSQL_USER'] = 'root'  # Replace with your Workbench username
app.config['MYSQL_PASSWORD'] = 'leakono'  # Replace with your Workbench password
app.config['MYSQL_DB'] = 'todo_db'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task = request.form['task']
        if not task:
            flash('Task cannot be empty!', 'error')
            return redirect(url_for('add_task'))

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
        mysql.connection.commit()
        cursor.close()
        flash('Task added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_task.html')
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    cursor = mysql.connection.cursor()
    
    if request.method == 'POST':
        updated_task = request.form['task']
        if not updated_task:
            flash('Task cannot be empty!', 'error')
            return redirect(url_for('edit_task', task_id=task_id))
        
        cursor.execute("UPDATE todos SET task = %s WHERE id = %s", (updated_task, task_id))
        mysql.connection.commit()
        cursor.close()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    
    # Fetch the task to be edited
    cursor.execute("SELECT * FROM todos WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cursor.close()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE todos SET status = 'completed' WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cursor.close()
    flash('Task marked as completed!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
