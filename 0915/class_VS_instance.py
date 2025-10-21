class Student:
    # 클래스 변수 (모든 학생이 공유)
    school_name = "파이썬 고등학교"    # 모든 학생이 다니는 학교는 같음
    
    def __init__(self, name):
        # 인스턴스 변수 (학생마다 다름)
        self.name = name              # 각 학생의 이름
        self.grade = 0                # 각 학생의 성적

# 사용 예시
student1 = Student("철수")
student2 = Student("영희")

# 클래스 변수는 모든 인스턴스가 공유
print(student1.school_name)  # "파이썬 고등학교"
print(student2.school_name)  # "파이썬 고등학교"

# 인스턴스 변수는 각 인스턴스마다 다른 값을 가질 수 있음
student1.grade = 90
student2.grade = 85

print(student1.grade)  # 90
print(student2.grade)  # 85