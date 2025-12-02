import os
import matplotlib.pyplot as plt

def load_students(path='data/students.txt'):
    students = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Assume first 3 digits are ID, rest is name
            student_id = line[:3]
            name = line[3:].strip()
            students[student_id] = name
    return students

def load_assignments(path='data/assignments.txt'):
    assignments = {}
    with open(path) as f:
        lines = [line.strip() for line in f if line.strip()]
        # Process every 3 lines as one assignment
        for i in range(0, len(lines), 3):
            name = lines[i]
            assignment_id = lines[i+1]
            points = int(lines[i+2])
            assignments[assignment_id] = (name, points)
    return assignments

def load_submissions(path='data/submissions/'):
    submissions = {}
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        if not os.path.isfile(full_path):
            continue
        with open(full_path) as f:
            line = f.read().strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) != 3:
                continue
            student_id, assignment_id, percent = parts
            submissions[(student_id, assignment_id)] = float(percent)
    return submissions

def student_grade(name, students, assignments, submissions):
    student_id = None
    for sid, sname in students.items():
        if sname.lower() == name.lower():
            student_id = sid
            break
    if not student_id:
        print("Student not found")
        return
    total_score = 0
    for aid, (aname, points) in assignments.items():
        percent = submissions.get((student_id, aid), 0)
        total_score += (percent/100)*points
    grade_percent = round(total_score/1000 * 100)
    print(f"{grade_percent}%")

def assignment_stats(name, assignments, submissions):
    assignment_id = None
    for aid, (aname, points) in assignments.items():
        if aname.lower() == name.lower():
            assignment_id = aid
            break
    if not assignment_id:
        print("Assignment not found")
        return

    scores = [percent for (sid, aid), percent in submissions.items() if aid == assignment_id]

    if not scores:
        print("No submissions found")
        return

    min_score = int(min(scores))
    max_score = int(max(scores))
    avg_score = int(sum(scores) / len(scores))

    print(f"Min: {min_score}%")
    print(f"Avg: {avg_score}%")
    print(f"Max: {max_score}%")

def assignment_graph(name, assignments, submissions):
    assignment_id = None
    for aid, (aname, points) in assignments.items():
        if aname.lower() == name.lower():
            assignment_id = aid
            break
    if not assignment_id:
        print("Assignment not found")
        return

    scores_percent = [
        percent
        for (sid, aid), percent in submissions.items()
        if aid == assignment_id
    ]

    if not scores_percent:
        print("No submissions found")
        return

    plt.hist(scores_percent, bins=range(50, 101, 5))
    plt.xticks([50, 60, 70, 80, 90, 100])
    plt.show()

def main():
    students = load_students()
    assignments = load_assignments()
    submissions = load_submissions()

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("Enter your selection: ").strip()

    if choice == '1':
        name = input("What is the student's name: ").strip()
        student_grade(name, students, assignments, submissions)
    elif choice == '2':
        name = input("What is the assignment name: ").strip()
        assignment_stats(name, assignments, submissions)
    elif choice == '3':
        name = input("What is the assignment name: ").strip()
        assignment_graph(name, assignments, submissions)
    else:
        print("invalid selection")

if __name__ == "__main__":
    main()