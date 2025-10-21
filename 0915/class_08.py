# 학생 클래스 생성
# 인스턴스 변수 : 이름, 국, 영, 수
# 인스턴스 매서드 : 총점, 평균, 학점
class Student:
    def __init__(self, name, kor, eng, math):
        self.name = name
        self.kor = kor
        self.eng = eng
        self.math = math

    def total(self):
        return self.kor + self.eng + self.math

    def average(self):
        return self.total() / 3

    def grade(self):
        avg = self.average()
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F' 
    def __str__(self):
            return f'이름: {self.name}, 총점: {self.total()}, 평균: {self.average():.2f}, 학점: {self.grade()}'

# 학생 인스턴스 생성
student1 = Student("홍길동", 85, 90, 78)    
student2 = Student("김철수", 92, 88, 95)
print(student1)
print(student2)
