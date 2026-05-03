import requests
from bs4 import BeautifulSoup
import json
import time

# Add your specific links here
program_links = [
    "https://www.superior.edu.pk/faculties/faculty-of-engineering-and-technology/bsc-mechanical-engineering-technology/",
    "https://superior.edu.pk/faculties/faculty-of-computer-science-and-information-technology/bs-robotics-and-artificial-intelligence/",
    "https://superior.edu.pk/faculties/faculty-of-computer-science-and-information-technology/ms-artificial-intelligence/",
    "https://www.superior.edu.pk/faculties/faculty-of-engineering-and-technology/bsc-mechanical-engineering-technology/"
    "https://www.superior.edu.pk/faculties/faculty-of-engineering-and-technology/bsc-civil-engineering-technology/",
    "https://www.superior.edu.pk/faculties/faculty-of-engineering-and-technology/bsc-electrical-engineering-technology/",
    "https://www.superior.edu.pk/faculties/faculty-of-engineering-and-technology/bs-information-security-and-digital-forensics/",
    "https://www.superior.edu.pk/faculties/faculty-of-engineering-and-technology/bs-robotics-and-artificial-intelligence/",
    "https://www.superior.edu.pk/faculties/faculty_category%/bs-biomedical-engineering-technology/",
    "https://www.superior.edu.pk/faculties/faculty-of-engineering-and-technology/bs-computer-system/",
    "https://www.superior.edu.pk/faculties/faculty-of-allied-health-sciences/bs-nuclear-medicine-technology/",
    "https://www.superior.edu.pk/faculties/faculty-of-allied-health-sciences/bs-nursing/",
    "https://www.superior.edu.pk/faculties/faculty-of-engineering-and-technology/bs-avionics-engineering/",
    "https://www.superior.edu.pk/faculties/faculty-of-allied-health-sciences/doctor-of-physical-therapy/",
    "https://www.superior.edu.pk/faculties/faculty-of-arts-and-humanities/bs-education-5th-semester/",
    "https://www.superior.edu.pk/faculties/faculty-of-engineering-and-technology/ms-electrical-engineering-2/",
    "https://www.superior.edu.pk/faculties/faculty-of-allied-health-sciences/ms-medical-laboratory-science/",
    "https://www.superior.edu.pk/faculties/faculty-of-allied-health-sciences/ms-public-health/",
    "https://www.superior.edu.pk/faculties/faculty-of-arts-and-humanities/ms-islamic-studies/",
    "https://www.superior.edu.pk/faculties/faculty-of-computer-science-and-information-technology/ms-artificial-intelligence-non-computing/",
    "https://www.superior.edu.pk/faculties/faculty-of-computer-science-and-information-technology/ms-artificial-intelligence/",
    "https://www.superior.edu.pk/faculties/faculty-of-computer-science-and-information-technology/ms-data-science-non-computing/",
    "https://www.superior.edu.pk/faculties/faculty-of-arts-and-humanities/m-phil-library-information-management/",
    "https://www.superior.edu.pk/faculties/faculty-of-arts-and-humanities/m-phil-education/",
    "https://www.superior.edu.pk/faculties/faculty-of-social-sciences/m-phil-mass-communication-management/",
    "https://www.superior.edu.pk/faculties/faculty-of-social-sciences/m-phil-mass-communication-professional-track/",
    "https://www.superior.edu.pk/faculties/faculty-of-social-sciences/ms-clinical-psychology/",
    "https://www.superior.edu.pk/faculties/associate-degree-programs/associate-degree-in-accounting-and-finance/",
    "https://www.superior.edu.pk/faculties/associate-degree-programs/associate-degree-in-computer-science/",
    "https://www.superior.edu.pk/faculties/associate-degree-programs/associate-degree-in-web-design-and-development/",
    "https://www.superior.edu.pk/faculties/associate-degree-programs/associate-degree-in-gaming-and-multimedia/",
    "https://www.superior.edu.pk/faculties/associate-degree-programs/associate-degree-in-cyber-security/",
    "https://www.superior.edu.pk/faculties/associate-degree-programs/associate-degree-in-business-administration/",
        # ... keep adding all the links you want to scrap here
]

headers = {"User-Agent": "Mozilla/5.0"}
all_programs_data = []

print(f"Starting Scraper for {len(program_links)} programs...")

for i, url in enumerate(program_links):
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            print(f"Skipping {url} - Status Code: {res.status_code}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        
        # Defensive extraction (Prevents the NoneType error we saw earlier)
        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Unknown Program"

        data = {
            "title": title,
            "url": url,
            "paragraphs": [p.text.strip() for p in soup.find_all("p") if p.text.strip()],
            "headings": [h.text.strip() for h in soup.find_all(["h2","h3","h4"]) if h.text.strip()],
            "tables": []
        }

        # Extract tables (Courses/Syllabus)
        for table in soup.find_all("table"):
            rows = []
            for tr in table.find_all("tr"):
                row = [td.text.strip() for td in tr.find_all(["td","th"])]
                rows.append(row)
            data["tables"].append(rows)

        all_programs_data.append(data)
        print(f"Successfully Scraped ({i+1}/{len(program_links)}): {title}")
        
        # Save every time a page is done (Safety measure)
        with open('superior_master_data.json', 'w', encoding='utf-8') as f:
            json.dump(all_programs_data, f, indent=4, ensure_ascii=False)
            
        time.sleep(1) # Small delay to avoid getting blocked

    except Exception as e:
        print(f"Error on {url}: {e}")

print("Master Knowledge Base Created!")