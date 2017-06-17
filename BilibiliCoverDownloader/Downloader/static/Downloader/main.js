var main = function() {
  function setBackgroundImage() {
    var imgs = ['images/bg-img-1.jpg', 'images/bg-img-2.jpg', 'images/bg-img-3.jpg'];
    var index = Math.floor(Math.random() * (imgs.length));
    $('body').css('background-image', 'url('+imgs[index]+')');
  }
  setBackgroundImage();
}

$(document).ready(main);
