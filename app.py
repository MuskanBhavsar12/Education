import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

# -------------------- FLASK APP CONFIG --------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-123'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Project folder path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'smart_institute.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- DATABASE MODELS --------------------
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    duration_weeks = db.Column(db.Integer)
    level = db.Column(db.String(50))
    rating = db.Column(db.Float)
    short_desc = db.Column(db.String(255))
    image_url = db.Column(db.String(500))

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.String(255))
    icon = db.Column(db.String(100))
    image_url = db.Column(db.String(500))

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    image_url = db.Column(db.String(500))
    thumb_url = db.Column(db.String(500))

# -------------------- LOGIN DECORATOR --------------------
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('admin'):
            flash('Please login first!', 'danger')
            return redirect(url_for('admin_login'))
        return view(*args, **kwargs)
    return wrapped

# -------------------- FRONTEND ROUTES --------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services_page():
    return render_template('services.html', services=Service.query.all())

@app.route('/courses')
def courses_page():
    return render_template('courses.html', courses=Course.query.all())

@app.route('/gallery')
def gallery_page():
    return render_template('gallery.html', gallery=Gallery.query.all())

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/student_corner')
@app.route('/student-corner')
def student_corner():
    return render_template('student_corner.html')


# -------------------- ADMIN ROUTES --------------------
@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid Credentials', 'danger')
    return render_template('admin_login.html')

@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    return render_template(
        'admin_dashboard.html',
        courses=Course.query.all(),
        services=Service.query.all(),
        gallery=Gallery.query.all()
    )

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

#-------------------- ADMIN CRUD ROUTES --------------------

# Courses
@app.route('/admin/courses/add', methods=['POST'])
@login_required
def add_course():
    c = Course(
        title=request.form['title'],
        duration_weeks=request.form.get('duration_weeks') or 0,
        level=request.form.get('level') or '',
        rating=request.form.get('rating') or 0,
        short_desc=request.form.get('short_desc') or '',
        image_url=request.form.get('image_url') or ''
    )
    db.session.add(c)
    db.session.commit()
    flash('Course added!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/courses/<int:id>/edit', methods=['POST'])
@login_required
def edit_course(id):
    c = Course.query.get_or_404(id)
    c.title = request.form['title']
    c.duration_weeks = request.form.get('duration_weeks') or 0
    c.level = request.form.get('level') or ''
    c.rating = request.form.get('rating') or 0
    c.short_desc = request.form.get('short_desc') or ''
    c.image_url = request.form.get('image_url') or ''
    db.session.commit()
    flash('Course updated!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/courses/<int:id>/delete', methods=['POST'])
@login_required
def delete_course(id):
    c = Course.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    flash('Course deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

# Services
@app.route('/admin/services/add', methods=['POST'])
@login_required
def add_service():
    s = Service(
        title=request.form['title'],
        short_desc=request.form.get('short_desc') or '',
        icon=request.form.get('icon') or '',
        image_url=request.form.get('image_url') or ''
    )
    db.session.add(s)
    db.session.commit()
    flash('Service added!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/services/<int:id>/edit', methods=['POST'])
@login_required
def edit_service(id):
    s = Service.query.get_or_404(id)
    s.title = request.form['title']
    s.short_desc = request.form.get('short_desc') or ''
    s.icon = request.form.get('icon') or ''
    s.image_url = request.form.get('image_url') or ''
    db.session.commit()
    flash('Service updated!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/services/<int:id>/delete', methods=['POST'])
@login_required
def delete_service(id):
    s = Service.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    flash('Service deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

# Gallery
@app.route('/admin/gallery/add', methods=['POST'])
@login_required
def add_gallery():
    g = Gallery(
        title=request.form.get('title') or '',
        image_url=request.form.get('image_url') or '',
        thumb_url=request.form.get('thumb_url') or ''
    )
    db.session.add(g)
    db.session.commit()
    flash('Gallery image added!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/gallery/<int:id>/edit', methods=['POST'])
@login_required
def edit_gallery(id):
    g = Gallery.query.get_or_404(id)
    g.title = request.form.get('title') or ''
    g.image_url = request.form.get('image_url') or ''
    g.thumb_url = request.form.get('thumb_url') or ''
    db.session.commit()
    flash('Gallery updated!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/gallery/<int:id>/delete', methods=['POST'])
@login_required
def delete_gallery(id):
    g = Gallery.query.get_or_404(id)
    db.session.delete(g)
    db.session.commit()
    flash('Gallery deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

# -------------------- SEED ROUTE (Optional initial data) --------------------
@app.route('/seed-db')
def seed_db():
    # Sample courses
    if not Course.query.first():
        c1 = Course(title="Python Basics", duration_weeks=4, level="Beginner", rating=4.5, short_desc="Learn Python", image_url="")
        c2 = Course(title="Web Development", duration_weeks=8, level="Intermediate", rating=4.7, short_desc="Full stack web dev", image_url="")
        db.session.add_all([c1, c2])

    # Sample services
    if not Service.query.first():
        s1 = Service(title="Web Design", short_desc="Modern UI/UX", icon="", image_url="")
        s2 = Service(title="App Development", short_desc="Mobile apps", icon="", image_url="")
        db.session.add_all([s1, s2])

    # Sample gallery
    if not Gallery.query.first():
        g1 = Gallery(title="Campus View", image_url="", thumb_url="")
        g2 = Gallery(title="Lab Session", image_url="", thumb_url="")
        db.session.add_all([g1, g2])

    db.session.commit()
    return "Database seeded with sample data!"

# -------------------- RUN --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)