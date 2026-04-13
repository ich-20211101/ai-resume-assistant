import os # .env에 넣어둔 API 키를 꺼내오는 용도
import json # JSON 문자열을 파이썬 딕셔너리(dict)로 바꾸거나, 반대로 바꾸는 모듈
from pathlib import Path
from groq import AsyncGroq # 비동기 방식으로 AI API를 호출
from dotenv import load_dotenv # .env 파일에 저장된 환경변수를 코드에서 읽게 해주는 함수

# .env 파일을 읽어서 환경변수로 등록
load_dotenv()

# Groq 클라이언트 생성
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

RULES_PATH = Path(__file__).parent.parent / "data" / "rules.txt"

def load_rules() -> str:
    if RULES_PATH.exists():
        return RULES_PATH.read_text(encoding="utf-8")
    return ""


SYSTEM_PROMPT = """You are an expert resume coach and career strategist.
Your job is to tailor resumes to specific job descriptions.

CRITICAL: You MUST return ALL four fields in your JSON response: keywords, summary, skills, and experience.
Returning only keywords is incorrect. You must always include summary, skills, and experience as well.

Follow these rules strictly:
{rules}

Always respond in valid JSON with this exact structure:
{{
  "keywords": {{
    "matched": ["keyword1", "keyword2"],
    "missing": ["keyword3", "keyword4"]
  }},
  "summary": "Tailored professional summary here...",
  "skills": ["Skill 1", "Skill 2", "Skill 3"],
  "experience": [
    {{
      "company": "Company Name",
      "title": "Job Title",
      "bullets": [
        "Tailored bullet point 1",
        "Tailored bullet point 2"
      ]
    }}
  ]
}}

Do not include any text outside the JSON object.
Do not return partial results. Always return all four fields."""


async def tailor_resume(
    job_description: str,
    resume: str,
    instruction: str = "",
) -> dict:
    rules = load_rules()
    system = SYSTEM_PROMPT.format(rules=rules)

    user_message = f"""## Job Description
    {job_description}

    ## Resume
    {resume}

    ## Additional Instructions
    {instruction if instruction else "None"}

    IMPORTANT: If the additional instructions specify a language (e.g. Korean), 
    you MUST write summary and experience bullets entirely in that language.

    Tailor this resume to the job description following all rules."""

    # 실제 AI 호출
    response = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[ # AI에게 전달하는 대화 내용
            {"role": "system", "content": system}, # system = 역할 + 규칙 + 출력 형식
            {"role": "user", "content": user_message}, # user_message = 실제 입력 데이터
        ],
        response_format={"type": "json_object"},
        temperature=0.4, # 응답의 창의성 정도
        max_tokens=4000,
    )

    # 응답 내용 꺼내기
    content = response.choices[0].message.content

    # json으로 파싱해서 반환
    return json.loads(content)