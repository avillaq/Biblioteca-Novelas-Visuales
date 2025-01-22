import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from gdata.blogger.service import BloggerService
from gdata.blogger.service import BlogPostQuery

class Post:
    def __init__(self, 
                full_url: str, 
                id_post: str,
                title: str, 
                synopsis: str, 
                cover_url: str, 
                screenshot_urls: list[str],
                specifications: dict[str, str],
                labels: list[str], 
                publication_date: str,
                update_date: str
            ):
        self._full_url = full_url
        self._id_post = id_post
        self._title = title
        self._synopsis = synopsis
        self._cover_url = cover_url
        self._screenshot_urls = screenshot_urls
        self._specifications = specifications
        self._labels = labels
        self._publication_date = publication_date
        self._update_date = update_date
    
    @property
    def full_url(self) -> str:
        return self._full_url
    
    @property
    def id_post(self) -> str:
        return self._id_post
    
    @property
    def title(self) -> str:
        return self._title

    @property
    def synopsis(self) -> str:
        return self._synopsis

    @property
    def cover_url(self) -> str:
        return self._cover_url

    @property
    def screenshot_urls(self) -> list[str]:
        return self._screenshot_urls
    
    @property
    def specifications(self) -> dict[str, str]:
        return self._specifications

    @property
    def labels(self) -> list[str]:
        return self._labels
    
    @property
    def publication_date(self) -> str:
        return self._publication_date
    
    @property
    def update_date(self) -> str:
        return self._update_date

    def __str__(self) -> str:
        return f"Url: {self.full_url}\nID: {self.id_post}\nTitle: {self.title}\nCover Image: {self.cover_url}\nSynopsis: {self.synopsis}\nScreenshots: {self.screenshot_urls}\nSpecifications: {self.specifications}\nLabels: {self.labels}\nPublication Date: {self.publication_date}\nUpdate Date: {self.update_date}"

class Post_Android:
    def __init__(self, title: str, full_url: str, cover_url: str, android_type: str):
        self._title = title
        self._full_url = full_url
        self._cover_url = cover_url
        self._android_type = android_type

    @property
    def title(self) -> str:
        return self._title

    @property
    def full_url(self) -> str:
        return self._full_url

    @property
    def cover_url(self) -> str:
        return self._cover_url
    
    @property
    def android_type(self) -> str:
        return self._android_type

    def __str__(self) -> str:
        return f"Title: {self.title}\nUrl: {self.full_url}\nUrl Image: {self.cover_url}\nType: {self.android_type}"



class VN_Blogger:
    def __init__(self):
        self._sections = {
            "inicio": "",
            "completo": "Completo",
            "allages": "sin h",
            "yuri": "yuri",
            "otome": "otome",
            "eroge": "eroge"
        }
        self._service = BloggerService()
        self._blog_id = "6976968703909484667"

    @property
    def sections(self) -> dict[str, str]:
        return self._sections
    
    @property
    def service(self) -> BloggerService:
        return self._service
    
    @property
    def blog_id(self) -> str:
        return self._blog_id

    # Private Methods
    def _verify_section(self, section: str) -> str:
        section = section.lower()
        for key in self.sections:
            if key.lower() == section:
                return key
        return None
    
    def _decode_data(self, data: str) -> str:
        if isinstance(data, bytes):
            return data.decode('utf-8')
        return data
    
    # Public Methods
    def get_section(self,
                    category: str = "inicio",
                    start_index: int = 1,
                    max_results: int = 25,
                    published_min: str = None,
                    published_max: str = None,
                    ) -> list[Post]:
        
        section = self._verify_section(category)
        if not section:
            raise ValueError(f"Section {section} not found")
        print(self.sections[section])

        list_posts = [] 
        query = BlogPostQuery(blog_id=self._blog_id)

        if self.sections[section]:
            query.categories = [self.sections[section]]

        query["start-index"] = str(start_index)
        query["max-results"] = str(max_results)
        if published_min:
            query["published-min"] = f"{published_min}T00:00:00-05:00"
        if published_max:
            query["published-max"] = f"{published_max}T00:00:00-05:00"

        feed = self.service.Get(query.ToUri())

        for entry in feed.entry:

            # Full URL
            full_url = self._decode_data(entry.link[4].href)

            # Id Post
            id_post = re.search(r"post-(\d+)", self._decode_data(entry.id.text)).group(1)

            # Title
            title = self._decode_data(entry.title.text)
            # Title exceptions to avoid. Maybe in the future there will be more exceptions like this
            title_exceptions = ["Kirikiroid", "Noticias", "Android", "Encuesta", "Navidad", "Aprende"]
            if any(exception in title for exception in title_exceptions):
                continue

            soup = BeautifulSoup("<html>"+self._decode_data(entry.content.text)+"</html>", "html.parser")
            first_part = soup.find("p")
            if not first_part:
                first_part = soup.find("div")
            print("-",id_post)
            first_part.decompose()
            
            html_text = soup.find("html").text
            expression = r"(Imágenes:|Imagenes:|Descarga Mega:|Descarga Mediafire:|Descarga OneDrive:)"
            slides = re.split(expression, html_text, flags=re.IGNORECASE)

            # Synopsis
            synopsis = re.sub(r'(\w+[,!\?\'\/\-\s\w]*(\[[^\]]*\])+)', "", slides[0].strip())

            # Cover and screenshots
            images = soup.find_all("img")
            cover_url = images[0].get("src")
            screenshot_urls = [image.get("src") for image in images[1:]]

            # Specifications
            specifications = slides[2].strip()
            expression = r"(Nombre|Genero|Tipo|Estudio|Tamaño del Archivo|Subtítulos|Subtitulos|Traducción Por|Traducción|Traduccion|Agradecimientos|Duración|Duracion)"
            slides = re.split(expression, specifications, flags=re.IGNORECASE)[1:]

            specifications = {}

            # The odd elements are the keys and the even elements are the values 
            for i in range(0, len(slides), 2):
                specifications[slides[i]] = slides[i+1].strip(': ').replace('\xa0', '')

            # Labels
            labels = []
            label_mapping = {
                "Completo": "Completo",
                "sin h": "All Ages",
                "yuri": "Yuri",
                "otome": "Otome",
                "eroge": "Eroge"
            }
            for i in entry.category:
                formatted_label = self._decode_data(i.term)
                if label_mapping.get(formatted_label):
                    labels.append(label_mapping[formatted_label])

            # Dates
            publication_date = datetime.strptime(self._decode_data(entry.published.text), "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")
            update_date = datetime.strptime(self._decode_data(entry.updated.text), "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")

            post = Post(full_url, id_post, title, synopsis, cover_url, screenshot_urls, specifications, labels, publication_date, update_date)
            list_posts.append(post)

        return list_posts


    def get_all_posts(self) -> list[Post]: # Get all the posts of the web site (PC)
        query = BlogPostQuery(blog_id=self._blog_id)

        list_posts = []
        start_index = 1
        max_results = 3
        while True:
            query["start-index"] = str(start_index)
            query["max-results"] = str(max_results)

            feed = self.service.Get(query.ToUri())

            if len(feed.entry) == 0 or start_index == 4:
                break

            for entry in feed.entry:

                # Full URL
                full_url = self._decode_data(entry.link[4].href)

                # Id Post
                id_post = re.search(r"post-(\d+)", self._decode_data(entry.id.text)).group(1)

                # Title
                title = self._decode_data(entry.title.text)
                # Title exceptions to avoid. Maybe in the future there will be more exceptions like this
                title_exceptions = ["Kirikiroid", "Noticias", "Android", "Encuesta", "Navidad", "Aprende"]
                if any(exception in title for exception in title_exceptions):
                    continue

                soup = BeautifulSoup("<html>"+self._decode_data(entry.content.text)+"</html>", "html.parser")
                soup.find("p").decompose()
                html_text = soup.find("html").text
                expression = r"(Imágenes:|Imagenes:|Descarga Mega:|Descarga Mediafire:|Descarga OneDrive:)"
                slides = re.split(expression, html_text, flags=re.IGNORECASE)

                # Synopsis
                synopsis = re.sub(r'(\w+[,!\?\'\/\-\s\w]*(\[[^\]]*\])+)', "", slides[0].strip())

                # Cover and screenshots
                images = soup.find_all("img")
                cover_url = images[0].get("src")
                screenshot_urls = [image.get("src") for image in images[1:]]

                # Specifications
                specifications = slides[2].strip()
                expression = r"(Nombre|Genero|Tipo|Estudio|Tamaño del Archivo|Subtítulos|Subtitulos|Traducción Por|Traducción|Traduccion|Agradecimientos|Duración|Duracion)"
                slides = re.split(expression, specifications, flags=re.IGNORECASE)[1:]

                specifications = {}

                # The odd elements are the keys and the even elements are the values 
                for i in range(0, len(slides), 2):
                    specifications[slides[i]] = slides[i+1].strip(': ').replace('\xa0', '')

                # Labels
                labels = []
                label_mapping = {
                    "Completo": "Completo",
                    "sin h": "All Ages",
                    "yuri": "Yuri",
                    "otome": "Otome",
                    "eroge": "Eroge"
                }
                for i in entry.category:
                    formatted_label = self._decode_data(i.term)
                    if label_mapping.get(formatted_label):
                        labels.append(label_mapping[formatted_label])

                # Dates
                publication_date = datetime.strptime(self._decode_data(entry.published.text), "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")
                update_date = datetime.strptime(self._decode_data(entry.updated.text), "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")

                post = Post(full_url, id_post, title, synopsis, cover_url, screenshot_urls, specifications, labels, publication_date, update_date)
                list_posts.append(post)

            start_index += max_results

        return list_posts

    # APK  http://www.visualnovelparapc.com/2022/01/android-apk.html
    ############################# The APK section is different from the others, so we need to scrap it differently #############################
    def get_apk_section(self) -> list[Post_Android]:

        url = self.sections["apk"]

        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.97'}
            response = requests.get(url, headers=header)
        except requests.exceptions.ConnectionError as e:
            print("Internet connection error. Please check your connection.")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')

        post = soup.find('div', class_='post-body')
  
        list_posts = []        
        
        # IMPORTANT !! 
        #I cannot scrap the titles of posts, so they will be added manually
        titles = [
            "Dorei to no Seikatsu -Teaching Feeling",
            "Sakura Swim Club",
            "Sakura Spirit",
            "Sakura Maid",
            "Sakura Halloween",
            "Sakura Christmas Party",
            "Sakura Valentine's Day",
            "My Neighbor is a Yandere!?",
            "Doki Doki Literature Club!",
            "Apricot Tei Monogatari",
            "Sono Hanabira - New Gen!",
            "Sono Hanabira 4",
            "Imouto Ijime",
            "Sunrider Academy",
            "Sakura Beach",
            "Sakura Fantasy",
            "Hidamari no Kioku(ntr)",
            "Sakura Shrine",
            "Butterfly Affection",
            "Sugar's Delight",
            "Sweetest Monster",
            "Aozora Meikyuu",
            "Sakura Magical Girls",
            "Wolf Tails",
            "Master of the Harem Guild",
            "The Demon's Stele & The Dog Princess",
            "Bullied Bride",
            "StayStay",
            "Wild Romance Mofu Mofu",
            "Imolicious",
            "Lost Life",
            "My Neighbor is a Yandere 2!?",
            "The Grim Reaper Who Reaped My Heart",
            "Lonely Yuri",
            "Love Love H Maid",
            "Otomaid @ Cafe(trap)",
            "Hansel y Gretel DS",
            "Kubitori Sarasa",
            "Cuidando la Casa con mi Hermanita",
            "Nai Training Diary[H]"
        ]
  
        # Image URL
        image_urls = post.find_all('img')
        
        # Full URL
        full_urls = post.find_all('a', string="Apk")

        # Type
        type = "apk"

        # IMPORTANT !! 
        # if the length of the titles, full_urls or image_urls is different, we need to check the original page: http://www.visualnovelparapc.com/2022/01/android-apk.html and manually add missing titles to the first position of the title list. Just do that.  
        if len(titles) != len(full_urls) or len(titles) != len(image_urls):
            raise ValueError("The length of the titles, full_urls or image_urls is different")

        for title, full_url, cover_url  in zip(titles,full_urls,image_urls):
            full_url = full_url.get('href')
            cover_url = cover_url.get('src')

            # Create a new instance
            post = Post_Android(title, full_url, cover_url, type)
            list_posts.append(post)

        return list_posts
        
    def get_kirikiroid2_section(self) -> list[Post_Android]:
        query = BlogPostQuery(blog_id=self._blog_id)
        query.categories = ["Kirikiroid2"]

        feed = self.service.Get(query.ToUri())
        
        soup = BeautifulSoup("<html>"+self._decode_data(feed.entry[0].content.text)+"</html>", "html.parser")

        list_posts = []

        # Titles
        all_title = soup.find_all("u")

        text_title = ""
        for title in all_title:
            text = title.text.strip()
            if text == "":
                continue
            text_title += text.replace("por AngelGbb", "").replace("por DaveVGN", "") # we discard the names of the uploaders

        filtered_titles = re.findall(r'(\w+[,!\?\'\/\-\s\w]*(\[[^\]]*\])+)', text_title)
        # Only the first match is the title of the post
        titles = [match[0] for match in filtered_titles]

        # Image URL
        image_urls = soup.find_all('img')[1:] # we discard the first image because it's not a game
    
        # Full URL
        full_urls = soup.find_all('a', string="Mediafire")

        # Type
        android_type = "kirikiroid2"

        # IMPORTANT !!
        # if the length of the titles, full_urls or image_urls is different, we need to check the original page: http://www.visualnovelparapc.com/2022/06/android-kirikiroid.html.
        if len(titles) != len(full_urls) or len(titles) != len(image_urls):
            raise ValueError("The length of the titles, full_urls or image_urls is different")

        for title, full_url, cover_url  in zip(titles,full_urls,image_urls):
            full_url = full_url.get("href")
            cover_url = cover_url.get("src")

            # Create a new instance
            post = Post_Android(title, full_url, cover_url, android_type)
            list_posts.append(post)

        return list_posts
        
    def get_kirikiroid2_emulator(self) -> str:
        query = BlogPostQuery(blog_id=self._blog_id)
        query.categories = ["Kirikiroid2"]

        feed = self.service.Get(query.ToUri())
        
        soup = BeautifulSoup("<html>"+self._decode_data(feed.entry[0].content.text)+"</html>", "html.parser")

        # Emulator
        emulator = soup.find("a", string="Apk").get("href")

        return emulator



if __name__ == '__main__':
    blogger = VN_Blogger()
    """ post = Post("Hanachirasu", "http://www.visualnovelparapc.com/2022/10/hanachirasu.html", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiloJxDae8yr-lKe0eAj2xmyekmU8SGMHpx2gX5hcXYLDcm1JBq2x4hfxMmfUtEiUs4UgFML7keBJaKKUlWsqwDOjDy7_bc9Cp4AapY-HzJczqM-MlL56xdv2EBhbZ-5Wx7hkQykX1JcV4GuJ-Bzw9OrefPf4Hti9uPa0juL4s6DotQEv_l9C3WZQZpAm4/w400-h299/sms.png", "Esto es una prueba", [],"2024-02-06") """
    
    
    list_posts= blogger.get_kirikiroid2_emulator()
    print(list_posts)

    """ for post in list_posts:
        print(post)
        print("\n") """
