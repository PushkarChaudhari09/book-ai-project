import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(context, question):
    try:
        from openai import OpenAI
        import os
        from dotenv import load_dotenv

        load_dotenv()

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful book assistant."},
                {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", e)

        # ✅ FALLBACK (ALWAYS WORKS)
        return f"📚 Based on available books:\n\n{context[:500]}"