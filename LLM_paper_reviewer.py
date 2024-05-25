import openai, os


class LLM_Reviewer:
    def __init__(self, openai_api_key=''):
        self.openai_client = openai.OpenAI(api_key=openai_api_key)

    def review_indirectly(self, pdf_text=''):
        message = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI research scientist, enjoys reading new papers. "
                                              "You are also known as famous paper reviewer for an outstanding "
                                              "critical thinking."},
                {"role": "user", "content":
                    "I will give you reviews of paper, published in prominent international conference."
                    "Summarize the paper in 4 sections, which corresponds to 4 different "
                    "perspectives, which are 'problem definition', 'contribution', "
                    "'importance of contribution or approaches', 'weakness or doubts.'"
                    f"Here it goes\n'{pdf_text}'"}]
        )

        return message.choices[0].message.content
