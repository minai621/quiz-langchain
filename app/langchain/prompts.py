from langchain_core.prompts import PromptTemplate

SUMMARY_TEMPLATE = """Analyze and summarize the following text at a graduate-level academic standard.
Focus on maintaining technical depth while organizing key concepts.

Text: {text}

Your response should be in English.

Format your response as follows:
1. Core Technical Concepts & Terminology
2. Theoretical Framework
3. Technical Implementation Details
4. Advanced Applications
5. Related Research & Future Directions"""


QUIZ_TEMPLATE = """Generate advanced-level academic quizzes based on the provided text about multidimensional arrays.
Avoid any overlap with existing quizzes and ensure high academic rigor.

Text: {text}
Existing Quizzes:
{existing_quizzes}

Requirements:
1. Create 10 undergraduate-level questions following these criteria:
   - 4 Multiple Choice (1 HIGH, 2 MEDIUM, 1 LOW complexity)
   - 3 Short Answer (1 HIGH, 1 MEDIUM, 1 LOW complexity)
   - 3 True/False (1 HIGH, 1 MEDIUM, 1 LOW complexity)

2. For Multiple Choice:
   - Focus on undergraduate-level computer science concepts
   - Include practical implementation scenarios
   - All options should be plausible
   - Minimum 4 options per question
   - Use natural Korean question endings (예: ~는 무엇입니까?, ~하는 이유는?, ~설명하시오.)
   
3. For Short Answer:
   - Questions should require concise, technical answers
   - Include both Korean and English versions of acceptable answers
   - Example:
     QUESTION: 다차원 배열의 메모리 할당 방식을 설명하시오.
     ANSWER: Contiguous memory allocation
     ACCEPTABLE_VARIATIONS: contiguous memory allocation | 연속 메모리 할당 | 연속 할당

4. For True/False:
   - Focus on common misconceptions and technical concepts
   - Use clear, natural Korean question endings
   - Include technical explanation for the answer
   - Example:
     LEVEL: MEDIUM
     TYPE: TRUE_FALSE
     QUESTION: 다차원 배열의 모든 차원은 반드시 동일한 크기를 가져야 한다.
     OPTIONS: True | False
     ANSWER: False
     EXPLANATION: 다차원 배열의 각 차원은 서로 다른 크기를 가질 수 있습니다.

Example Questions:
- "다차원 배열의 시간 복잡도를 개선하기 위한 최적화 방법은 무엇입니까?"
- "희소 행렬(sparse matrix)을 다차원 배열로 구현할 때의 단점을 설명하시오."
- "다차원 배열의 캐시 지역성(cache locality)을 향상시키는 방법은 무엇입니까?"

Example Question Format:
---
LEVEL: HIGH
TYPE: SHORT_ANSWER
QUESTION: 다차원 배열의 값을 효율적으로 저장하기 위해 사용되는 프로그래밍 기법은 무엇일까요?
ANSWER: dynamic programming
ACCEPTABLE_VARIATIONS: dynamic programming | 동적 프로그래밍 | DP | dp
---

Format each question as follows:
---
LEVEL: [HIGH/MEDIUM]
TYPE: [MULTIPLE_CHOICE/SHORT_ANSWER]
QUESTION: [Question text in Korean ending with 일까요?]
OPTIONS: [For multiple choice, separate with |]
ANSWER: [Correct answer in English for technical terms]
ACCEPTABLE_VARIATIONS: [Alternative acceptable answers, separated by |]
---

Example True/False Question:
---
LEVEL: MEDIUM
TYPE: TRUE_FALSE
QUESTION: 모든 다차원 배열은 시각적으로 초직사각형으로 표현될 수 있다.
OPTIONS: True | False
ANSWER: False
---
LEVEL: HIGH
TYPE: TRUE_FALSE
QUESTION: 다차원 배열에서 행 우선 순회(row-major traversal)가 열 우선 순회(column-major traversal)보다 캐시 효율성이 항상 더 높다.
OPTIONS: True | False
ANSWER: False
EXPLANATION: 캐시 효율성은 메모리 레이아웃과 하드웨어 아키텍처에 따라 달라지며, 특히 FORTRAN과 같은 열 우선 저장 방식을 사용하는 언어에서는 column-major traversal이 더 효율적일 수 있다.
---
LEVEL: MEDIUM
TYPE: TRUE_FALSE
QUESTION: 다차원 배열에서 동적 메모리 할당을 사용할 경우, 배열의 연속성(contiguity)이 보장된다.
OPTIONS: True | False
ANSWER: False
EXPLANATION: 동적으로 할당된 다차원 배열은 각 차원이 서로 다른 메모리 영역에 할당될 수 있어 메모리 연속성이 보장되지 않으며, 이는 캐시 성능에 영향을 미칠 수 있다.
---
LEVEL: LOW
TYPE: TRUE_FALSE
QUESTION: 다차원 배열의 메모리 접근 패턴이 시간적 지역성(temporal locality)과 공간적 지역성(spatial locality)에 동시에 영향을 미친다.
OPTIONS: True | False
ANSWER: True
EXPLANATION: 배열 요소 접근 패턴은 캐시의 시간적 지역성(동일 데이터의 재사용)과 공간적 지역성(인접 데이터 사용)에 모두 영향을 미치며, 이는 프로그램의 성능을 좌우하는 중요한 요소이다.
---

Example Technical Question:
---
LEVEL: HIGH
TYPE: MULTIPLE_CHOICE
QUESTION: REST API와 GraphQL의 핵심적인 차이점은 무엇인가요?
OPTIONS: REST API는 고정된 엔드포인트 구조를 따르지만 | GraphQL은 유연한 데이터 쿼리를 지원합니다 | REST API는 여러 개의 엔드포인트가 필요합니다 | GraphQL은 네트워크 부하를 증가시킵니다
ANSWER: GraphQL은 유연한 데이터 쿼리를 지원합니다
---

Example General Question:
---
LEVEL: HIGH
TYPE: MULTIPLE_CHOICE
QUESTION: 르네상스 시대 과학 발전에 가장 큰 영향을 미친 요인은 무엇인가요?
OPTIONS: 인문주의적 사고방식 | 종교적 교리의 약화 | 봉건제도의 붕괴 | 상업의 발달
ANSWER: 인문주의적 사고방식
---
"""

SUMMARY_PROMPT = PromptTemplate(template=SUMMARY_TEMPLATE, input_variables=["text"])
QUIZ_PROMPT = PromptTemplate(template=QUIZ_TEMPLATE, input_variables=["text", "existing_quizzes"])
