from flask import Flask, render_template, request, jsonify
import os
from quiz_parser import extract_text_from_docx_bytes, extract_text_from_pdf_bytes, parse_questions

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

ALLOWED_EXTENSIONS = {'docx', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return jsonify({'error': '没有文件被上传'}), 400
    
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    
    all_text = ""
    
    for file in files:
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            file_bytes = file.read()
            
            try:
                if ext == 'docx':
                    text = extract_text_from_docx_bytes(file_bytes)
                elif ext == 'pdf':
                    text = extract_text_from_pdf_bytes(file_bytes)
                else:
                    continue
                
                all_text += text + "\n\n"
            except Exception as e:
                return jsonify({'error': f'文件解析失败: {str(e)}'}), 400
    
    if not all_text.strip():
        return jsonify({'error': '未能从文件中提取到任何文本'}), 400
    
    try:
        result = parse_questions(all_text)
        if result['total'] == 0:
            return jsonify({'error': '未能解析出任何题目，请检查文件格式'}), 400
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'题目解析失败: {str(e)}'}), 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'false').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)