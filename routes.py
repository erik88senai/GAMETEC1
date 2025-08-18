from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from app import app
from utils import *
from team_system import load_teams_data
import os
import tempfile

@app.route('/')
def index():
    """Main dashboard page"""
    data = load_data()
    teams_data = load_teams_data()
    return render_template('index.html', data=data, modalidades=MODALIDADES, criterios=CRITERIOS, teams_data=teams_data)

@app.route('/register_student', methods=['POST'])
def register_student():
    """Register a single student"""
    modalidade = request.form.get('modalidade')
    nome = request.form.get('nome', '').strip()
    
    if not nome:
        flash('Por favor, digite um nome válido.', 'warning')
        return redirect(url_for('index'))
    
    if modalidade not in MODALIDADES:
        flash('Modalidade inválida.', 'error')
        return redirect(url_for('index'))
    
    result = register_student_func(modalidade, nome)
    flash(result['message'], result['type'])
    return redirect(url_for('index'))

@app.route('/bulk_register', methods=['POST'])
def bulk_register():
    """Register students in bulk from CSV/Excel file"""
    modalidade = request.form.get('modalidade')
    
    if 'file' not in request.files:
        flash('Nenhum arquivo foi selecionado.', 'warning')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo foi selecionado.', 'warning')
        return redirect(url_for('index'))
    
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        result = bulk_register_func(modalidade, filepath)
        flash(result['message'], result['type'])
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
            
        return redirect(url_for('index'))
    
    flash('Tipo de arquivo não permitido. Use CSV ou Excel.', 'error')
    return redirect(url_for('index'))

@app.route('/add_points', methods=['POST'])
def add_points():
    """Add points to a student"""
    modalidade = request.form.get('modalidade')
    aluno = request.form.get('aluno')
    criterios = request.form.getlist('criterios')
    variable_points = {}
    
    # Handle variable criteria
    for criterio in criterios:
        if CRITERIOS.get(criterio) == "variável":
            points_key = f"points_{criterio}"
            try:
                variable_points[criterio] = int(request.form.get(points_key, 0))
            except ValueError:
                flash(f'Valor inválido para {criterio}.', 'error')
                return redirect(url_for('index'))
    
    result = add_points_func(modalidade, aluno, criterios, variable_points)
    flash(result['message'], result['type'])
    return redirect(url_for('index'))

@app.route('/delete_student', methods=['POST'])
def delete_student():
    """Delete a student"""
    modalidade = request.form.get('modalidade')
    aluno = request.form.get('aluno')
    
    result = delete_student_func(modalidade, aluno)
    flash(result['message'], result['type'])
    return redirect(url_for('index'))

@app.route('/bulk_delete', methods=['POST'])
def bulk_delete():
    """Delete multiple students at once"""
    modalidade = request.form.get('modalidade')
    alunos_selected = request.form.getlist('alunos_selected')
    
    if not alunos_selected:
        flash('Nenhum aluno foi selecionado para exclusão.', 'warning')
        return redirect(url_for('index'))
    
    result = bulk_delete_func(modalidade, alunos_selected)
    flash(result['message'], result['type'])
    return redirect(url_for('index'))

@app.route('/get_students/<modalidade>')
def get_students(modalidade):
    """Get students list for a modality (AJAX endpoint)"""
    data = load_data()
    students = list(data.get(modalidade, {}).keys())
    return jsonify(students)

@app.route('/get_ranking/<modalidade>')
def get_ranking(modalidade):
    """Get ranking for a modality (AJAX endpoint)"""
    data = load_data()
    
    if modalidade == "Geral":
        ranking = get_general_ranking(data)
    else:
        ranking = get_modality_ranking(data, modalidade)
    
    return jsonify(ranking)

@app.route('/export_html/<modalidade>')
def export_html(modalidade):
    """Export ranking to HTML file"""
    try:
        filepath = export_ranking_html(modalidade)
        return send_file(filepath, as_attachment=True, download_name=f"ranking_{modalidade}.html")
    except Exception as e:
        flash(f'Erro ao exportar: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/reset_data', methods=['POST'])
def reset_data():
    """Reset all data (for testing purposes)"""
    try:
        data = {mod: {} for mod in MODALIDADES}
        save_data(data)
        flash('Todos os dados foram resetados.', 'success')
    except Exception as e:
        flash(f'Erro ao resetar dados: {str(e)}', 'error')
    return redirect(url_for('index'))

@app.route('/teams_admin')
def teams_admin():
    """Admin view for managing teams"""
    teams_data = load_teams_data()
    main_data = load_data()
    
    # Create team summary with statistics
    team_summary = []
    for team_id, team in teams_data['teams'].items():
        members = []
        total_points = 0
        
        for member_id in team['members']:
            member = teams_data['students'].get(member_id)
            if member:
                student_points = main_data.get(team['modalidade'], {}).get(member['name'], 0)
                total_points += student_points
                members.append({
                    'name': member['name'],
                    'email': member['email'],
                    'points': student_points,
                    'is_captain': member_id == team['captain_id']
                })
        
        team_summary.append({
            'id': team_id,
            'name': team['name'],
            'description': team.get('description', ''),
            'modalidade': team['modalidade'],
            'access_code': team['access_code'],
            'members': members,
            'member_count': len(members),
            'total_points': total_points,
            'average_points': total_points / len(members) if members else 0,
            'created_at': team.get('created_at', 'N/A')
        })
    
    # Sort teams by total points
    team_summary.sort(key=lambda x: x['total_points'], reverse=True)
    
    return render_template('teams_admin.html', teams=team_summary, modalidades=MODALIDADES)
