import re

def parse_questions(text):
    questions = []
    
    pattern = r'(\d+)\s*[.．、]\s*\(([^)]+)\)\s*'
    matches = list(re.finditer(pattern, text))
    
    for i, match in enumerate(matches):
        question_id = int(match.group(1))
        question_type = match.group(2).strip()
        
        start_pos = match.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start_pos:end_pos].strip()
        
        question_data = {
            "id": question_id,
            "type": question_type,
            "question": "",
            "options": {},
            "correct_answer": "",
            "user_answer": ""
        }
        
        lines = body.split('\n')
        question_lines = []
        option_pattern = r'^([A-E])[.．、]\s*(.+)$'
        answer_pattern = r'正确答案[：:]\s*(.+)$'
        user_answer_pattern = r'我的答案[：:]\s*(.+)$'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            option_match = re.match(option_pattern, line)
            if option_match:
                option_key = option_match.group(1).upper()
                option_value = option_match.group(2).strip()
                question_data["options"][option_key] = option_value
            else:
                answer_match = re.search(answer_pattern, line)
                if answer_match:
                    question_data["correct_answer"] = answer_match.group(1).strip()
                    continue
                
                user_answer_match = re.search(user_answer_pattern, line)
                if user_answer_match:
                    question_data["user_answer"] = user_answer_match.group(1).strip()
                    continue
                
                question_lines.append(line)
        
        question_data["question"] = " ".join(question_lines).strip()
        
        if question_type == "填空题":
            bracket_pattern = r'【([^】]+)】'
            bracket_matches = re.findall(bracket_pattern, question_data["question"])
            if bracket_matches:
                question_data["correct_answer"] = bracket_matches[0]
        
        questions.append(question_data)
    
    return {
        "questions": questions,
        "total": len(questions)
    }

test_text = """1. (单选题) 以下哪个是Python的基本数据类型？
A. 整数
B. 字符串
C. 列表
D. 以上都是
正确答案：D
我的答案：C

2. (填空题) Python中用于定义函数的关键字是【def】。
正确答案：def
我的答案：function

3. (判断题) Python是解释型语言。
正确答案：正确
我的答案：错误

4. (多选题) 以下哪些是Python的内置函数？
A. print()
B. len()
C. max()
D. 以上都是
正确答案：D
我的答案：A"""

result = parse_questions(test_text)
print(f"解析成功！共找到 {result['total']} 道题目")
print("\n题目详情：")
for q in result['questions']:
    print(f"\n题目 {q['id']} ({q['type']}):")
    print(f"  题干: {q['question']}")
    if q['options']:
        print(f"  选项: {q['options']}")
    print(f"  正确答案: {q['correct_answer']}")
    print(f"  我的答案: {q['user_answer']}")