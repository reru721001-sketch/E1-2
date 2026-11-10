from quiz_data import get_default_quizzes

class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스"""

    def __init__(self):
        self.quizzes = get_default_quizzes()   # 퀴즈 목록
        self.best_score = None                 # 최고 점수 (None = 아직 안 풀어봄)

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

    def run(self):
        """프로그램의 메인 반복 흐름"""
        while True:
            self.show_menu()
            choice = self.get_number("선택: ", 1, 5)

            if choice == 5:
                print("👋 프로그램을 종료합니다.")
                break
            else:
                print("🚧 아직 준비 중인 기능입니다.")


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️ 입력이 중단되었습니다. 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()