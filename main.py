from tqdm import tqdm

from src.llm_openai import LLM
from src.utils import (
    get_linkedin_url,
    get_all_jobs_links,
    get_structured_html,
    get_job_info,
    summarize_skills,
    compose_and_save_markdown_text
)


FIRST_N_JOBS_TO_PROCESS = 3

GEOID_OPTIONS = {
    "Krakow"  : "103263110",
    "Warsaw"  : "105076658",
    "Poland"  : "105072130",
    "Tampere" : "102656323",
    "Helsinki": "106591199",
    "Finland" : "100456013",
    "Tokyo"   : "103925994",
    "Japan"   : "101355337",
    "Milano"  : "100881402",
    "Italy"   : "103350119",
    "London"  : "90009496",
    "UK"      : "101165590",
    "Oslo"    : "105719246",
    "Bergen"  : "100492051",
    "Norway"  : "103819153",
    "Sweden"  : "105117694",
    "Germany" : "101282230",
    "France"  : "105015875",
    "Spain"   : "105646813",
}


def main():

    keyword = "Software Engineer, C++"
    city = "Tokyo"

    llm = LLM()

    linkedin_url = get_linkedin_url(geoid=GEOID_OPTIONS[city], keyword=keyword)
    structured_html = get_structured_html(linkedin_url)
    collection_of_jobs_urls = get_all_jobs_links(structured_html=structured_html)
    print(f"Found {len(collection_of_jobs_urls)} jobs in {city} with keyword `{keyword}`.")

    collection_of_jobs_info = []
    for job_url in tqdm(collection_of_jobs_urls[0:FIRST_N_JOBS_TO_PROCESS]):
        job_info = get_job_info(url=job_url, llm=llm)
        collection_of_jobs_info.append(job_info)

    summarized_skills = summarize_skills(collection_of_jobs_info, llm)

    compose_and_save_markdown_text(
        city=city,
        keyword=keyword,
        collection=collection_of_jobs_info,
        summarized_skills=summarized_skills
    )


if __name__ == "__main__":
    main()