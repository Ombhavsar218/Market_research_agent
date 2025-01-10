# -*- coding: utf-8 -*-
"""Source code Without Gradio.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hmut6BM0sPq_CQcxaNqYPcjvcH0dYeF6
"""

import requests
import os


os.environ["SERP_API_KEY"] = "Your_Serp_API_key"
SERP_API_KEY = os.getenv("SERP_API_KEY")


def serpapi_search(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_search_results(query):
    results = serpapi_search(query)
    search_results = results.get("organic_results", [])

    if not search_results:
        return "No results found."

    search_info = []
    for result in search_results:
        title = result.get('title', 'No title')
        link = result.get('link', 'No link')
        snippet = result.get('snippet', 'No description available')
        search_info.append(f"{title}: {snippet} \nLink: {link}")

    return "\n\n".join(search_info)


def search_company_industry(company_name):
    query = f"{company_name} industry or business sector"
    results = get_search_results(query)

    if not results:
        return "Industry not found"


    return results.split("\n")[0]


def search_for_datasets(query):
    kaggle_query = f"{query} site:kaggle.com"
    huggingface_query = f"{query} site:huggingface.co"
    github_query = f"{query} site:github.com"

    kaggle_results = get_search_results(kaggle_query)
    huggingface_results = get_search_results(huggingface_query)
    github_results = get_search_results(github_query)

    dataset_results = f"### Relevant Datasets\nKaggle Datasets:\n{kaggle_results}\n\nHuggingFace Datasets:\n{huggingface_results}\n\nGitHub Datasets:\n{github_results}"

    return dataset_results

class MarketResearchCrew:
    def __init__(self, company_name=None):
        self.company_name = company_name
        self.industry = self.auto_determine_industry()

    def auto_determine_industry(self):
        print(f"Automatically determining industry for: {self.company_name}")
        return search_company_industry(self.company_name)

    def research_agent(self):
        query = f"{self.company_name} company overview" if self.company_name else f"{self.industry} industry trends"
        results = get_search_results(query)
        return f"### Research Agent Results\n{results}"

    def market_analysis_agent(self):
        query = f"{self.industry} industry AI ML automation trends"
        results = get_search_results(query)
        return f"### Market Analysis Agent Results\n{results}"

    def use_case_generation_agent(self):
        query1 = f"AI ML automation use cases in {self.industry}, case studies, and industry applications"
        results1 = get_search_results(query1)

        query2 = f"Top AI ML applications in {self.company_name}"
        results2 = get_search_results(query2)


        def format_results_as_list(results):
            use_cases = results.split("\n\n")
            formatted_list = "\n".join([f"{i + 1}. {case}" for i, case in enumerate(use_cases) if case.strip()])
            return formatted_list

        formatted_results1 = format_results_as_list(results1)
        formatted_results2 = format_results_as_list(results2)

        full_results = f"#### Industry Use Cases\n{formatted_results1}\n\n#### Company Use Cases\n{formatted_results2}"
        return f"### Expanded Use Case Generation Agent Results\n{full_results}"

    def dataset_agent(self):
        dataset_results = search_for_datasets(self.industry)
        return dataset_results

    def run_crew(self):
        research_report = self.research_agent()
        market_analysis_report = self.market_analysis_agent()
        use_case_report = self.use_case_generation_agent()
        dataset_report = self.dataset_agent()

        company = self.company_name or "N/A"
        industry = self.industry.split(":")[-1].strip() if ":" in self.industry else self.industry
        title = f"**Market Research Report**\n\n**Company:** {company}\n**Industry:** {industry}\n\n"

        full_report = f"{title}{research_report}\n\n{market_analysis_report}\n\n{use_case_report}\n\n{dataset_report}"

        with open("market_research_report.md", "w") as file:
            file.write(full_report)

        return full_report

if __name__ == "__main__":
    crew = MarketResearchCrew(company_name="Zomato")
    result = crew.run_crew()

    print(result)


