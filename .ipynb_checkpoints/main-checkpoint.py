from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# 数据库连接
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    conn = get_db_connection()
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.close()

# 路由：首页，显示所有记录
@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

# 路由：显示单个记录
@app.route('/<string:title>')
def post(title):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE title =?', (title,)).fetchone()
    conn.close()
    return render_template('post.html', post=post)

# 路由：创建新记录
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?,?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

# 路由：编辑记录
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id =?', (id,)).fetchone()
    conn.close()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        conn.execute('UPDATE posts SET title =?, content =? WHERE id =?', (title, content, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('edit.html', post=post)

# 路由：删除记录
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id =?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()  # 初始化数据库
    app.run(debug=True)
