const swiperTop = new Swiper('.top__swiper', {
  // Optional parameters
  effect: 'fade',
/*
  autoplay: {
  delay: 3500,
  disableOnInteraction: false,
  },
*/
  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});

document.addEventListener('DOMContentLoaded', function () {
    const swiperTop = new Swiper('.video__swiper', {
        slidesPerView: 3,
        spaceBetween: 30,
        freeMode: true,
        effect: 'fade',
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });

    function pauseAllVideos() {
        const videos = document.querySelectorAll('.video__container-video');
        videos.forEach(function (video) {
            if (!video.paused) {
                video.pause();
            }
        });
    }

    swiperTop.on('slideChange', function () {
        pauseAllVideos();
    });
});



const swiperAbout = new Swiper(".about__slider", {
  slidesPerView: 4,
  spaceBetween: 20,
  freeMode: true,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});

const  swiper = new Swiper(".period__slider", {
  direction: "vertical",
  slidesPerView: 1,
  spaceBetween: 30,
  mousewheel: true,
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});
/*
document.getElementById('toggleNav').addEventListener('click', function(event) {
    const mainNav = document.getElementById('mainNav');
    if (mainNav.style.display === 'none') {
      mainNav.style.display = 'flex';
    } else {
      mainNav.style.display = 'none';
    }
});
 */


document.querySelectorAll(".video__container-trigger").forEach((trigger) => {
    trigger.addEventListener('click', function () {
            trigger.classList.add('video__container--active');
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const triggers = document.querySelectorAll('.video__container-trigger');
    const videoContainers = document.querySelectorAll('.video__container');
    const videoElements = document.querySelectorAll('.video__container-video');

    triggers.forEach((trigger, index) => {
        trigger.addEventListener('click', function() {
            videoContainers[index].classList.add('video-container--active');
            videoElements[index].play();
        });
    });
});





