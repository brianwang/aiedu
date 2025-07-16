from app.services.question_generator import QuestionGenerator
from database import get_db
import asyncio

db = next(get_db())
gen = QuestionGenerator(db)
result = asyncio.run(
    gen.generate_questions_by_tags_and_skills(['数学'], ['四则运算'],
                                              count_per_skill=2))
print('生成题目数:', result)
