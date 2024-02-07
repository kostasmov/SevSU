var photos = ["photos/1.webp", "photos/2.webp", "photos/3.webp", "photos/4.webp", "photos/5.webp", 
            "photos/6.webp", "photos/7.webp", "photos/8.webp", "photos/9.webp", "photos/10.webp", 
            "photos/11.webp", "photos/12.webp", "photos/13.webp", "photos/14.webp", "photos/15.webp", 
            "photos/16.webp", "photos/17.webp", "photos/18.webp", "photos/19.webp", "photos/20.webp"];

var titles = ["Подпись 1", "Подпись 2", "Подпись 3", "Подпись 4", "Подпись 5", "Подпись 6", "Подпись 7",
              "Подпись 8", "Подпись 9", "Подпись 10", "Подпись 11", "Подпись 12", "Подпись 13", "Подпись 14", 
              "Подпись 15", "Подпись 16", "Подпись 17", "Подпись 18", "Подпись 19", "Подпись 20"];

$(document).ready(function() {
  var photoAlbum = $("#photo-album");
  var totalImages = photos.length;

  for (var i = 0; i < photos.length; i++) {
    var cell = $("<div>").addClass("cell");
    var photoImg = $("<img>").addClass("photo")
      .attr("src", photos[i])
      .attr("title", titles[i]);
    var title = $("<p>").text(titles[i]);

    cell.append(photoImg);
    cell.append(title);

    photoImg.click(openPhoto);

    photoImg.mouseover(function() {
      $(this).css("cursor", "pointer");
    });

    photoAlbum.append(cell);
  }

  function openPhoto() {
    var index = $(this).index(".photo");
    var photo = photos[index];
    var title = titles[index];

    var $photoModal = $("<div>").addClass("photo-modal");
    var $photoContainer = $("<div>").addClass("photo-container");
    var $enlargedPhoto = $("<img>").addClass("enlarged-photo")
      .attr("src", photo)
      .attr("alt", title)
      .attr("title", title);

    var $titleText = $("<p>").addClass("title-text").text(title);
    var $counterText = $("<p>").addClass("counter-text").text((index + 1) + " из " + totalImages);

    var $btnContainer = $("<div>").addClass("btn-container");
    var $previousBtn = $("<button>").addClass("previous-btn").text("◀");
    var $nextBtn = $("<button>").addClass("next-btn").text("▶");

    $photoContainer.append($enlargedPhoto, $titleText);
    $btnContainer.append($previousBtn, $counterText, $nextBtn);
    $photoModal.append($photoContainer, $btnContainer);

    $photoModal.on("click", closePhoto);

    $("body").append($photoModal);

    function updatePhoto(index) {
      var newPhoto = photos[index];
      var newTitle = titles[index];
      var newCounter = (index + 1) + " из " + totalImages;

      $counterText.text(newCounter);
      
      $enlargedPhoto.fadeOut(200, function() {
        $enlargedPhoto
          .attr("src", newPhoto)
          .attr("alt", newTitle)
          .attr("title", newTitle)
          .fadeIn(400);
      });
      
      $titleText.fadeOut(200, function() {
        $titleText
          .text(newTitle)
          .fadeIn(200);
      });
    }

    $previousBtn.on("click", function (e) {
      e.stopPropagation();
      index = (index - 1 + totalImages) % totalImages;
      updatePhoto(index);
    });

    $nextBtn.on("click", function (e) {
      e.stopPropagation();
      index = (index + 1) % totalImages;
      updatePhoto(index);
    });

    function closePhoto() {
      $photoModal.fadeOut("fast", function () {
        $photoModal.remove();
      });
    }
  }
});