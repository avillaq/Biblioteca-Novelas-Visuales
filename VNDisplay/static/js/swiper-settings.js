import Swiper from 'https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.mjs'

document.addEventListener('DOMContentLoaded', init);
function init() {

    const swiper = new Swiper('.swiper', {
        slidesPerView: 2,  // when window width is <= 540px
        spaceBetween: 20,
        loop: true,
        autoplay: {
            delay: 2500,
            disableOnInteraction: false,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            // when window width is >= 540px
            540: {
              slidesPerView: 3
            },
            // when window width is >= 800px
            800: {
              slidesPerView: 4
            },
            // when window width is >= 1000px
            1000: {
              slidesPerView: 5
            }
        }
    });




}