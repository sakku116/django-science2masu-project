function showFetchDataLoading() {
  const fetch_data_loading = document.querySelector('#fetch_data_loading');
  fetch_data_loading.style.display = "block";
};

function hideFetchDataLoading() {
  const fetch_data_loading = document.querySelector('#fetch_data_loading');
  fetch_data_loading.style.display = 'none';
};

function triggerMasonryLayout() {
  // idk why masonry must be declared after element is rendered
  // init Masonry
  const masonry_grid = document.querySelector('.masonry-grid');
  var masonry = new Masonry(masonry_grid, {
    itemSelector: ".masonry-grid-item",
    isFitWidth: true,
    gutter: 5,
    transitionDuration: 0,
  });
  // layout Masonry after each image loads
  imagesLoaded(masonry_grid).on('progress', function () {
    masonry.layout();
  });
}

function renderImages(img_url_list) {
  const gallery_container = document.querySelector('#gallery_container');

  for (img_url of img_url_list) {
    var a = document.createElement('a');
    a.setAttribute('href', `/external_hit?url=${img_url}`)
    a.setAttribute('target', '_blank');

    var img = document.createElement('img')
    img.setAttribute('title', 'Click to open in new tab')
    img.setAttribute('class', 'masonry-grid-item')
    img.setAttribute('loading', 'lazy')
    img.setAttribute('src', img_url + '?w=400'); // add imgix query to process image (only imgix url)

    a.append(img)
    gallery_container.append(a);
  };

  triggerMasonryLayout();

  hideFetchDataLoading();
};

function fetchImageUrls(url) {
  showFetchDataLoading();
  fetch(url)
    .then(response => response.json())
    .then(result => {
      const img_url_list = result['img_url_list'];
      renderImages(img_url_list);
    })
    .catch(error => {
      console.log(error);

      const fetch_data_loading = document.querySelector('#fetch_data_loading');
      if ((document.querySelectorAll('.masonry-grid-item')).length === 0) {
        fetch_data_loading.innerHTML = "failed to fetch data";
      } else {
        fetch_data_loading.innerHTML = "failed to fetch others data";
      };

    });
};

document.addEventListener('DOMContentLoaded', () => {
  fetchImageUrls('/api/img-url-list?prefix=gallery')
  setTimeout(() => fetchImageUrls('/api/img-url-list?prefix=gallery/others'), 5000)

  /* LOAD IMAGE LIST USING RESTAPI 

  const total_data = 5;
  var from_index = 0;
  var to_index = from_index + total_data;

  var do_fetch = true;

  function addGalleryItems(img_url_list) {
    img_url_list.forEach(img_url => {
      const gallery_container = document.querySelector('#gallery_container');
      const gallery_item_wrapper = document.createElement('a');
      gallery_item_wrapper.setAttribute('href', `/external_hit?url=${img_url}`);

      const gallery_item = document.createElement('img');
      gallery_item.setAttribute('title', 'Click to open in new tab');
      gallery_item.setAttribute('class', 'masonry-grid-item');
      gallery_item.setAttribute('loading', 'lazy');
      gallery_item.setAttribute('src', img_url);

      gallery_item_wrapper.append(gallery_item);
      gallery_container.append(gallery_item_wrapper);
      masonry.layout();
    });
    hideFetchDataLoading();
  };

  function fetch_img_url_list() {
    fetch(`/img-url-list?from_index=${from_index}&to_index=${to_index}&prefix=gallery/others`)
      .then(response => response.json())
      .then(data => {
        console.log(`fetched file_name_list ${data.from_index}->${data.to_index}`);
        from_index = to_index;
        to_index = from_index + total_data;
        var img_url_list = data.img_url_list;

        // prevent repeating event
        if ((from_index != data.from_index)) {
          addGalleryItems(img_url_list);
        };

        // dissable schedule when data is over
        if (data.is_data_over) {
          clearTimeout(schedule_enable_fetch);
        };

      })
  };

  window.onscroll = () => {
    // detect whether page is scrolled in bottom
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
      if (do_fetch) {
        console.log('fetching...');
        showFetchDataLoading();

        // disable fetching event for a while
        do_fetch = false;
        const schedule_enable_fetch = setTimeout(() => {do_fetch = true}, 5000);

        fetch_img_url_list()
      }
    }
  };
  */

});
/*  data-masonry='{"itemSelector": ".masonry-grid-item", "horizontalOrder": true, "isFitWidth": true, "gutter": 5, "transitionDuration": 0}' */