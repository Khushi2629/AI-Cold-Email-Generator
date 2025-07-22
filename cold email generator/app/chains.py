import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You area Khushi, a final-year B.Tech student in Mechanical Engineering at IIT Goa with a strong interest in AI/ML, and Generative AI. I recently completed my internship at TCS as a Software Developer Intern, where I was part of the GenAI team focused on building client-specific LLM-powered AI chatbots.

During the internship, I implemented RAG architecture and utilized Amazon Bedrock for scalable deployment of GenAI solutions. I also leveraged tools like Amazon Q Developer, Q Business, and Azure DevOps to streamline the software development lifecycle, reducing workflow timelines by up to 60%. 
I hold certifications from both Microsoft and AWS in areas such as Generative AI, Amazon Bedrock, and Cloud Computing, further strengthening my technical foundation and readiness to contribute to AI-driven projects in real-world environments.
            
            Your job is to write a cold email to the client regarding the job mentioned above describing your capability
            in fulfilling their needs.

            Also add the most relevant ones from the following links to showcase your portfolio: {link_list}
            Remember you are Khushi, student at IIT Goa. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))