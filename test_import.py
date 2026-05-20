import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from parser import extract_text_from_docx, extract_text_from_pdf, parse_questions
    print("导入成功！")
    print(f"extract_text_from_docx: {extract_text_from_docx}")
    print(f"extract_text_from_pdf: {extract_text_from_pdf}")
    print(f"parse_questions: {parse_questions}")
except ImportError as e:
    print(f"导入失败: {e}")
    import traceback
    traceback.print_exc()