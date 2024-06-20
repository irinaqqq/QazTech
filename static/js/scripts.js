function changeMainImage(imageUrl) {
    document.getElementById('main-image').src = imageUrl;
}
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
scrollFunction();
};

function scrollFunction() {
if (
document.body.scrollTop > 20 ||
document.documentElement.scrollTop > 20
) {
mybutton.style.display = "block";
} else {
mybutton.style.display = "none";
}
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
document.body.scrollTop = 0;
document.documentElement.scrollTop = 0;
}


function myFunction() {
var x = document.getElementById("myTopnav");
if (x.className === "navbar-nav flex-row borderXwidth d-flex flex-wrap") {
  x.className = "navbar-nav responsive";
} else {
  x.className = "navbar-nav flex-row borderXwidth d-flex flex-wrap";
}
}


$(document).ready(function() {
  var isHovered = false; // Флаг для отслеживания наведения на #hoveredCategoryProducts
  var hoverTimeout; // Переменная для хранения таймаута скрытия #hoveredCategoryProducts

  // Функция для показа товаров
  function showProducts(category_id) {
      // Проверяем размер экрана
      if ($(window).width() < 992) {
          $('#hoveredCategoryProducts').hide(); // Скрываем элемент, если размер экрана меньше 992px
          return; // Завершаем выполнение функции
      }

      $.ajax({
          url: '/get_category_products/',
          method: 'GET',
          data: {'category_id': category_id},
          success: function(data) {
              var products = data.products;
              var limit = 9;
              if (products.length > 0) {
                  var productList = '<div class="row g-5 px-5 my-2">'; // Начинаем с контейнера
                  for (var i = 0; i < Math.min(products.length, limit); i++) {
                      productList += '<div class="col-md-3 mx-3" style="width: 11%; opacity: 0; margin:0; padding:0;">';
                      productList += '<a href="' + products[i].url + '" class="h-100">';
                      productList += '<div class="card h-100" style="box-shadow: none;">';
                      productList += '<img src="' + (products[i].image_url ? products[i].image_url : '{% static "images/placeholder.png" %}') + '" class="card-img-top" alt="' + products[i].name + '" style="height:170px;"/>';
                      productList += '<div class="card-body d-flex" style="padding:0.25rem;">';
                      productList += '<div class="m-auto">';
                      productList += '<h5 class="card-title" style="font-size:1rem;">' + products[i].name + '</h5>';
                      productList += '</div>';
                      productList += '</div>';
                      productList += '</div>';
                      productList += '</a>';
                      productList += '</div>';
                  }
                  productList += '</div>'; // Заканчиваем контейнером
                  $('#hoveredCategoryProducts').html(productList);
                  $('#hoveredCategoryProducts').fadeIn();
                  // Показываем товары с анимацией fadeIn и задержкой
                  $('#hoveredCategoryProducts').find('.row .col-md-3').each(function(index) {
                      $(this).css('animation', 'fadeInFromTop 1s ease ' + (index * 0.2) + 's forwards');
                  });
              } else {
                  $('#hoveredCategoryProducts').hide(); // Скрываем элемент, если нет товаров
              }
          },
          error: function(error) {
              console.log(error);
          }
      });
  }

  // Вызываем функцию при загрузке страницы и изменении размера окна
  $(window).resize(function() {
      showProducts($('.nav-link.active').data('category-id'));
  });

  // Показываем товары при наведении на ссылку в навбаре
  $(".nav-link").mouseenter(function() {
      clearTimeout(hoverTimeout); // Очищаем предыдущий таймаут, если есть
      showProducts($(this).data('category-id'));
  });

  // Скрываем #hoveredCategoryProducts при уходе мыши с .nav-link
  $(".nav-link").mouseleave(function(e) {
      clearTimeout(hoverTimeout); // Очищаем предыдущий таймаут, если есть

      // Задержка перед скрытием #hoveredCategoryProducts
      hoverTimeout = setTimeout(function() {
          if (!isHovered) {
              $('#hoveredCategoryProducts').hide();
          }
      }, 300); // Задержка в миллисекундах (в данном случае 300 мс)
  });

  // Показываем или скрываем #hoveredCategoryProducts при наведении или уходе мыши с него
  $('#hoveredCategoryProducts').mouseenter(function() {
      isHovered = true;
  }).mouseleave(function() {
      isHovered = false;
      $('#hoveredCategoryProducts').hide();
  });
})



$(document).ready(function(){
    $('#feedbackForm').on('submit', function(e){
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(response){
                if(response.success){
                    $('#successMessage').fadeIn().delay(10000).fadeOut();
                    $('#errorMessage').hide();
                    $('#feedbackForm')[0].reset();
                } else {
                    $('#successMessage').hide();
                    $('#errorMessage').show();
                    if(response.errors){
                        if(response.errors.name){
                            $('#nameError').text(response.errors.name);
                        } else {
                            $('#nameError').text('');
                        }
                        if(response.errors.email){
                            $('#emailError').text(response.errors.email);
                        } else {
                            $('#emailError').text('');
                        }
                        if(response.errors.phone){
                            $('#phoneError').text(response.errors.phone);
                        } else {
                            $('#phoneError').text('');
                        }
                        if(response.errors.message){
                            $('#messageError').text(response.errors.message);
                        } else {
                            $('#messageError').text('');
                        }
                    }
                }
            },
            error: function(){
                $('#successMessage').hide();
                $('#errorMessage').show();
            }
        });
    });
});