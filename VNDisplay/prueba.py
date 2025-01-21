from gdata.blogger.service import BloggerService
from gdata.blogger.service import BlogPostQuery

def get_blog_posts(blog_id, max_results=3):
    try:
        # Configuración del servicio BloggerService
        service = BloggerService()
        
        # Crear query con filtros
        query = BlogPostQuery(blog_id=blog_id, categories=["sin h"], params={
            "max-results": str(max_results),
            "orderby": "published",
            "start-index": "1"
        })
        
        # Obtener posts filtrados
        filtered_feed = service.Get(query.ToUri())
        
        for entry in filtered_feed.entry:
            # Decodificar el título de bytes a string UTF-8
            title = entry.title.text.decode('utf-8') if isinstance(entry.title.text, bytes) else entry.title.text
            url = entry.link[4].href
            print(f"\n-{title.strip()}")
            print(f"-{url}")
            
    except Exception as e:
        print(f"Error al obtener posts: {str(e)}")

if __name__ == "__main__":
    BLOG_ID = "6976968703909484667"
    get_blog_posts(BLOG_ID)