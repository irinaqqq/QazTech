// Function to change the main image
function changeMainImage(imageUrl) {
    document.getElementById('main-image').src = imageUrl;
}

// Function to initialize the back-to-top button
function initBackToTopButton() {
    let mybutton = document.getElementById("btn-back-to-top");

    if (mybutton) {
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
    }
}

// Function to handle navbar toggle
function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "navbar-nav flex-row borderXwidth d-flex flex-wrap") {
        x.className = "navbar-nav responsive";
    } else {
        x.className = "navbar-nav flex-row borderXwidth d-flex flex-wrap";
    }
}

// Function to show products on hover
function initShowProductsOnHover() {
    var isHovered = false; // Флаг для отслеживания наведения на #hoveredCategoryProducts
    var hoverTimeout; // Переменная для хранения таймаута скрытия #hoveredCategoryProducts

    // Функция для показа товаров
    function showProducts(category_id) {
        // Проверяем размер экрана
        if ($(window).width() < 1275) {
            $('#hoveredCategoryProducts').hide(); // Скрываем элемент, если размер экрана меньше 1275px
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
}

// Function to handle feedback form submission
function initFeedbackForm() {
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
}

// Function to initialize dropdown menus
function initDropdownMenus() {
    $('.ui.dropdown').dropdown({
        fullTextSearch: true,
        match: 'text',
        message: {
            noResults: 'Нету результатов'
        },
    });
}

// Function to initialize image and description formsets
function initFormsets() {
    // Handle image formset
    const addImageButton = document.getElementById('add-image-form');
    const imageTotalForms = document.getElementById('id_images-TOTAL_FORMS');

    if (addImageButton) {
        addImageButton.addEventListener('click', function () {
            const imageFormsetDiv = document.getElementById('image-formset');
            const currentImageFormCount = imageFormsetDiv.getElementsByClassName('image-form').length;
            const newImageFormHtml = `
                <div class="image-form">
                    <div class="custom-file-upload">
                        <input type="file" name="images-${currentImageFormCount}-image" accept="image/*" id="id_images-${currentImageFormCount}-image" class="custom-file-input">
                        <label for="id_images-${currentImageFormCount}-image" class="custom-select custom-file-label">Выберите файл</label>
                    </div>
                </div>`;
            imageFormsetDiv.insertAdjacentHTML('beforeend', newImageFormHtml);
            imageTotalForms.setAttribute('value', currentImageFormCount + 1);

            // Reset the event listener for file input change
            const newFileInput = imageFormsetDiv.querySelector(`#id_images-${currentImageFormCount}-image`);
            const newFileLabel = imageFormsetDiv.querySelector(`label[for="id_images-${currentImageFormCount}-image"]`);

            newFileInput.addEventListener('change', function () {
                const fileName = this.files[0].name;
                newFileLabel.innerText = fileName;
            });
        });
    }

    // Handle description formset
    const addDescriptionButton = document.getElementById('add-description-form');
    const descriptionTotalForms = document.getElementById('id_descriptions-TOTAL_FORMS');

    if (addDescriptionButton) {
        addDescriptionButton.addEventListener('click', function () {
            const descriptionFormsetDiv = document.getElementById('description-formset');
            const currentDescriptionFormCount = descriptionFormsetDiv.getElementsByClassName('description-form').length;
            const newDescriptionFormHtml = `
                <div class="description-form row g-3">
                    <div class="col-sm-6">
                        <label for="id_descriptions-${currentDescriptionFormCount}-title" class="form-label">Заголовок</label>
                        <input type="text" name="descriptions-${currentDescriptionFormCount}-title" maxlength="255" id="id_descriptions-${currentDescriptionFormCount}-title" class="form-control" placeholder="Введите заголовок текста">
                    </div>
                    <div class="col-sm-6 d-flex flex-column justify-content-end">
                        <input type="file" name="descriptions-${currentDescriptionFormCount}-image" accept="image/*" id="id_descriptions-${currentDescriptionFormCount}-image" class="custom-file-input">
                        <label for="id_descriptions-${currentDescriptionFormCount}-image" class="custom-select custom-file-label">Выберите изображение</label>
                    </div>
                    <div class="col-sm-12">
                        <label for="id_descriptions-${currentDescriptionFormCount}-text" class="form-label">Описание:</label>
                        <textarea name="descriptions-${currentDescriptionFormCount}-text" cols="40" rows="10" id="id_descriptions-${currentDescriptionFormCount}-text" class="form-control" style="min-height: 105px;"></textarea>
                    </div>
                </div>`;
            descriptionFormsetDiv.insertAdjacentHTML('beforeend', newDescriptionFormHtml);
            descriptionTotalForms.setAttribute('value', currentDescriptionFormCount + 1);

            // Reset the event listener for file input change
            const newFileInput = descriptionFormsetDiv.querySelector(`#id_descriptions-${currentDescriptionFormCount}-image`);
            const newFileLabel = descriptionFormsetDiv.querySelector(`label[for="id_descriptions-${currentDescriptionFormCount}-image"]`);

            newFileInput.addEventListener('change', function () {
                const fileName = this.files[0].name;
                newFileLabel.innerText = fileName;
            });
        });
    }

    // Event listeners for file inputs in existing forms
    const fileInputs1 = document.querySelectorAll('#image-formset input[type="file"]');
    const fileLabels1 = document.querySelectorAll('#image-formset .custom-file-label');

    fileInputs1.forEach((fileInput, index) => {
        fileInput.addEventListener('change', function () {
            const fileName = this.files[0].name;
            fileLabels1[index].innerText = fileName;
        });
    });

    // For second form (product description)
    const fileInputs2 = document.querySelectorAll('#description-formset input[type="file"]');
    const fileLabels2 = document.querySelectorAll('#description-formset .custom-file-label');

    fileInputs2.forEach((fileInput, index) => {
        fileInput.addEventListener('change', function () {
            const fileName = this.files[0].name;
            fileLabels2[index].innerText = fileName;
        });
    });
}

// Initialize all scripts when the document is ready
$(document).ready(function() {
    initBackToTopButton();
    initShowProductsOnHover();
    initFeedbackForm();
    initDropdownMenus();
    initFormsets();
});
