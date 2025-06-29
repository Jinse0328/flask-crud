from flask import Flask, request, redirect, url_for, render_template, session, flash
import pymysql
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def connect():
    return pymysql.connect(
        host='localhost', user='root', password='asd098', db='crud_db', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor
    )


@app.route("/", methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        
        db = connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=%s AND user_pw=%s", (user_id, user_pw))
        user = cursor.fetchone()
        db.close()
        
        if user:
            session['user_id'] = user['user_id']
            session['user_name'] = user['user_name']
            return redirect(url_for('home'))
        else:
            flash("아이디 혹은 비밀번호가 틀렸습니다")
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route("/join/", methods=['GET', 'POST'])
def join(): 
    if request.method == 'POST':
        user_name = request.form['user_name']
        date_of_birth = request.form['date_of_birth']
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        user_pw_re = request.form['user_pw_re']
        if user_pw != user_pw_re:
            return "비밀번호가 일치하지 않습니다"
        
        db = connect()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (user_name, date_of_birth, user_id, user_pw) VALUES (%s, %s, %s, %s)", (user_name, date_of_birth, user_id, user_pw))
        db.commit()
        db.close()
        
        return redirect(url_for('login'))
    
    return render_template('join.html')


@app.route("/home/")
def home(): 
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    search = request.args.get('search', '')
    db = connect()
    cursor = db.cursor()
    if search:
        cursor.execute("SELECT * FROM posts WHERE title LIKE %s OR user_name LIKE %s ORDER BY num DESC", ('%' + search + '%', search))
    else:
        cursor.execute("SELECT * FROM posts ORDER BY num DESC")
    posts = cursor.fetchall()
    db.close()
    
    return render_template('home.html', posts=posts, search=search)


@app.route("/read/<int:num>")
def read(num):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM posts WHERE num = %s", (num,))
    post = cursor.fetchone()
    db.close()
    
    return render_template('read.html', post=post)


@app.route("/write/", methods=['GET', 'POST'])
def write():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        
        db = connect()
        cursor = db.cursor()
        cursor.execute("INSERT INTO posts (title, content, user_id, user_name) VALUES (%s, %s, %s, %s)", (title, content, user_id, user_name))
        db.commit()
        db.close()
        return redirect(url_for('home'))
    
    return render_template('write.html')


@app.route("/mypage/")
def mypage():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM posts WHERE user_id = %s ORDER BY num DESC", (user_id,))
    posts = cursor.fetchall()
    db.close()
    
    return render_template('mypage.html', posts=posts)
    
    
@app.route("/delete/<int:num>", methods=['POST'])
def delete(num):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM posts WHERE num = %s", (num,))
    post = cursor.fetchone()
    
    if post and post['user_id'] == user_id:
        cursor.execute("DELETE FROM posts WHERE num = %s", (num,))
        db.commit()
    
    db.close()
    return redirect(url_for('mypage'))


@app.route("/update/<int:num>", methods=['GET', 'POST'])
def update(num):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM posts WHERE num = %s", (num,))
    post = cursor.fetchone()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        cursor.execute("UPDATE posts SET title=%s, content=%s WHERE num=%s", (title, content, num))
        db.commit()
        db.close()
        return redirect(url_for('mypage'))
    
    db.close()
    return render_template('update.html', post=post)
        


if __name__ == '__main__':
    app.run(port="5002", debug=True)
