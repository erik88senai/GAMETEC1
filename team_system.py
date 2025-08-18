"""
New team-based system for Game Tec Edition
This will integrate with the existing JSON-based system while adding PostgreSQL support
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from utils import load_data, save_data, MODALIDADES
import json
import string
import random
import os

# Team system blueprint
teams = Blueprint('teams', __name__, url_prefix='/teams')

# File-based storage for team data (extending the current system)
TEAMS_FILE = 'teams_data.json'

def load_teams_data():
    """Load teams data from JSON file"""
    try:
        if os.path.exists(TEAMS_FILE):
            with open(TEAMS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'teams': {}, 'students': {}, 'next_id': 1}
    except:
        return {'teams': {}, 'students': {}, 'next_id': 1}

def save_teams_data(data):
    """Save teams data to JSON file and integrate with main system"""
    try:
        with open(TEAMS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Integrate teams with main system
        integrate_teams_with_main_system(data)
        return True
    except:
        return False

def integrate_teams_with_main_system(teams_data):
    """Integrate team students with the main ranking system"""
    main_data = load_data()
    
    # Add team students to the main ranking system
    for team_id, team in teams_data['teams'].items():
        modalidade = team['modalidade']
        
        # Ensure modalidade exists in main data
        if modalidade not in main_data:
            main_data[modalidade] = {}
        
        # Add each team member to the main system if not already there
        for member_id in team['members']:
            member = teams_data['students'].get(member_id)
            if member:
                student_name = member['name']
                # Add student to main ranking system if not exists
                if student_name not in main_data[modalidade]:
                    main_data[modalidade][student_name] = 0
    
    # Save updated main data
    save_data(main_data)

def generate_access_code():
    """Generate a random 8-character access code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@teams.route('/student/register', methods=['GET', 'POST'])
def student_register():
    """Student registration page"""
    if request.method == 'POST':
        teams_data = load_teams_data()
        
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        team_action = request.form.get('team_action')
        
        # Validation
        if not all([name, email, password]):
            flash('Todos os campos são obrigatórios.', 'error')
            return render_template('teams/student_register.html', modalidades=MODALIDADES)
        
        # Check if email already exists
        if any(student['email'] == email for student in teams_data['students'].values()):
            flash('Este email já está cadastrado.', 'error')
            return render_template('teams/student_register.html', modalidades=MODALIDADES)
        
        # Create student ID
        student_id = str(teams_data['next_id'])
        teams_data['next_id'] += 1
        
        # Create student data
        student_data = {
            'id': student_id,
            'name': name,
            'email': email,
            'password_hash': generate_password_hash(password),
            'team_id': None,
            'total_points': 0,
            'is_active': True,
            'created_at': str(json.dumps({})),  # Current timestamp placeholder
        }
        
        # Handle team creation or joining
        team_id = None
        if team_action == 'create':
            team_name = request.form.get('team_name', '').strip()
            modalidade = request.form.get('modalidade')
            description = request.form.get('description', '').strip()
            
            if not team_name or not modalidade:
                flash('Nome da equipe e modalidade são obrigatórios.', 'error')
                return render_template('teams/student_register.html', modalidades=MODALIDADES)
            
            # Check if team name already exists
            if any(team['name'] == team_name for team in teams_data['teams'].values()):
                flash('Já existe uma equipe com este nome.', 'error')
                return render_template('teams/student_register.html', modalidades=MODALIDADES)
            
            # Create team
            team_id = str(len(teams_data['teams']) + 1)
            teams_data['teams'][team_id] = {
                'id': team_id,
                'name': team_name,
                'description': description,
                'modalidade': modalidade,
                'captain_id': student_id,
                'access_code': generate_access_code(),
                'members': [student_id],
                'created_at': str(json.dumps({}))
            }
            
        elif team_action == 'join':
            access_code = request.form.get('access_code', '').strip().upper()
            
            if not access_code:
                flash('Código de acesso é obrigatório.', 'error')
                return render_template('teams/student_register.html', modalidades=MODALIDADES)
            
            # Find team by access code
            found_team = None
            for tid, team in teams_data['teams'].items():
                if team['access_code'] == access_code:
                    found_team = team
                    team_id = tid
                    break
            
            if not found_team:
                flash('Código de acesso inválido.', 'error')
                return render_template('teams/student_register.html', modalidades=MODALIDADES)
            
            # Add student to team
            teams_data['teams'][team_id]['members'].append(student_id)
        
        # Set team_id for student
        student_data['team_id'] = team_id
        teams_data['students'][student_id] = student_data
        
        # Save data and integrate with main system
        if save_teams_data(teams_data):
            flash('Cadastro realizado com sucesso! Seu perfil foi automaticamente adicionado ao sistema de ranking.', 'success')
            # Store student session
            session['student_id'] = student_id
            session['is_student'] = True
            return redirect(url_for('teams.student_dashboard'))
        else:
            flash('Erro ao cadastrar. Tente novamente.', 'error')
    
    return render_template('teams/student_register.html', modalidades=MODALIDADES)

@teams.route('/student/login', methods=['GET', 'POST'])
def student_login():
    """Student login page"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Email e senha são obrigatórios.', 'error')
            return render_template('teams/student_login.html')
        
        teams_data = load_teams_data()
        
        # Find student by email
        student = None
        for sid, student_data in teams_data['students'].items():
            if student_data['email'] == email:
                student = student_data
                break
        
        if student and check_password_hash(student['password_hash'], password):
            if not student['is_active']:
                flash('Sua conta está desativada.', 'error')
                return render_template('teams/student_login.html')
            
            # Create session
            session['student_id'] = student['id']
            session['is_student'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('teams.student_dashboard'))
        else:
            flash('Email ou senha incorretos.', 'error')
    
    return render_template('teams/student_login.html')

@teams.route('/student/dashboard')
def student_dashboard():
    """Student dashboard"""
    if not session.get('is_student'):
        flash('Por favor, faça login como aluno.', 'error')
        return redirect(url_for('teams.student_login'))
    
    teams_data = load_teams_data()
    student_id = session.get('student_id')
    student = teams_data['students'].get(student_id)
    
    if not student:
        flash('Aluno não encontrado.', 'error')
        session.clear()
        return redirect(url_for('teams.student_login'))
    
    # Get team data
    team = None
    if student['team_id']:
        team = teams_data['teams'].get(student['team_id'])
    
    # Get ranking data from existing system
    ranking_data = load_data()
    
    return render_template('teams/student_dashboard.html', 
                         student=student, 
                         team=team, 
                         teams_data=teams_data,
                         ranking_data=ranking_data)

@teams.route('/student/logout')
def student_logout():
    """Student logout"""
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('teams.student_login'))

@teams.route('/student/team/manage')
def manage_team():
    """Team management page for captains"""
    if not session.get('is_student'):
        flash('Por favor, faça login como aluno.', 'error')
        return redirect(url_for('teams.student_login'))
    
    teams_data = load_teams_data()
    student_id = session.get('student_id')
    student = teams_data['students'].get(student_id)
    
    if not student or not student['team_id']:
        flash('Você não está em nenhuma equipe.', 'error')
        return redirect(url_for('teams.student_dashboard'))
    
    team = teams_data['teams'].get(student['team_id'])
    
    if not team or team['captain_id'] != student_id:
        flash('Você não é o capitão desta equipe.', 'error')
        return redirect(url_for('teams.student_dashboard'))
    
    # Get team members
    members = []
    for member_id in team['members']:
        member = teams_data['students'].get(member_id)
        if member:
            members.append(member)
    
    return render_template('teams/manage_team.html', 
                         student=student, 
                         team=team, 
                         members=members)

@teams.route('/api/get_team_ranking/<team_id>')
def get_team_ranking(team_id):
    """API endpoint to get team ranking"""
    teams_data = load_teams_data()
    team = teams_data['teams'].get(team_id)
    
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    
    # Get points from existing ranking system
    ranking_data = load_data()
    modalidade = team['modalidade']
    
    team_ranking = []
    for member_id in team['members']:
        member = teams_data['students'].get(member_id)
        if member:
            points = ranking_data.get(modalidade, {}).get(member['name'], 0)
            team_ranking.append({
                'name': member['name'],
                'points': points,
                'email': member['email']
            })
    
    # Sort by points
    team_ranking.sort(key=lambda x: x['points'], reverse=True)
    
    return jsonify(team_ranking)