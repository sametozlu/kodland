from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Veritabanı yapılandırması
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

# Veritabanı modeli
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)

# Veritabanını oluşturma
with app.app_context():
    db.create_all()

# Ana sayfa rotası
@app.route('/')
def home():
    highest_score = Score.query.order_by(Score.score.desc()).first()
    user_name = session.get('name', 'Guest')  # Kullanıcı adı yoksa 'Guest' göster
    return render_template('index.html', highest_score=highest_score, user_name=user_name)

# Form gönderimi ve puan hesaplama
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    session['name'] = name  # Kullanıcı adını oturuma kaydet

    # Yeni form elemanları
    list_answer = request.form.get('list')
    loop_answer = request.form.get('loop')
    tuple_vs_list = request.form.get('tuple_vs_list')

    # Basit puanlama sistemi (örnek olarak)
    score = 0
    if list_answer == 'myList = [1, 2, 3]':
        score += 1
    if loop_answer == 'for i in myList:':
        score += 1
    if tuple_vs_list:
        score += 1  # Tuple ve liste farkına dair cevap verildiği için ek puan

    # Puanı veritabanına kaydet
    new_score = Score(name=name, score=score)
    db.session.add(new_score)
    db.session.commit()

    # En yüksek skoru yeniden sorgula
    highest_score = Score.query.order_by(Score.score.desc()).first()

    return render_template('result.html', name=name, score=score, user_name=name, highest_score=highest_score)


# Hakkında sayfası
@app.route('/about')
def about():
    user_name = session.get('name', 'Guest')
    return render_template('about.html', user_name=user_name)

# Uygulamayı çalıştırma
if __name__ == '__main__':
    app.run(debug=True)
