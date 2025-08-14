import json
import os
import pandas as pd
import tempfile
from datetime import datetime

# Data file
ARQUIVO_DADOS = "game_tec_data.json"

# Default criteria with points
CRITERIOS = {
    "Frequência escolar acima de 80%": 100,
    "Pontualidade": 50,
    "Participação em atividades extras": 70,
    "Cumprimento de tarefas escolares": 60,
    "Participação em ações": 80,
    "Trancamento de matrícula": -100,
    "Competições culturais/esportivas": "variável",
    "Realização de diagnóstica SAEP": 100,
    "Nota média ou acima no SAEP": 100,
    "Frequência abaixo de 75%": -70,
    "Receber advertências": -50,
    "Emprego na indústria": 100,
    "Locação de livros": 70,
    "Ações do Psicossocial": 70,
    "Curso no Senai Play": 50
}

# Modalities
MODALIDADES = ["Aprendizagem", "Técnico", "Técnico NEM"]

def load_data():
    """Load data from JSON file"""
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {mod: {} for mod in MODALIDADES}
    return {mod: {} for mod in MODALIDADES}

def save_data(data):
    """Save data to JSON file"""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx', 'xls'}

def register_student_func(modalidade, nome):
    """Register a single student"""
    data = load_data()
    
    if nome in data[modalidade]:
        return {"message": f"{nome} já está cadastrado.", "type": "info"}
    else:
        data[modalidade][nome] = 0
        save_data(data)
        return {"message": f"Aluno {nome} cadastrado com sucesso!", "type": "success"}

def bulk_register_func(modalidade, filepath):
    """Register students in bulk from file"""
    try:
        data = load_data()
        
        if filepath.endswith(".csv"):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        registered_count = 0
        for nome in df.iloc[:,0].dropna():
            nome = str(nome).strip()
            if nome and nome not in data[modalidade]:
                data[modalidade][nome] = 0
                registered_count += 1
        
        save_data(data)
        return {"message": f"Cadastro em massa concluído! {registered_count} alunos registrados.", "type": "success"}
        
    except Exception as e:
        return {"message": f"Falha ao importar arquivo: {str(e)}", "type": "error"}

def add_points_func(modalidade, aluno, criterios, variable_points=None):
    """Add points to a student"""
    if variable_points is None:
        variable_points = {}
        
    data = load_data()
    
    if not aluno or aluno not in data[modalidade]:
        return {"message": "Selecione um aluno válido.", "type": "warning"}
    
    total_pontos = 0
    for crit in criterios:
        if crit in CRITERIOS:
            pontos = CRITERIOS[crit]
            if pontos == "variável":
                pontos = variable_points.get(crit, 0)
            total_pontos += pontos
    
    data[modalidade][aluno] += total_pontos
    save_data(data)
    return {"message": f"{total_pontos} pontos adicionados para {aluno}!", "type": "success"}

def delete_student_func(modalidade, aluno):
    """Delete a student"""
    data = load_data()
    
    if aluno in data[modalidade]:
        del data[modalidade][aluno]
        save_data(data)
        return {"message": f"Aluno {aluno} removido com sucesso.", "type": "success"}
    else:
        return {"message": "Aluno não encontrado.", "type": "warning"}

def get_modality_ranking(data, modalidade):
    """Get ranking for a specific modality"""
    if modalidade not in data:
        return []
    
    ranking = sorted(data[modalidade].items(), key=lambda x: x[1], reverse=True)
    return [{"pos": pos, "nome": nome, "pontos": pontos} 
            for pos, (nome, pontos) in enumerate(ranking, start=1)]

def get_general_ranking(data):
    """Get general ranking combining all modalities"""
    total_geral = {}
    for mod in MODALIDADES:
        for aluno, pontos in data.get(mod, {}).items():
            total_geral[aluno] = total_geral.get(aluno, 0) + pontos
    
    ranking = sorted(total_geral.items(), key=lambda x: x[1], reverse=True)
    return [{"pos": pos, "nome": nome, "pontos": pontos} 
            for pos, (nome, pontos) in enumerate(ranking, start=1)]

def export_ranking_html(modalidade):
    """Export ranking to HTML file"""
    data = load_data()
    
    if modalidade == "Geral":
        ranking = get_general_ranking(data)
    else:
        ranking = get_modality_ranking(data, modalidade)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ranking - {modalidade}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #222; color: white; }}
            h1 {{ color: #f39c12; text-align: center; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
            th {{ background-color: #3498db; color: white; }}
            tr:nth-child(even) {{ background-color: #34495e; }}
            tr:nth-child(odd) {{ background-color: #2c3e50; }}
        </style>
    </head>
    <body>
        <h1>🎮 Ranking - {modalidade} 🎮</h1>
        <p style="text-align: center; color: #bdc3c7;">Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
        <table>
            <thead>
                <tr>
                    <th>Posição</th>
                    <th>Aluno</th>
                    <th>Pontos</th>
                </tr>
            </thead>
            <tbody>
    """
    
    for item in ranking:
        html_content += f"""
                <tr>
                    <td>{item['pos']}</td>
                    <td>{item['nome']}</td>
                    <td>{item['pontos']}</td>
                </tr>
        """
    
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    # Save to temporary file
    filename = f"ranking_{modalidade}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(tempfile.gettempdir(), filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return filepath
