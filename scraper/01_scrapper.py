"""
Step 1: Scrape ITI Website
Run: python 01_scrape.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time, pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

visited = set()
data = []
options = Options()
options.add_argument("--headless")                # run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")   # important for pages that depend on size
# Optional: speed up page loads
options.page_load_strategy = "eager"
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

def scrape(url, depth=0):
    if (url not in visited )and(depth < 5):
        visited.add(url)
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        
        

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        text_parts = []

        for tag in soup.find_all(["h1","h2","h3","h4","p","li","span","div"]):
            content = tag.get_text(strip=True)
            if content:
                text_parts.append(content)
        data.append({"url": url, "content": " ".join(text_parts)})
        for a in soup.find_all("a", href=True):
            link = a["href"]

            # ignore mailto, tel, pdf, images
            if link.startswith("mailto") or link.startswith("tel") or ".pdf" in link:
                continue

            #internal links
            if link.startswith("/"):
                link = "https://iti.gov.eg" + link
            
            # only focus on iti.gov.eg links
            if "iti.gov.eg" in link:
                scrape(link, depth + 1)


service_links = [
    "https://iti.gov.eg/home",
    ######################################################################################################
    "https://iti.gov.eg/services/programCategory/details/90eb9189-6cd2-4ed1-6890-08dbe5cce072",#post_grad
    "https://iti.gov.eg/services/programCategory/details/1f8881bc-7bd5-4402-6891-08dbe5cce072",#under_grad
    "https://iti.gov.eg/services/programCategory/details/55def364-fdbc-4c71-a507-3acdc4a08bf9",#tech_buisiness
    "https://iti.gov.eg/services/programCategory/details/6bcfaf35-26b9-4db6-b9d4-9790fa77d8e7",#tech_ambassadors
    "https://iti.gov.eg/services/programCategory/details/03ff42e5-8523-40e4-b0b8-9b79127c7cc2",#jouniors
    ####################### Professional Training Program - (9 Months) ##################################
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/bbb80029-50e7-45dd-fe28-08dbe75ac461",#Digital IC Design
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/59d2e6c7-7221-4024-fe29-08dbe75ac461",#Industrial Automation
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/6fe70953-57eb-4108-e476-08ddbf895a42",#Telco-Cloud Engineering
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/911e3ea8-e71d-42be-8915-08ddc45d0929",#Embedded & Edge Architectures
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/f84a5c67-29ae-4584-fe16-08dbe75ac461",#Game Programming
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/f8c443d7-7e5a-4f28-fe1d-08dbe75ac461",#Game Art
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/081938a0-8844-4c43-fe20-08dbe75ac461",#VFX Compositing
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/694d8ce5-d1f5-4f18-fe2e-08dbe75ac461",#2D Animation and Motion Graphics
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/5196d2a0-aacb-4f69-569e-08dc1681e04a",#3D FX Dynamics and Simulation
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/111116ff-5fb8-4bb2-569f-08dc1681e04a",#3D Generalist
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/c395af87-08de-4ad0-56a0-08dc1681e04a",#3D Animation
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/4d22d3a0-fa19-4018-a1fe-08dca49e88db",#CG Technical Director
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/809b6241-1a01-4848-fde6-08dbe75ac461", #Systems Administration
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/def7af93-bc81-471a-fe03-08dbe75ac461", #Cyber Security
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/540d81d0-5f53-4875-fe1c-08dbe75ac461", #Cloud Architecture
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/2d24f998-e356-418b-fddf-08dbe75ac461", #Geoinformatics
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/f6e5a1b0-6659-4cb7-fde4-08dbe75ac461", #ERP Consulting
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/a414a379-621b-498e-fe25-08dbe75ac461", #Architecture, Engineering and Construction Informatics
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/ed19aabf-7ac0-43d5-fe2f-08dbe75ac461", #Data Management
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/134636fe-7a41-49b0-fe32-08dbe75ac461", #Data Science
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/eb1cf1fe-b577-4d09-fe07-08dbe75ac461", #Open Source Applications Development
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/8dfcab71-1d6c-47e4-fe0b-08dbe75ac461", #Cloud Platform Development
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/4769cf5d-3f00-4d47-fe0c-08dbe75ac461", #Enterprise & Web Apps Development (Java)
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/5e7419be-1f6e-4d2f-fe10-08dbe75ac461", #Mobile Applications Development (Native)
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/0ce12985-b2a6-4167-fe11-08dbe75ac461", #Professional Development & BI-infused CRM
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/34cf88d0-cbf9-45a4-fe13-08dbe75ac461", #Web & User Interface Development
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/03fd8892-7259-4340-fe1a-08dbe75ac461", #Telecom Applications Development
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/911a6fa1-66db-4e6e-fe21-08dbe75ac461", #Mobile Applications Development (Cross Platform)
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/6e205a30-e997-4568-a1ff-08dca49e88db", #Integrated Software Development & Architecture
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/a7f31797-bfe7-4ba5-fe30-08dbe75ac461", #AI and Machine Learning
    "https://iti.gov.eg/diplomaStructure/139758dc-e1ee-4d2c-ba87-08dbe615d378/tracks/4d854c93-3ac7-411b-5cf6-08ddad7f3080/efdb3708-b42d-44ef-fdf1-08dbe75ac461", #Software Testing & Quality Assurance
     ####################### Intensive Code Camps - (3 Months) ##################################
     ###Industrial systemd
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/ded3c57d-3d49-4c32-fe8b-08dbe75ac461", #Industrial Automation
    ###Conten development
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/f6df68ad-b9b5-4cca-fe56-08dbe75ac461", #2D Graphic Design
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/47e16692-6133-4e51-fe7c-08dbe75ac461", #3D character artist
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/f08f151a-089b-4e65-fe92-08dbe75ac461", #Interior Design
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/949e8eb0-7107-46cc-c46f-08dce3928d72", #Concept Art
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/9d2833f6-0e85-4593-c6f5-08de05724155", #Furniture Visualization
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/e6bef3d8-9377-4795-fe79-08dbe75ac461", #E-Learning Specialist
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/a480153c-74a7-492a-fe80-08dbe75ac461", #Motion Graphics
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/8adeab38-e25f-4af9-c46d-08dce3928d72", #3D Rigger
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/e1c836ea-4490-4822-b232-08de04a8e6a4", #Full Stack CMS & E-Commerce Development
    ###Cyber Security
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/dc9bc1fe-5283-40ce-fe6b-08dbe75ac461", #Cybersecurity Associate
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/acaeee9d-d820-4361-fe89-08dbe75ac461", #AWS Re /Start
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/894d2d8c-42e6-48d4-fe85-08dbe75ac461", #Systems Administration
    ###Information Systems
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/bdc6038a-1f54-47df-fe4b-08dbe75ac461", #Geo-Spatial Technologies
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/e42aae84-85a9-48a9-fe97-08dbe75ac461", #Data Engineering
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/fae2a23d-4b1f-45c4-fe8d-08dbe75ac461", #Building Information Modeling Automation Development
    ###Software engineering and agentic AI development
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/9fd05d75-f143-4ad8-fe6c-08dbe75ac461", #Front-end and Cross-Platform Mobile Development with Gen AI Integration
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/dcdd9728-8df9-4a6d-fe6e-08dbe75ac461", #Full-Stack Web & Generative AI Development using MEA|RN
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/48466676-3ee9-490e-fe73-08dbe75ac461", #Software Development Fundamentals
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/0ad01172-0265-4198-fe82-08dbe75ac461", #UI/UX Design
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/4a3b5d66-2e43-4035-daa0-08dc1a7d1958", #Business Analysis
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/17da2093-adc1-42bf-fe6d-08dbe75ac461", #Full-Stack Web & Generative AI Development using .Net
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/f544724f-6824-4b69-fe6f-08dbe75ac461", #Full-Stack Web & Generative AI Development using Python
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/8df36de3-659c-450c-fe75-08dbe75ac461", #Web Development Using CMS
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/69c378dc-5477-427a-6719-08dc15a4ea55", #Full-Stack Web & Generative AI Development using PHP
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/e1c836ea-4490-4822-b232-08de04a8e6a4", #Full Stack CMS & E-Commerce Development
    ### Cognitive Computing and Artificial intelligence
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/5ced0985-9a99-46a4-fe95-08dbe75ac461", #Power BI Development
    ### AI software testing & Validation
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/5d78e48c-e891-4fce-fe45-08dbe75ac461", #Software Testing
    ### Digital Marketing
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/fa40ec14-324f-4a9a-fe3d-08dbe75ac461", # Digital Marketing
    "https://iti.gov.eg/diplomaStructure/3eb61fd9-bcc5-4d5c-ba88-08dbe615d378/tracks/1235b303-eafc-4480-1799-08de017145e6/0261af02-e795-4c42-fe55-08dbe75ac461", #Social Media Marketing
]


# 2. Start the crawling operation from level 0
for link in service_links:
    scrape(link, depth=0)

driver.quit()
# store data
df = pd.DataFrame(data)
df.drop_duplicates(subset=['url', 'content'], inplace=True)
df.to_csv("data/iti_full_website_data.csv", index=False)
print("Scrapping Done ")