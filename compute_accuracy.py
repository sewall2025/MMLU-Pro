import glob
import sys
import json
import re
import random

assert len(sys.argv) > 1, 'You need to pass the directory'
path = sys.argv[1]
random.seed(12345)


def extract_answer(text, level):
    if level == 'l1':
        pattern = r"answer is \(?([A-J])\)?"
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None
    elif level == 'l2':
        pattern = r"answer is \(?([A-J])\)?"
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return extract_again(text)


def extract_again(text):
    match = re.search(r'.*[aA]nswer:\s*([A-J])', text)
    if match:
        return match.group(1)
    else:
        return extract_final(text)
    

def extract_final(text):
    pattern = r"\b[A-J]\b(?!.*\b[A-J]\b)"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(0)
    else:
        return None


for name in sorted(glob.glob(path + '/*_result.json')):
    print('Level 1 regex' + '==' * 20)
    succ, fail = 0, 0
    with open(name, 'r') as f:
        entries = json.load(f)
        if not isinstance(entries, list):
            continue
        for e in entries:
            if not isinstance(e, dict):
                continue
            if 'model_outputs' not in e or 'answer' not in e:
                continue
            pred = extract_answer(e['model_outputs'], 'l1')
            if pred is None:
                pred = random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])
            # Remove the None cases
            if pred == e['answer']:
                succ += 1
            else:
                fail += 1
    print(name, succ / (succ + fail) if (succ + fail) else 0)

    print('Level 2 regex' + '==' * 20)
    succ, fail = 0, 0
    with open(name, 'r') as f:
        entries = json.load(f)
        if not isinstance(entries, list):
            continue
        for e in entries:
            if not isinstance(e, dict):
                continue
            if 'model_outputs' not in e or 'answer' not in e:
                continue
            pred = extract_answer(e['model_outputs'], 'l2')
            if pred is None:
                pred = random.choice(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])
            # Remove the None cases
            if pred == e['answer']:
                succ += 1
            else:
                fail += 1
    print(name, succ / (succ + fail) if (succ + fail) else 0)
    
    print()
