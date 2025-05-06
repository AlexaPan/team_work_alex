import requests
from bs4 import BeautifulSoup

def parse_flru_projects(page=1):
    url = f"https://www.fl.ru/projects/?page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    projects = []

    for card in soup.select(".b-post"):  # каждый проект
        title_tag = card.select_one(".b-post__link")
        price_tag = card.select_one(".b-post__price")
        desc_tag = card.select_one(".b-post__txt")

        title = title_tag.get_text(strip=True) if title_tag else "Без названия"
        link = f"https://www.fl.ru{title_tag['href']}" if title_tag else None
        price = price_tag.get_text(strip=True) if price_tag else "Не указано"
        desc = desc_tag.get_text(strip=True) if desc_tag else "Нет описания"

        projects.append({
            "title": title,
            "link": link,
            "price": price,
            "description": desc
        })

    return projects
def debug_parse_flru():
    url = "https://www.fl.ru/projects/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Сохраняем HTML для отладки
    with open("flru_page.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("✅ HTML сохранён в 'flru_page.html'. Открой его в браузере и найди структуру карточек.")

    # Простой вывод для отладки
    soup = BeautifulSoup(response.text, "html.parser")
    all_divs = soup.find_all("div")
    print(f"🔍 Всего <div>: {len(all_divs)}")

    # Выведем первые 10 с классами
    for div in all_divs[:20]:
        print(div.get("class"))

    return soup



def fetch_flru_projects_api(page=1, limit=20):
    url = f"https://api.fl.ru/v1/projects/?page={page}&limit={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()

    projects = []

    for item in data.get("items", []):
        project = {
            "title": item.get("name"),
            "link": f"https://www.fl.ru/projects/{item.get('id')}/",
            "price": item.get("budget", {}).get("amount") or "Не указано",
            "currency": item.get("budget", {}).get("currency", {}).get("code"),
            "description": item.get("description")
        }
        projects.append(project)

    return projects


if __name__ == "__main__":
    projects = fetch_flru_projects_api()

    for p in projects[:5]:
        print(f"\n📌 {p['title']}")
        print(f"🔗 {p['link']}")
        print(f"💰 {p['price']} {p['currency']}")
        print(f"📝 {p['description'][:100]}...")