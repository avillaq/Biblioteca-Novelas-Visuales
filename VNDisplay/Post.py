import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'es_ES') # Set the locale to spanish

# En esta clase se define la estructura de un post y se define el scraper para obtener los posts de la página web

############ En esta clase una sola funcion para todas las secciones ############

class Post:
    def __init__(self, title: str, full_url: str, image_url: str, description: str, labels: list[str], date: str):
        self._title = title
        self._full_url = full_url
        self._image_url = image_url
        self._description = description
        self._labels = labels
        self._date = date

    @property
    def title(self) -> str:
        return self._title

    @property
    def full_url(self) -> str:
        return self._full_url

    @property
    def image_url(self) -> str:
        return self._image_url

    @property
    def description(self) -> str:
        return self._description

    @property
    def labels(self) -> list[str]:
        return self._labels
    
    @property
    def date(self) -> str:
        return self._date
    

    def __str__(self) -> str:
        return f"Title: {self.title}\nUrl: {self.full_url}\nUrl Image: {self.image_url}\nDescription: {self.description}\nLabels: {self.labels}\nDate: {self.date}"

class Post_Android:
    def __init__(self, title: str, full_url: str, image_url: str, type: str):
        self._title = title
        self._full_url = full_url
        self._image_url = image_url
        self._type = type

    @property
    def title(self) -> str:
        return self._title

    @property
    def full_url(self) -> str:
        return self._full_url

    @property
    def image_url(self) -> str:
        return self._image_url
    
    @property
    def type(self) -> str:
        return self._type

    def __str__(self) -> str:
        return f"Title: {self.title}\nUrl: {self.full_url}\nUrl Image: {self.image_url}\nType: {self.type}"



class VN_Scraper:
    def __init__(self):
        self._sections = {
            "inicio": "http://www.visualnovelparapc.com/",
            "Completo": "http://www.visualnovelparapc.com/search/label/Completo",
            "allages": "http://www.visualnovelparapc.com/search/label/sin%20h",
            "yuri": "http://www.visualnovelparapc.com/search/label/yuri",
            "otome": "http://www.visualnovelparapc.com/search/label/otome",
            "eroge": "http://www.visualnovelparapc.com/search/label/eroge",
            "apk": "http://www.visualnovelparapc.com/2022/01/android-apk.html",
            "kirikiroid2": "http://www.visualnovelparapc.com/2022/06/android-kirikiroid.html"
        }
        self._current_page = 1

    @property
    def sections(self) -> dict[str, str]:
        return self._sections

    @property
    def current_page(self) -> int:
        return self._current_page
    
    @current_page.setter
    def current_page(self, value: int):
        self._current_page = value

    # Private Methods
    def _verify_section(self, section: str) -> str:
        section = section.lower()
        for key in self.sections:
            if key.lower() == section:
                return key

        return None

    def _get_posts(self, url : str) -> list[Post]:
        
        domain = "www.visualnovelparapc.com"  # The domain of the page
        if domain not in url:
            raise ValueError("URL does not belong to the domain")

        try:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.97'}
            response = requests.get(url, headers=header)
        except requests.exceptions.ConnectionError as e:
            print("Internet connection error. Please check your connection.")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')

        posts_by_date = soup.find_all('div', class_='date-outer') #############################

        list_posts = []

        for post_by_date in posts_by_date:

            # Date
            date = post_by_date.find('h2', class_='date-header').text     
            date = datetime.strptime(date, '%A, %d de %B de %Y')
            date = date.strftime("%Y-%m-%d")


            posts = post_by_date.find_all('div', class_='post-outer')
            for post in posts:
                # Title
                title = post.find('h3', class_='post-title').text

                # Title exceptions to avoid. Maybe in the future there will be more exceptions like this
                title_exceptions = ["Kirikiroid", "Noticias", "Android", "Encuesta", "Navidad"]
                if any(exception in title for exception in title_exceptions):
                    continue

                # Post body
                post_body = post.find('div', class_='post-body')
                
                # Url full
                post_url = post_body.find('a')
                full_url = post_url.get('href')
                if "html" not in full_url:
                    continue

                # Url image
                if not post_body.find('img'): # if there's no image in the post, we avoid it
                    continue
                image_url = post_body.find('img').get('src')
                
                # Description
                post_description = post_body.text
                description = post_description.strip().replace("\n", " ").replace(post_url.text, "")

                # Labels
                post_labels = post.find('span', class_='post-labels').text
                list_labels = []

                label_mapping = {
                    "Completo": "Completo",
                    "sin h": "All Ages",
                    "yuri": "Yuri",
                    "otome": "Otome",
                    "eroge": "Eroge"
                }

                for label in label_mapping:
                    if label in post_labels:
                        list_labels.append(label_mapping[label])
                
                
                # Create a new instance
                post = Post(title, full_url, image_url, description, list_labels, date)
                list_posts.append(post)

        return list_posts
    
    # Public Methods
    def get_section(self, section: str) -> list[Post]: ### Only scrap the first page of the section
        section = self._verify_section(section) ################################### mover contenido de _verify_section aqui ###################
        if not section:
            raise ValueError(f"Section {section} not found")
        
        # Get the url of the section
        url = self.sections[section]
        
        list_posts = self._get_posts(url)

        return list_posts

    def get_all_posts(self) -> list[Post]:
        url = self.sections["inicio"]
        list_posts = self._get_posts(url) # get the first page

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.97'}
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')

        url = soup.find('a', class_='blog-pager-older-link')
        while url:
            url = url.get('href')
            list_posts += self._get_posts(url)

            response = requests.get(url, headers=header)
            soup = BeautifulSoup(response.content, 'html.parser')
            url = soup.find('a', class_='blog-pager-older-link')

        return list_posts


    ## TODO: Esta funcion funciona correctamente, pero solo para segunda pagina, hay que hacerla para todas las paginas (SOLO SI ES POSIBLE), ya que tenemos que ver como sera la paginacion con Django
    def get_next_page_section(self, section: str) -> list[Post]:
        section = self._verify_section(section)
        if not section:
            raise ValueError(f"Section {section} not found")
        
        # Get the url of the section
        url = self.sections[section]   

        # Get the next page 
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.97'}
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')

        next_page = soup.find('a', class_='blog-pager-older-link').get('href')
        return self._get_posts(next_page)
    

    def get_post_detail(self, post: Post = None) -> tuple[any]:

        #Title
        title = post.title

        # Main image
        main_image = post.image_url

        url = post.full_url

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.97'}
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')

        post_detail = soup.find('div', class_='post-body')

        # Images
        images = post_detail.find_all('img')[1:] # we discard the first image because we already have it in the post list
        images = [image.get('src') for image in images]


        expression = r"(Imágenes:|Imagenes:|Descarga Mega:|Descarga Mediafire:)"
        slides = re.split(expression, post_detail.text, flags=re.IGNORECASE)
        # Sinopsis
        sinopsis = slides[0].strip().replace(title, "")

        # Specifications
        specifications = slides[2].strip()
        expression = r"(Nombre|Genero|Tipo|Estudio|Tamaño del Archivo|Subtítulos|Subtitulos|Traducción Por|Traducción|Traduccion|Agradecimientos|Duración|Duracion)"
        slides = re.split(expression, specifications, flags=re.IGNORECASE)[1:]

        specifications = {}

        # The odd elements are the keys and the even elements are the values 
        for i in range(0, len(slides), 2):
            specifications[slides[i]] = slides[i+1].strip(': ').replace('\xa0', '')

        # Return the post detail
        post_detail = (title, main_image, sinopsis, images, specifications)
        
        return post_detail

    # APK  http://www.visualnovelparapc.com/2022/01/android-apk.html
    ############################# The APK section is different from the others, so we need to scrap it differently #############################
    def get_apk_section(self) -> list[Post_Android]:

        url = self.sections["apk"]
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.97'}
        response = requests.get(url, headers=header)
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

        for title, full_url, image_url  in zip(titles,full_urls,image_urls):
            full_url = full_url.get('href')
            image_url = image_url.get('src')

            # Create a new instance
            post = Post_Android(title, full_url, image_url, type)
            list_posts.append(post)

        return list_posts
        

    # Emulador Kirikiroid2   http://www.visualnovelparapc.com/2022/06/android-kirikiroid.html
    ############################# The kirikiroid2 section is different from the others, so we need to scrap it differently #############################
    def get_kirikiroid2_section(self) -> tuple[list[Post_Android], str]:
        url = self.sections["kirikiroid2"]
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.2151.97'}
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')

        post = soup.find('div', class_='post-body')

        list_posts = []

        # Emulator
        emulator = post.find('a', string="Apk").get('href')

        # Titles
        titles = post.find_all("u")

        text_title = ""
        for title in titles:
            text = title.text.strip()
            if text == "":
                continue
            text_title += text.replace("por AngelGbb", "").replace("por DaveVGN", "") # we discard the names of the uploaders

        titles = re.findall(r'(\w+[,!\?\'\/\-\s\w]*(\[[^\]]*\])+)', text_title)
        # Only the first match is the title of the post
        titles = [match[0] for match in titles]

        # Image URL
        image_urls = post.find_all('img')[1:] # we discard the first image because it's not a game
    
        # Full URL
        full_urls = post.find_all('a', string="Mediafire")

        # Type
        type = "kirikiroid2"

        # IMPORTANT !!
        # if the length of the titles, full_urls or image_urls is different, we need to check the original page: http://www.visualnovelparapc.com/2022/06/android-kirikiroid.html.
        if len(titles) != len(full_urls) or len(titles) != len(image_urls):
            raise ValueError("The length of the titles, full_urls or image_urls is different")

        for title, full_url, image_url  in zip(titles,full_urls,image_urls):
            full_url = full_url.get('href')
            image_url = image_url.get('src')

            # Create a new instance
            post = Post_Android(title, full_url, image_url, type)
            list_posts.append(post)

        return list_posts, emulator
        


if __name__ == '__main__':
    scraper = VN_Scraper()
    #post = Post("PruebaPOST", "http://www.visualnovelparapc.com/2022/10/hanachirasu.html", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiloJxDae8yr-lKe0eAj2xmyekmU8SGMHpx2gX5hcXYLDcm1JBq2x4hfxMmfUtEiUs4UgFML7keBJaKKUlWsqwDOjDy7_bc9Cp4AapY-HzJczqM-MlL56xdv2EBhbZ-5Wx7hkQykX1JcV4GuJ-Bzw9OrefPf4Hti9uPa0juL4s6DotQEv_l9C3WZQZpAm4/w400-h299/sms.png", "Esto es una prueba", [],"2024-02-06")
    
    
    
    list_posts, emulador = scraper.get_kirikiroid2_section()
    #print(list_posts)

    for post in list_posts:
        print(post)
        print("\n")

    print(emulador)
