from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests

from src.llm_openai import LLM


def get_linkedin_url(geoid: str, keyword: str) -> str:
    return (
        f"https://www.linkedin.com/jobs/search/"
        f"?geoId={geoid}&keywords={keyword}"
        f"&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true"
    )


def get_all_jobs_links(structured_html: BeautifulSoup) -> list[str]:
    # Find all tags with the attribute `data-occludable-job-id`
    links = structured_html.find_all("a", class_="base-card__full-link")
    collection_of_jobs_urls = [link.get("href") for link in links if link.get("href")]
    return collection_of_jobs_urls


def get_structured_html(url: str) -> BeautifulSoup:
    simulated_chrome_on_windows = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
    headers = {"User-Agent": simulated_chrome_on_windows}
    raw_response = requests.get(url, headers=headers)
    structured_response = BeautifulSoup(raw_response.text, "html.parser")
    return structured_response


@dataclass
class JobPost:
    title: str
    url: str
    job_description: str
    detected_post_language: str
    required_skills: str
    required_languages: list[str]
    preferable_languages: list[str]


def compose_and_save_markdown_text(city: str, keyword: str, collection: list[JobPost], summarized_skills: str) -> None:
    overall_text = f"# Search in {city}, keyword `{keyword}`\n\n## Available Jobs\n\n"
    for job in collection:
        overall_text += f"{job.title}<br>\n{job.url}<br>\n"
        overall_text += f"Post written in: {job.detected_post_language}<br>\n"
        for language in job.required_languages:
            overall_text += f"Required language: {language}<br>\n"
        for language in job.preferable_languages:
            overall_text += f"Preferable language: {language}<br>\n"
        overall_text += "\n\n"

    overall_text += f"\n## Summarized Skills\n{summarized_skills}\n\n"
    overall_text += f"\n## Details\n\n"

    for job in collection:
        overall_text += f"{job.title}<br>\n{job.url}<br>\n"
        overall_text += f"Post written in: {job.detected_post_language}<br>\n"
        for language in job.required_languages:
            overall_text += f"Required language: {language}<br>\n"
        for language in job.preferable_languages:
            overall_text += f"Preferable language: {language}<br>\n"
        overall_text += "\n"
        overall_text += (
            f"<details>\n\n"
            f"   <summary>Detailed Required Skills</summary>\n\n"
            f"   {job.required_skills}\n\n"
            f"\n</details>\n\n"
        )

    with open("output.md", "w") as file:
        file.write(overall_text)


def get_job_info(url: str, llm: LLM) -> JobPost:
    structured_html_job = get_structured_html(url)
    title = structured_html_job.find("h1", class_="topcard__title").get_text(strip=True)  # top-card-layout__title
    job_description = structured_html_job.find("div", class_="show-more-less-html__markup").get_text(strip=True)
    extracted_job_post_language = llm.detect_text_language(content=job_description).capitalize()
    extracted_skills = llm.extract_skills(content=job_description)
    extracted_language_requirements = llm.extract_languages_requirements(content=job_description)
    return JobPost(
        title=title,
        url=url,
        job_description=job_description,
        detected_post_language=extracted_job_post_language,
        required_skills=extracted_skills,
        required_languages=extracted_language_requirements.required_languages,
        preferable_languages=extracted_language_requirements.preferable_languages,
    )


def summarize_skills(collection: list[JobPost], llm: LLM) -> str:
    all_skills = ""
    for job in collection:
        all_skills += f"{job.required_skills}\n\n"
    summarized_skills = llm.summarize_collection_of_skills(all_skills)
    return summarized_skills
