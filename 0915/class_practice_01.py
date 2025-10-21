students = [
    {"name" : "윤인성", "korean": 87, "math": 98, "english": 88, "science": 95},
    {"name" : "연하진", "korean": 92, "math": 98, "english": 96, "science": 98},
    {"name" : "박지호", "korean": 76, "math": 96, "english": 94, "science": 90},
    {"name" : "김민서", "korean": 98, "math": 92, "english": 96, "science": 92},
    {"name" : "이수현", "korean": 95, "math": 98, "english": 98, "science": 98},
    {"name" : "홍길동", "korean": 64, "math": 88, "english": 92, "science": 92}
]

for student in students:
    total = student['korean'] + student['math'] + student['english'] + student['science']
    average = total / 4
    print(student['name'], total, average, sep='\t')

