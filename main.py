import json
import os
import random
import shutil

from quiz import Quiz
from quiz_data import get_default_quizzes

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")
BACKUP_FILE = STATE_FILE + ".bak"   # 손상된 파일을 보관할 백업 파일

class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = []        # 퀴즈 목록
        self.best_score = None   # 최고 점수 (None = 아직 안 풀어봄)
        self.load()              # 시작할 때 파일에서 불러오기

    def load(self):
        """state.json에서 퀴즈와 최고 점수를 불러온다."""
        if not os.path.exists(STATE_FILE):
            print("📂 저장된 파일이 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = get_default_quizzes()
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            self.best_score = data.get("best_score")
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")
        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            print("⚠️ 데이터 파일이 손상되어 기본 퀴즈로 복구합니다.")
            self.backup_broken_file()
            self.quizzes = get_default_quizzes()
            self.best_score = None

    def backup_broken_file(self):
        """손상된 state.json을 덮어쓰기 전에 state.json.bak으로 복사해 둔다."""
        try:
            shutil.copy(STATE_FILE, BACKUP_FILE)
            print("💾 손상된 파일을 state.json.bak으로 백업했습니다.")
        except OSError:
            print("⚠️ 손상된 파일을 백업하지 못했습니다.")

    def save(self):
        """퀴즈와 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        temp_file = STATE_FILE + ".tmp"
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            os.replace(temp_file, STATE_FILE)   # 다 쓴 뒤에 한 번에 바꿔치기
        except OSError:
            print("⚠️ 파일 저장 중 오류가 발생했습니다.")

    def show_menu(self):
        """메뉴를 화면에 출력한다."""
        print()
        print("=" * 40)
        print("        🎯 대한민국 상식 퀴즈 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def get_number(self, prompt, min_value, max_value):
        """min~max 사이의 숫자를 입력받을 때까지 반복한다."""
        while True:
            text = input(prompt).strip()   # 앞뒤 공백 제거

            if text == "":
                print("⚠️ 입력이 비어 있습니다. 숫자를 입력하세요.")
                continue

            try:
                number = int(text)
            except ValueError:
                print(f"⚠️ 숫자가 아닙니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if number < min_value or number > max_value:
                print(f"⚠️ 범위를 벗어났습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return number

    def play_quiz(self):
        """퀴즈를 순서대로 출제하고 결과를 보여준다."""
        if len(self.quizzes) == 0:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")


        quizzes = self.quizzes[:]      # 원본 목록을 복사
        random.shuffle(quizzes)        # 복사본의 순서를 무작위로 섞기
        for number, quiz in enumerate(quizzes, start=1):
            quiz.display(number)
            user_answer = self.get_number("정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score = int(correct / total * 100)
        print()
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            self.save()
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

    def get_text(self, prompt):
        """빈 문자열이 아닌 글자를 입력받을 때까지 반복한다."""
        while True:
            text = input(prompt).strip()
            if text == "":
                print("⚠️ 입력이 비어 있습니다. 다시 입력하세요.")
                continue
            return text

    def add_quiz(self):
        """사용자에게 문제, 선택지 4개, 정답을 입력받아 퀴즈를 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = self.get_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = self.get_text(f"선택지 {i}: ")
            choices.append(choice)

        answer = self.get_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        print("\n✅ 퀴즈가 추가되었습니다!")
        self.save()

    def show_quizzes(self):
        """등록된 퀴즈의 문제 목록을 보여준다."""
        if len(self.quizzes) == 0:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40) 

    def show_score(self):
        """최고 점수를 보여준다."""
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어보세요!")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점")

    def run(self):
        """프로그램의 메인 반복 흐름"""
        while True:
            self.show_menu()
            choice = self.get_number("선택: ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quizzes()
            elif choice == 4:
                self.show_score()
            else:
                self.save()
                print("👋 프로그램을 종료합니다.")
                break
            
def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되었습니다. 저장 후 종료합니다.")
        game.save()


if __name__ == "__main__":
    main()