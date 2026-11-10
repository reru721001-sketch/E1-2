class Quiz:
    """퀴즈 한 문제를 나타내는 클래스"""

    def __init__(self, question, choices, answer):
        self.question = question   # 문제 (str)
        self.choices = choices     # 선택지 4개 (list)
        self.answer = answer       # 정답 번호 1~4 (int)

    def display(self, number):
        """문제와 선택지를 화면에 출력한다."""
        print()
        print("-" * 40)
        print(f"[문제 {number}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답인지 True/False로 알려준다."""
        return user_answer == self.answer

    def to_dict(self):
        """JSON으로 저장할 수 있도록 dict로 바꾼다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @staticmethod
    def from_dict(data):
        """dict(저장된 데이터)를 다시 Quiz 객체로 만든다."""
        return Quiz(data["question"], data["choices"], data["answer"])