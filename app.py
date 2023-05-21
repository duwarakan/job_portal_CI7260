from flask import Flask, render_template, request, redirect, url_for, session, send_file
from sqlalchemy import or_, and_
import io, os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from models import db, Employer, Candidate, CV
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

logger = Config.init_logger()
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/candidate_register', methods=['GET', 'POST'])
def candidate_register():
    print("/candidate_register used")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_candidate = Candidate(username=username, email=email)
        new_candidate.set_password(password)
        db.session.add(new_candidate)
        db.session.commit()
        logger.info("A Candidate Successfully registered" +" "+username)
        return redirect(url_for('candidate_login'))
    return render_template('candidate_register.html')





@app.route('/employer_register', methods=['GET', 'POST'])
def employer_register():
    print("/employer_register used")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        new_employer = Employer(username=username, email=email)
        new_employer.set_password(password)
        db.session.add(new_employer)
        db.session.commit()
        logger.info("A Employer Successfully registered", username)
        return redirect(url_for('employer_login'))
    return render_template('employer_register.html')

@app.route('/candidate_login', methods=['GET', 'POST'])
def candidate_login():
    print("/candidate_login used")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        candidate = Candidate.query.filter_by(username=username).first()

        if candidate and candidate.check_password(password):
            session['candidate_id'] = candidate.id
            logger.info("A Candidate Successfully logged in"+" "+ username)
            return redirect(url_for('candidate_dashboard'))
        else:
            return render_template('candidate_login.html', message='Invalid credentials')

    return render_template('candidate_login.html')

@app.route('/employer_login', methods=['GET', 'POST'])
def employer_login():
    print("/employer_login used")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        employer = Employer.query.filter_by(username=username).first()
        if employer and employer.check_password(password):
            session['employer_id'] = employer.id
            logger.info("A Employer Successfully logged in"+" "+ username)
            return redirect(url_for('employer_dashboard'))
        else:
            return render_template('employer_login.html', message='Invalid credentials')
    return render_template('employer_login.html')


@app.route('/candidate_dashboard')
def candidate_dashboard():
    print("/candidate dashboard used")
    if 'candidate_id' in session:
        logger.info("A Candidate Successfully used candidate dashboard"+" "+ str(session['candidate_id']))
        return render_template('candidate_dashboard.html')
    else:
        return redirect(url_for('candidate_login'))


def advanced_search(filters):
    query = CV.query
    print(filters)
    if 'search_name' in filters:
        query = query.filter(CV.full_name.ilike(f"%{filters['search_name']}%"))

    if 'search_sector' in filters:
        query = query.filter(CV.sector.ilike(f"%{filters['search_sector']}%"))

    if 'search_address' in filters:
        query = query.filter(CV.address.ilike(f"%{filters['search_address']}%"))

    if 'search_experience' in filters:
        query = query.filter(CV.experience >= filters['search_experience'])

    if 'search_gcse_passes' in filters:
        query = query.filter(CV.gcse_passes >= filters['search_gcse_passes'])

    if 'search_education_level' in filters:
        print('search_education_level')
        print(filters['search_education_level'])
        query = query.filter(CV.education_level >= filters['search_education_level'])

    if 'search_skills' in filters:
        skills = [skill.strip() for skill in filters['search_skills'].split(',')]
        query = query.filter(or_(CV.skills.ilike(f"%{skill}%") for skill in skills))

    if 'search_contact_number' in filters:
        query = query.filter(CV.contact_number.ilike(f"%{filters['search_contact_number']}%"))

    if 'search_past_experience' in filters:
        query = query.filter(CV.past_experience.ilike(f"%{filters['search_past_experience']}%"))

    print("query..........", query)
    return query.all()


@app.route('/employer_dashboard', methods=['GET', 'POST'])
def employer_dashboard():
    print("/employer dashboard used")
    if 'employer_id' in session:
        if request.method == 'POST':
            filter_names = [
                'search_name',
                'search_sector',
                'search_address',
                'search_experience',
                'search_skills',
                'search_contact_number',
                'search_past_experience',
                'search_gcse_passes',
                'search_education_level'
            ]

            filters = {
                filter_name: (int(value) if filter_name == 'search_experience' and value else value)
                for filter_name, value in request.form.items() if value and filter_name in filter_names
            }

            print("Filters: ..........................", filters)

            search_result = advanced_search(filters)
            return render_template('employer_dashboard.html', search_result=search_result)
        logger.info("A Employer Successfully used employer dashboard"+" "+ str(session['employer_id']))
        return render_template('employer_dashboard.html')
    else:
        return redirect(url_for('employer_login'))


@app.route('/candidate_profile', methods=['GET', 'POST'])
def candidate_profile():
    print("/candidate profile used")
    if 'candidate_id' not in session:
        return redirect(url_for('candidate_login'))
    candidate = Candidate.query.get(session['candidate_id'])
    if request.method == 'POST':
        candidate.username = request.form['username']
        candidate.email = request.form['email']
        candidate.set_password(request.form['password'])
        db.session.commit()
        logger.info("Candidate changed their settings" + " " + str(session['candidate_id'])+ " " + candidate.username)
        return redirect(url_for('candidate_dashboard'))
    return render_template('candidate_profile.html', candidate=candidate)


@app.route('/employer_profile', methods=['GET', 'POST'])
def employer_profile():
    print("/employer profile used")
    if 'employer_id' not in session:
        return redirect(url_for('employer_login'))
    employer = Employer.query.get(session['employer_id'])
    if request.method == 'POST':
        employer.username = request.form['username']
        employer.email = request.form['email']
        employer.set_password(request.form['password'])
        db.session.commit()
        logger.info("Employer changed their settings" + " " + str(session['employer_id']) + " " + employer.username)
        return redirect(url_for('employer_dashboard'))
    return render_template('employer_profile.html', employer=employer)


@app.route('/candidate_cv', methods=['GET', 'POST'])
def candidate_cv():
    print("/candidate_cv used")
    if 'candidate_id' not in session:
        return redirect(url_for('candidate_login'))
    candidate = Candidate.query.get(session['candidate_id'])
    cv = candidate.cv if candidate.cv else None
    if request.method == 'POST':
        if cv is None:
            cv = CV(candidate_id=session['candidate_id'])
            db.session.add(cv)
        cv.full_name = request.form['full_name']
        cv.sector = request.form['sector']
        cv.address = request.form['address']
        cv.experience = request.form['experience']
        cv.skills = request.form['skills']
        cv.references = request.form['references']
        cv.contact_number = request.form['contact_number']
        cv.gcse_passes = request.form['gcse_passes']
        cv.education_level = request.form['education_level']
        cv.past_experience = request.form['past_experience']
        db.session.commit()
        logger.info("checked their cv" + " " + cv.full_name)
        return redirect(url_for('candidate_dashboard'))
    return render_template('candidate_cv.html', cv=cv)  # Pass the cv object to the template


@app.route('/logout')
def logout():
    print("/logout used")
    session.pop('candidate_id', None)
    session.pop('employer_id', None)
    logger.info("Logged out")
    return redirect(url_for('home'))


@app.route('/cv/<int:cv_id>', methods=['GET'])
def cv_detail(cv_id):
    print("/cv personalised used")
    cv = CV.query.get_or_404(cv_id)
    if (cv.education_level == 2):
        cv.education_level = "GCSE"
    elif (cv.education_level == 3):
        cv.education_level = "Bachelor's Degree"
    else:
        cv.education_level = "Master's Degree"
    return render_template('cv_detail.html', cv=cv)


def create_pdf(cv):
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Define custom styles for the paragraphs
    title_style = ParagraphStyle(
        name='TitleStyle',
        parent=styles['Heading1'],
        fontSize=14,
        leading=18,
        spaceAfter=10
    )
    info_style = ParagraphStyle(
        name='InfoStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        spaceAfter=5
    )
    line_style = ParagraphStyle(
        name='LineStyle',
        parent=styles['Normal'],
        fontSize=1,
        leading=2,
        spaceAfter=10,
        spaceBefore=10
    )

    if (cv.education_level == 2):
        cv.education_level = "GCSE ALevel"
    elif (cv.education_level == 3):
        cv.education_level = "Bachelor's Degree"
    else:
        cv.education_level = "Master's Degree"

    # Add the content to the PDF
    elements.append(Paragraph(f"<u>Full Name:</u> {cv.full_name}", title_style))
    elements.append(Spacer(1, 12))  # Add space below the title
    elements.append(Paragraph(f"<u>Sector:</u> {cv.sector}", info_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<u>Address:</u> {cv.address}", info_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<u>Experience:</u> {cv.experience} years", info_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<u>Skills:</u> {cv.skills}", info_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<u>GCSE Passes:</u> {cv.gcse_passes}", info_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<u>Education Level:</u> {cv.education_level}", info_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<u>References:</u> {cv.references}", info_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<u>Contact Number:</u> {cv.contact_number}", info_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<u>Past Experience:</u> {cv.past_experience}", info_style))

    # Add lines between each title
    for _ in range(len(elements) - 1):
        elements.append(Paragraph("<hr/>", line_style))

    # Build the PDF document
    doc.build(elements)

    output.seek(0)
    return output


@app.route('/download_cv')
def download_cv():
    if 'candidate_id' not in session:
        return redirect(url_for('candidate_login'))
    candidate = Candidate.query.get(session['candidate_id'])
    cv = candidate.cv if candidate.cv else None
    if cv is None:
        return "No CV available", 404

    pdf = create_pdf(cv)
    return send_file(pdf, as_attachment=True, download_name="cv.pdf")


if __name__ == '__main__':
    try:
        with app.app_context():
            if os.path.exists(Config.First_run):
                db.create_all()
                logger.info("New tables are created")
        app.run(debug=True)
    except Exception as e:
        logger.critical(e)


