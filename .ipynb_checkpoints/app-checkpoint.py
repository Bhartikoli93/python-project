#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask,render_template,request, jsonify                         # API
import sqlite3 as sql                                                            # database
import re                                                                        # regular expressions
import uuid                                                                      # ui
from datetime import datetime as dt                                              # date formates


# In[2]:


QUESTIONS = [
    {"field": "fullname", "question": "Enter Full Name"},
    {"field": "dob", "question": "Enter Date of Birth (YYYY-MM-DD)"},
    {"field": "age", "question": "Enter Age"},
    {"field": "gender", "question": "Enter Gender (Male/Female/Other)"},
    {"field": "marital_status", "question": "Enter Marital Status"},
    {"field": "mobile", "question": "Enter Mobile Number"},
    {"field": "email", "question": "Enter Email Address"},
    {"field": "aadhaar", "question": "Enter Aadhaar Number"},
    {"field": "address", "question": "Enter House No / Street"},
    {"field": "area", "question": "Enter Area / Locality"},
    {"field": "city", "question": "Enter City"},
    {"field": "state", "question": "Enter State"},
    {"field": "pincode", "question": "Enter Pincode"},
    {"field": "blood_group", "question": "Enter Blood Group"},
    {"field": "emergency_name", "question": "Emergency Contact Name"},
    {"field": "emergency_number", "question": "Emergency Contact Number"},
    {"field": "symptoms", "question": "Describe Symptoms"},
    {"field": "symptom_duration", "question": "How long have symptoms existed?"},
    {"field": "current_condition", "question": "Current Medical Condition"},
    {"field": "allergies", "question": "Any Allergies?"},
    {"field": "previous_surgery", "question": "Any Previous Surgery?"},
    {"field": "family_history", "question": "Family Medical History (Optional)"},
    {"field": "has_insurance", "question": "Do you have Health Insurance? (Yes/No)"},
    {"field": "insurance_provider", "question": "Insurance Provider Name"},
    {"field": "policy_number", "question": "Policy Number"},
    {"field": "insurance_validity", "question": "Policy Expiry Date (YYYY-MM-DD)"},
    {"field": "department", "question": "Preferred Department"},
    {"field": "preferred_doctor", "question": "Preferred Doctor"},
    {"field": "appointment_date", "question": "Appointment Date (YYYY-MM-DD)"},
    {"field": "appointment_time", "question": "Appointment Time (HH:MM)"}
]


# In[3]:


patient_sessions = {}


# In[4]:


def init_db():
    conn = sql.connect("hims.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        patient_id TEXT PRIMARY KEY,
        fullname TEXT,
        dob TEXT,
        age INTEGER,
        gender TEXT,
        marital_status TEXT,
        mobile TEXT,
        email TEXT,
        aadhaar TEXT,
        address TEXT,
        area TEXT,
        city TEXT,
        state TEXT,
        pincode TEXT,
        blood_group TEXT,
        emergency_name TEXT,
        emergency_number TEXT,
        symptoms TEXT,
        symptom_duration TEXT,
        current_condition TEXT,
        allergies TEXT,
        previous_surgery TEXT,
        family_history TEXT,
        has_insurance TEXT,
        insurance_provider TEXT,
        policy_number TEXT,
        insurance_validity TEXT,
        department TEXT,
        preferred_doctor TEXT,
        appointment_date TEXT,
        appointment_time TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()


# In[5]:


init_db() 





def validate(field,value):
    if field == 'fullname':
        return re.match(r'[A-Za-z]+$',value.replace(' ',''))
    if field == 'age':
        return value.isdigit() and (int(value)>=0 and int (value)<=120)
    if field =='mobile':
        return re.match(r'^\\+91-[0-9]{10}$',value)
    if field=='email':
        return re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',value)
    if field=='aadhaar':
        returnre.match(r'^\d{12}$',value)
    if field == 'pincode':
        return re.match(r'^\d{6}$',value)
    if field =='blood_group':
        return value.upper() in ['A+','A-','B+','B-','AB+','AB-','O+','O-']
    if field =='emergency_number':
        return re.match(r'^\\+91-[0-9]{10}$',value)
    return True


# In[7]:


def assign_ddepartment(symptoms):
    s = symptoms.lower()
    if 'chest' in s or 'heart' in s:
        return 'Caridology'
    elif 'bone' in s or 'fracture' in s:
        return'Orthopedics'
    elif 'skin' in s:
        return 'Dermatology'
    elif 'eye' in s:
        return'Ophthalmaology'
    elif 'brain' in s or 'headache' in s:
        return 'Neurology'
    elif 'lung' in s:
        return 'Pulmonology'
    elif 'teeth' in s: 
        return'Dentistry'
    return 'Genral Medicine'


# In[8]:


app=Flask(__name__)


# In[9]:


@app.route('/')
def home():
    return render_tempalte('index.html')


# In[10]:


@app.route('/start')
def start_chat():
    session_id=str(uuid.uuid4())
    patient_sessions[session_id]={'step':0,'data':{}}
    return jsonify({'session_id': session_id,'question':QUESTIONS[0]['question']})



# In[11]:


@app.route('/chat',methods=['Post'])
def chat():
    req = request.json
    session_id=req('session_id')
    answer =req['answer'].strip()
    session=patient_sessions[session_id]
    step = session['sep']
    field=QUESTIONS[step]['field']
    if not validate(field,answer):
        return jsonify({'success':False,
                       'massage':f'Invalid{field}.please enter vaild date'})
        session['data'][field]=answer
        if  field=='has_insuraance' and answer.lower()=='no':
            step+=4
            sessiom['step']=step
            return jsonify ({'success':True,
                            'completed':False,
                            'question':QUESTIONS[step]['question'],
                            'summary':session[data]})
            step+=1
            session['step']

            if step<len(Questions):
                return jsonify({'success': True ,
                                'completed':False,
                                'question':Questions[step]['question'],
                                'summary':session[data]})
                patient_id ='PAT'+date_time.now().strftime('%Y%m%d%H%M%S')
                auto_department =  assign_department(session['data'].get('symtoms',''))
                department = session['data'].get('department',auto_department)
                try :
                    conn = sql.connect('hims.db')
                    cur = sql.cursor()
                    values = (patient_id,
                             session['data']['fullname'],
                             session['data']['dob'],
                             session['data']['age'],
                             session['data']['gender'],
                             session['data']['matritial_satus'],
                             session['data']['mobile'],
                             session['data']['email'],
                             session['data']['aadhaar'],
                             session['data']['address'],
                             session['data']['area'],
                             session['data']['city'],
                             session['data']['state'],
                             session['data']['pincode'],
                             session['data']['blood_group'],
                             session['data']['emergency_name'],
                             session['data']['emergency_number'],
                             session['data']['symtoms'],
                             session['data']['symtoms_duration'],
                             session['data']['current_condition'],
                             session['data']['allergies'],
                             session['data']['previous_surgery'],
                             session['data']['family_history'],
                             session['data']['has_insurance'],
                             session['data']['insurance_provider'],
                             session['data']['policy_number'],
                             session['data']['insurance_validity'],
                             department,
                             session['data']['preferred_doctor'],
                             session['data']['appointment_date'],
                             session['data']['appointment_time'],
                             datetime.now().strftime('%Y-%m-%d %H:%M:%S')) 
                    curr.execute("""
                    insert into patients values
                    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",values)
                    conn.commit()
                    print('Patient data saved in HIMS DB successfully')

                except Exception as e:
                    print('Database Error :' ,str(e))
                    return jsonify({
                        'success':False,
                        'message':str(e) })
                finally:
                    conn.close()
                summary = session['data'].copy()

                summary['patient_id']=patient_id

                summary['assgin_department']=auto_department
                del patient_sessions['session_id']
                return jsonify({
                'success':True,
                'completed':True,
                'summary':summary})       


# In[12]:


@app.route("/patients")
def patients():
    conn - sql.connect('hims.db')
    conn.row_factory=sql.Roe
    cur = conn.cursor()
    cur.execute("""SELECT * FROM PATIENTS order by created_at DESC""")
    rows = [dict(row)]


# In[ ]:





# In[ ]:




