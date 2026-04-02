from flask import Flask, render_template, request, redirect
from database import get_db
import json

app = Flask(__name__)

# DASHBOARD
@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total FROM applications")
    stats = cursor.fetchone()
    conn.close()
    return render_template("dashboard.html", stats=stats)


# ---------------- COMPANIES ----------------
@app.route('/companies')
def companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies")
    data = cursor.fetchall()
    conn.close()
    return render_template("companies.html", companies=data)

@app.route('/add_company', methods=['POST'])
def add_company():
    name = request.form['name']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO companies (company_name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()
    return redirect('/companies')

@app.route('/delete_company/<int:id>')
def delete_company(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM companies WHERE company_id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/companies')

@app.route('/edit_company/<int:id>', methods=['GET','POST'])
def edit_company(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        cursor.execute("UPDATE companies SET company_name=%s WHERE company_id=%s", (name, id))
        conn.commit()
        conn.close()
        return redirect('/companies')

    cursor.execute("SELECT * FROM companies WHERE company_id=%s", (id,))
    company = cursor.fetchone()
    conn.close()
    return render_template("edit_company.html", company=company)


# ---------------- JOBS ----------------
@app.route('/jobs')
def jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jobs")
    data = cursor.fetchall()
    conn.close()
    return render_template("jobs.html", jobs=data)

@app.route('/add_job', methods=['POST'])
def add_job():
    title = request.form['title']
    skills = [s.strip() for s in request.form['skills'].split(',')]

    requirements = json.dumps({"skills": skills})

    conn = get_db()
    cursor = conn.cursor()

    # FIX: give company_id default 1
    cursor.execute(
        "INSERT INTO jobs (company_id, job_title, requirements) VALUES (%s,%s,%s)",
        (1, title, requirements)
    )

    conn.commit()
    conn.close()
    return redirect('/jobs')

@app.route('/delete_job/<int:id>')
def delete_job(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/jobs')

@app.route('/edit_job/<int:id>', methods=['GET','POST'])
def edit_job(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form['title']
        cursor.execute("UPDATE jobs SET job_title=%s WHERE job_id=%s", (title, id))
        conn.commit()
        conn.close()
        return redirect('/jobs')

    cursor.execute("SELECT * FROM jobs WHERE job_id=%s", (id,))
    job = cursor.fetchone()
    conn.close()
    return render_template("edit_job.html", job=job)


# ---------------- APPLICATIONS ----------------
@app.route('/applications')
def applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT a.application_id, a.status, j.job_title
    FROM applications a
    JOIN jobs j ON a.job_id = j.job_id
    """)
    data = cursor.fetchall()
    conn.close()
    return render_template("applications.html", applications=data)

@app.route('/add_application', methods=['POST'])
def add_application():
    job_id = request.form['job_id']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO applications (job_id, application_date) VALUES (%s, CURDATE())",
        (job_id,)
    )
    conn.commit()
    conn.close()
    return redirect('/applications')

@app.route('/delete_application/<int:id>')
def delete_application(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE application_id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/applications')

@app.route('/edit_application/<int:id>', methods=['GET','POST'])
def edit_application(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        status = request.form['status']
        cursor.execute("UPDATE applications SET status=%s WHERE application_id=%s", (status, id))
        conn.commit()
        conn.close()
        return redirect('/applications')

    cursor.execute("SELECT * FROM applications WHERE application_id=%s", (id,))
    app_data = cursor.fetchone()
    conn.close()
    return render_template("edit_application.html", app_data=app_data)


# ---------------- CONTACTS ----------------
@app.route('/contacts')
def contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    conn.close()
    return render_template("contacts.html", contacts=data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO contacts (company_id, first_name, last_name) VALUES (%s,%s,%s)",
        (1, first_name, last_name)
    )

    conn.commit()
    conn.close()
    return redirect('/contacts')


@app.route('/delete_contact/<int:id>')
def delete_contact(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE contact_id=%s", (id,))
    conn.commit()
    conn.close()
    return redirect('/contacts')


@app.route('/edit_contact/<int:id>', methods=['GET','POST'])
def edit_contact(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        cursor.execute(
            "UPDATE contacts SET first_name=%s, last_name=%s WHERE contact_id=%s",
            (first_name, last_name, id)
        )

        conn.commit()
        conn.close()
        return redirect('/contacts')

    cursor.execute("SELECT * FROM contacts WHERE contact_id=%s", (id,))
    contact = cursor.fetchone()
    conn.close()
    return render_template("edit_contact.html", contact=contact)


# ---------------- JOB MATCH ----------------
@app.route('/job_match', methods=['GET','POST'])
def job_match():
    results = []

    if request.method == 'POST':
        skills = [s.strip().lower() for s in request.form['skills'].split(',')]

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM jobs")
        jobs = cursor.fetchall()

        for job in jobs:
            if job['requirements']:
                req_json = json.loads(job['requirements'])
                req_skills = [r.lower() for r in req_json.get('skills', [])]

                match = sum(1 for s in skills if s in req_skills)

                if len(skills) > 0:
                    percent = int((match / len(skills)) * 100)
                else:
                    percent = 0

                results.append((job['job_title'], percent))

    return render_template("job_match.html", results=results)


if __name__ == '__main__':
    app.run(debug=True)