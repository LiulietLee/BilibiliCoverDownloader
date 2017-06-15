var main = function() {
  function setBackgroundImage() {
    var imgs = ['css/img/bg-img-1.jpg', 'css/img/bg-img-2.jpg', 'css/img/bg-img-3.jpg'];
    var index = Math.floor(Math.random() * (imgs.length));
    $('body').css('background-image', 'url('+imgs[index]+')');
  }
  setBackgroundImage();
}

$(document).ready(main);
