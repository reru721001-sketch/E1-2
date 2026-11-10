# 🎯 대한민국 상식 퀴즈 게임

## 1. 프로젝트 개요
터미널에서 실행하는 Python 콘솔 퀴즈 게임입니다.
메뉴에서 번호를 선택해 퀴즈를 풀고, 새 퀴즈를 추가하고, 목록과 최고 점수를 확인할 수 있습니다.
퀴즈와 최고 점수는 `state.json` 파일에 저장되어 프로그램을 다시 실행해도 유지됩니다.

## 2. 개발 환경
| 구분 | 내용 |
|---|---|
| OS | Windows 11 |
| Python | 3.14.7 (3.10 이상 필요, 표준 라이브러리만 사용) |
| Git | 2.56.0 |
| 에디터 / 터미널 | VSCode / Windows Terminal (cmd) |

## 3. 퀴즈 주제 선정 이유
주제는 **대한민국 기초 상식**으로 정했습니다.
이번 미션의 목표는 퀴즈 내용보다 Python 문법, 클래스 설계, 파일 저장, Git 사용법을 직접 익히는 것이라고 생각했습니다.
그래서 누구나 알 만하고 정답을 확인하기 쉬운 주제를 골라, 문제를 만드는 시간은 줄이고 기능 구현에 더 집중했습니다.

## 4. 실행 방법
```bash
git clone https://github.com/reru721001-sketch/E1-2.git
cd E1-2
python main.py
```
(macOS / Linux에서는 `python3 main.py`)

## 5. 기능 목록
| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 등록된 퀴즈를 **랜덤 순서**로 출제하고 정답/오답과 최종 점수(100점 만점)를 보여줍니다. 최고 점수를 넘으면 갱신합니다. |
| 2 | 퀴즈 추가 | 문제, 선택지 4개, 정답 번호를 입력받아 새 퀴즈를 등록하고 파일에 저장합니다. |
| 3 | 퀴즈 목록 | 등록된 퀴즈의 문제 목록을 번호와 함께 보여줍니다. |
| 4 | 점수 확인 | 최고 점수를 보여줍니다. 아직 풀지 않았다면 안내 메시지를 출력합니다. |
| 5 | 종료 | 데이터를 저장하고 프로그램을 종료합니다. |

### 입력 및 예외 처리
- 입력값의 앞뒤 공백을 제거한 뒤 처리합니다.
- 빈 입력, 숫자가 아닌 입력(`abc`), 범위 밖 숫자(메뉴 `9`, 정답 `0`)는 안내 후 다시 입력받습니다.
- `Ctrl+C`(KeyboardInterrupt)나 입력 종료(EOFError)가 발생하면 저장 후 안전하게 종료합니다.
- `state.json`이 없으면 기본 퀴즈 5개로 시작하고, 손상되었으면 안내 후 기본 퀴즈로 복구합니다.

### 보너스
- 랜덤 출제: `random.shuffle()`로 출제 순서를 섞습니다. (원본 목록 순서는 유지)

## 6. 파일 구조
```
E1-2/
├── main.py        # 프로그램 시작점, QuizGame 클래스 (메뉴, 풀기, 추가, 목록, 점수, 저장/불러오기)
├── quiz.py        # Quiz 클래스 (퀴즈 한 문제: 출력, 정답 확인, dict 변환)
├── quiz_data.py   # 기본 퀴즈 5개를 만드는 함수
├── state.json     # 퀴즈 목록과 최고 점수 저장 파일
├── README.md      # 프로젝트 설명서
├── .gitignore     # Git이 무시할 파일 목록
└── docs/
    └── screenshots/  # 실행 화면 스크린샷
```

### 클래스 구조
| 클래스 | 역할 | 주요 메서드 |
|---|---|---|
| `Quiz` | 퀴즈 한 문제 | `display()`, `is_correct()`, `to_dict()`, `from_dict()` |
| `QuizGame` | 게임 전체 관리 | `run()`, `play_quiz()`, `add_quiz()`, `show_quizzes()`, `show_score()`, `load()`, `save()`, `backup_broken_file()` |

설계 이유는 [11. 설계 설명](#11-설계-설명)에 정리했습니다.

## 7. 데이터 파일 설명 (`state.json`)
- **경로**: 프로젝트 루트 (`main.py`와 같은 폴더)
- **역할**: 퀴즈 목록과 최고 점수를 저장해, 프로그램을 다시 실행해도 데이터가 유지되게 합니다.
- **인코딩**: UTF-8 (한글이 그대로 저장되도록 `ensure_ascii=False` 사용)
- **저장 시점**: 퀴즈 추가 시, 최고 점수 갱신 시, 프로그램 종료 시(Ctrl+C 포함)

### 스키마
| 키 | 자료형 | 설명 |
|---|---|---|
| `quizzes` | list | 퀴즈 목록 |
| `quizzes[].question` | str | 문제 |
| `quizzes[].choices` | list[str] | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `best_score` | int 또는 null | 최고 점수 (100점 만점, 아직 풀지 않았으면 null) |

### 예시
```json
{
    "quizzes": [
        {
            "question": "대한민국의 수도는?",
            "choices": ["부산", "서울", "대구", "인천"],
            "answer": 2
        }
    ],
    "best_score": 80
}
```
> clone한 저장소에서 추가한 문장입니다. (clone/pull 실습)


## 8. 실행 화면 (Windows 11, Windows Terminal)

### 개발 환경
![개발 환경](docs/screenshots/env.png)

### 메뉴
![메뉴](docs/screenshots/menu.png)

### 퀴즈 추가
![퀴즈 추가](docs/screenshots/add_quiz.png)

### 퀴즈 목록
다시 실행해도 추가한 퀴즈가 유지됩니다.

![퀴즈 목록](docs/screenshots/list.png)

### 퀴즈 풀기 (랜덤 출제)
![퀴즈 풀기](docs/screenshots/play.png)

### 최고 점수
![최고 점수](docs/screenshots/score.png)

### Git 커밋 기록
![git log](docs/screenshots/git_log.png)

## 9. Git 작업 기록
- 저장소: https://github.com/reru721001-sketch/E1-2
- 커밋 수: 이 섹션 작성 시점 기준 **16개** (일반 커밋 15개 + 병합 커밋 1개), 이후 README 보강 커밋 추가
- 브랜치: `main`, `feature/play-quiz` (퀴즈 풀기 기능을 별도 브랜치에서 개발 후 `--no-ff`로 병합)
- 확인 명령: `git log --oneline --graph`, `git rev-list --count HEAD`

### 커밋 그래프 (`git log --oneline --graph`)
```
* c321aab Feat: 손상 파일 백업(state.json.bak) 및 안전한 저장 구현
* 07f99b0 Docs: 실행 화면 스크린샷 추가 및 README에 첨부
* e0a7f03 Docs: clone 실습용 README 문구 추가
* 4cbc35a Docs: README 작성 (개요, 개발 환경, 실행 방법, 기능, 파일 구조, state.json 설명)
* 6c13c09 Chore: 기본 상태의 state.json 추가
* 1b650e4 Feat: 퀴즈 랜덤 출제 기능 추가 (보너스)
* c4ab24c Feat: state.json 저장/불러오기 및 손상 파일 복구 구현
* 95f1daf Feat: 최고 점수 갱신 및 점수 확인 기능 구현
* 35c0224 Feat: 퀴즈 목록 보기 기능 구현
* c2a5aef Feat: 퀴즈 추가 기능 구현 (문제, 선택지, 정답 입력 검증)
*   bc9620e Merge: feature/play-quiz 브랜치 병합
|\
| * 52fe529 Feat: 퀴즈 풀기 기능 구현 (출제, 채점, 결과 표시)
|/
* dc85e65 Feat: 대한민국 상식 기본 퀴즈 5개 추가
* 7c59aa3 Feat: Quiz 클래스 구현 (출력, 정답 확인, dict 변환)
* 006fb59 Feat: 메뉴 화면 및 숫자 입력 검증 구현
* bf3bb3d Chore: 프로젝트 초기 설정 (.gitignore, README 추가)
```

### 브랜치 생성 및 병합 과정
그래프에서 `|/`는 브랜치가 갈라진 지점, `|\`는 다시 합쳐진 지점입니다.
`dc85e65`(기본 퀴즈 추가) 이후 `feature/play-quiz` 브랜치를 만들어 `52fe529`(퀴즈 풀기)를 개발했고, `bc9620e`에서 `main`에 병합했습니다.

```bash
git checkout -b feature/play-quiz        # 브랜치 생성 및 이동
git add main.py
git commit -m "Feat: 퀴즈 풀기 기능 구현 (출제, 채점, 결과 표시)"
git push -u origin feature/play-quiz     # 브랜치를 원격에 업로드
git checkout main                        # main으로 이동 (이 시점의 main에는 퀴즈 풀기 기능이 없음)
git merge --no-ff feature/play-quiz -m "Merge: feature/play-quiz 브랜치 병합"
git push
```
`--no-ff` 옵션을 사용해 병합 커밋을 남겼기 때문에, 그래프에서 브랜치 작업 기록이 구분되어 보입니다.

### clone / pull 실습
```bash
git clone https://github.com/reru721001-sketch/E1-2.git E1-2-clone   # 다른 폴더로 복제
cd E1-2-clone
# README.md 끝에 문장 추가
git add README.md
git commit -m "Docs: clone 실습용 README 문구 추가"
git push
cd ..\E1-2
git pull                                  # Fast-forward로 e0a7f03 반영
```
`7. 데이터 파일 설명` 끝의 인용문(`> clone한 저장소에서 추가한 문장입니다.`)이 이 실습으로 추가된 문장입니다.

### 사용한 Git 명령
| 명령 | 사용한 곳 |
|---|---|
| `git init` | 저장소 초기화 |
| `git add` / `git commit` | 모든 기능 단위 커밋 |
| `git push` | 매 커밋 후 원격 반영, 브랜치 업로드 (`-u`) |
| `git checkout` | 브랜치 생성(`-b`) 및 `main` 복귀 |
| `git merge` | `feature/play-quiz` 병합 |
| `git clone` | `E1-2-clone` 폴더로 복제 |
| `git pull` | clone 폴더에서 push한 변경을 원래 폴더로 반영 |

## 10. 커밋 규칙
### 커밋 단위
- **기능 하나 = 커밋 하나**: 메뉴, Quiz 클래스, 기본 데이터, 풀기, 추가, 목록, 점수, 저장/불러오기, 랜덤 출제를 각각 따로 커밋했습니다.
- 커밋하기 전에 `python main.py`로 해당 기능이 동작하는지 확인합니다. (실행되지 않는 상태로 커밋하지 않음)
- 문서 변경과 코드 변경은 커밋을 나눕니다.

### 메시지 형식
```
<타입>: <무엇을 했는지 한국어로 요약> (필요하면 괄호 안에 세부 내용)
```

| 타입 | 의미 | 예시 |
|---|---|---|
| `Feat` | 새 기능 추가 | `Feat: 퀴즈 추가 기능 구현 (문제, 선택지, 정답 입력 검증)` |
| `Docs` | 문서 수정 | `Docs: README 작성 (개요, 실행 방법, 기능, 파일 구조, state.json 설명)` |
| `Chore` | 설정, 데이터 정리 등 기능 외 작업 | `Chore: 기본 상태의 state.json 추가` |
| `Merge` | 브랜치 병합 | `Merge: feature/play-quiz 브랜치 병합` |
| `Fix` | 버그 수정 (필요 시 사용) | `Fix: 정답 번호 범위 검사 오류 수정` |

## 11. 설계 설명
### 왜 클래스를 사용했나 (추상화와 재사용성)
- **추상화**: `Quiz` 클래스는 "퀴즈 한 문제"라는 개념을 문제·선택지·정답 3개 속성과 `display()`, `is_correct()` 같은 행동으로 묶은 것입니다. 게임 쪽 코드는 `quiz.is_correct(답)`만 호출하면 되고, 정답을 어떻게 비교하는지는 몰라도 됩니다.
- **재사용성**: 같은 `Quiz` 설계도로 기본 퀴즈 5개(`quiz_data.py`)와 사용자가 추가한 퀴즈(`add_quiz()`)를 똑같이 만들고, `to_dict()` / `from_dict()`로 저장·불러오기도 같은 방식으로 처리합니다. 입력 검증 `get_number()`도 메뉴 선택(1~5), 정답 입력(1~4), 퀴즈 추가 시 정답 번호(1~4)의 세 곳에서 재사용합니다.
- **역할 분리**: `Quiz`는 "문제 한 개", `QuizGame`은 "게임 진행과 데이터 관리"만 맡습니다. 문제 형식을 바꿀 때는 `Quiz`만, 메뉴 흐름을 바꿀 때는 `QuizGame`만 수정하면 됩니다.

### 로직 분리
| 영역 | 메서드 | 분리한 이유 |
|---|---|---|
| 입력 검증 | `get_number()`, `get_text()` | 공백 제거·빈 입력·숫자 변환·범위 검사를 한 곳에 모아, 여러 기능에서 같은 규칙을 재사용하고 수정도 한 번에 할 수 있게 했습니다. |
| 게임 진행 | `run()`, `play_quiz()`, `add_quiz()`, `show_quizzes()`, `show_score()` | 메뉴 번호 하나에 메서드 하나를 대응시켜, 기능별로 독립적으로 이해하고 테스트할 수 있게 했습니다. |
| 데이터 입출력 | `load()`, `save()`, `backup_broken_file()` | 파일 형식(JSON)이나 저장 위치가 바뀌어도 게임 진행 코드는 건드리지 않도록 저장 관련 코드를 모았습니다. |

### 실행 흐름 (로드 → 사용 → 저장)
```
python main.py
   │
   ▼
main() ─▶ QuizGame() ─▶ __init__() ─▶ load()
                                        ├─ 파일 없음 → 기본 퀴즈 5개
                                        ├─ 정상      → state.json 내용
                                        └─ 손상      → state.json.bak 백업 후 기본 퀴즈 5개
   │
   ▼
run() 메뉴 반복
   ├─ 1 풀기 ── 최고 점수 갱신 시 ─▶ save()
   ├─ 2 추가 ── 추가 직후 ─────────▶ save()
   ├─ 3 목록 / 4 점수 (조회만, 저장 없음)
   └─ 5 종료 ─────────────────────▶ save() → 종료
   
Ctrl+C / EOF ─▶ main()의 except ─▶ save() → 종료
```

### 요구사항이 바뀌면 수정할 위치
| 바뀌는 요구사항 | 수정할 파일 / 메서드 |
|---|---|
| 점수 계산 방식 (예: 문제당 배점, 감점) | `main.py` → `play_quiz()`의 `score = ...` 줄 |
| 퀴즈 형식 (예: 선택지 개수, 힌트 추가) | `quiz.py` → `Quiz.__init__()`, `display()`, `to_dict()`, `from_dict()` / `main.py` → `add_quiz()` |
| 기본 퀴즈 내용 | `quiz_data.py` → `get_default_quizzes()` |
| 저장 형식이나 경로 (예: 다른 파일, DB) | `main.py` → `STATE_FILE`, `load()`, `save()` |
| 메뉴 항목 추가 | `main.py` → `show_menu()`, `run()`, `get_number()`의 범위 값 |
| 입력 규칙 (예: 허용 범위, 안내 문구) | `main.py` → `get_number()`, `get_text()` |
