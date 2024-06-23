const swiperTop = new Swiper('.top__swiper', {
    /*
    effect: 'fade',
    autoplay: {
    delay: 3500,
    disableOnInteraction: false,
    },
     */
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});

function playVideo(videoId) {
    var video = document.getElementById('video' + videoId);
    var preview = document.getElementById('preview' + videoId);
    preview.style.display = 'none';
    video.play();
}

const SwiperVideo = new Swiper('.video__swiper', {
    slidesPerView: 3,
    spaceBetween: 30,
    freeMode: true,
    effect: 'fade',
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    on: {
        slideChange: function () {
            const videos = document.querySelectorAll('.video-container video');
            videos.forEach(video => {
                video.pause();
                video.currentTime = 0;
            });
        },
    },
});

const swiperAbout = new Swiper(".about__slider", {
    slidesPerView: 3,
    spaceBetween: 5,
    loop: true,
    freeMode: true,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});

const swiper = new Swiper(".period__slider", {
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

function openDetails(photoId) {
    var photo = document.getElementById(photoId);
    var details = document.getElementById('photoDetails');
    var image = photo.querySelector('img').src;

    var title = photo.getAttribute('data-title');
    var source = photo.getAttribute('data-source');
    var tags = photo.getAttribute('data-tags');
    var period = photo.getAttribute('data-period');

    document.getElementById('details-image').src = image;
    document.getElementById('details-title').innerText = title || 'No title';
    document.getElementById('details-source').innerText = source || 'No source';

    var tagsContainer = document.getElementById('details-tags');
    tagsContainer.innerHTML = ''; // Clear existing tags
    if (tags) {
        var tagsArray = tags.split(', ');
        tagsArray.forEach(function(tag) {
            var tagLink = document.createElement('a');
            tagLink.href = '/photos?tags=' + encodeURIComponent(tag);
            tagLink.innerText = tag;
            tagsContainer.appendChild(tagLink);
            tagsContainer.appendChild(document.createTextNode(', ')); // Add a comma and space
        });
        // Remove the last comma and space
        tagsContainer.removeChild(tagsContainer.lastChild);
    } else {
        tagsContainer.innerText = 'No tags';
    }

    document.getElementById('details-period').innerText = period || 'No period';

    details.style.display = 'block';
}





function closeDetails() {
    var details = document.getElementById('photoDetails');
    details.style.display = 'none';
}






