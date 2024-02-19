document.addEventListener('DOMContentLoaded', init);
function init() {
    const novels = document.querySelectorAll('.novel');
    novels.forEach(novel => {
        novel.addEventListener('click', function () {
            const novel_id = novel.getAttribute('data-id');

            let url = new URL(novel_id);
            let ruta = url.pathname.replace('.html', '');

            let nuevaUrl = `${window.location.origin}/novel${ruta}`;
            //console.log(nuevaUrl);
            window.location.href = nuevaUrl;
        });
    });
}