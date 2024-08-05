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

function previewImage(event, formIndex) {
    var input = event.target;
    var preview = document.getElementById(`image-preview-${formIndex}`);

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }

        reader.readAsDataURL(input.files[0]); // convert to base64 string
    } else {
        preview.style.display = 'none';
        preview.src = '#';
    }
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
                    <div class="custom-file-upload d-flex flex-column">
                        <img id="image-preview-${currentImageFormCount}" src="#" alt="Preview" style="display: none; height: 100px; align-self: center; margin-bottom: 10px;">
                        <input type="file" name="images-${currentImageFormCount}-image" accept="image/*" id="id_images-${currentImageFormCount}-image" class="custom-file-input" onchange="previewImage(event, ${currentImageFormCount})">
                        <label for="id_images-${currentImageFormCount}-image" class="custom-select custom-file-label">Выберите файл</label>
                    </div>
                </div>`;
            imageFormsetDiv.insertAdjacentHTML('beforeend', newImageFormHtml);
            imageTotalForms.setAttribute('value', currentImageFormCount + 1);

            // Reset the event listener for file input change
            const newFileInput = imageFormsetDiv.querySelector(`#id_images-${currentImageFormCount}-image`);
            const newFileLabel = imageFormsetDiv.querySelector(`label[for="id_images-${currentImageFormCount}-image"]`);


            newFileInput.addEventListener('change', function (event) {
                if (this.files && this.files[0]) {
                    const fileName = this.files[0].name;
                    newFileLabel.innerText = fileName;
                    previewImage(event, currentImageFormCount);
                } else {
                    newFileLabel.innerText = 'Выберите файл';
                    const preview = document.getElementById(`image-preview-${currentImageFormCount}`);
                    preview.style.display = 'none';
                    preview.src = '#';
                }
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
            if (this.files && this.files[0]) {
                const fileName = this.files[0].name;
                fileLabels1[index].innerText = fileName;
            } else {
                fileLabels1[index].innerText = 'Выберите файл';
            }
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

function setupDeleteFunctionality() {
    // Обработка кликов по меткам
    const labels = document.querySelectorAll('.custom-file-label');
    
    labels.forEach(label => {
        label.addEventListener('click', function() {
            const index = label.getAttribute('data-index');
            const relatedCheckbox = document.querySelector(`input[id$="-${index}-DELETE"]`);
            const preview = document.getElementById(`image-preview-${index}`);
            if (relatedCheckbox) {
                relatedCheckbox.checked = true;
                label.style.display = 'none';
                if (preview) {
                    preview.style.display = 'none';
                }
            }
        });
    });

    // Скрыть все DELETE чекбоксы
    const checkboxes = document.querySelectorAll('input[type="checkbox"][id*="-DELETE"]');
    checkboxes.forEach(checkbox => {
        checkbox.classList.add('hidden-checkbox');
    });

    // Обработка изменений состояния DELETE чекбоксов
    const deleteCheckboxes = document.querySelectorAll('input[type="checkbox"][name*="-DELETE"]');
    deleteCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const descriptionForm = checkbox.closest('.description-form');
            if (checkbox.checked) {
                if (descriptionForm) {
                    descriptionForm.style.display = 'none';
                }
            } else {
                if (descriptionForm) {
                    descriptionForm.style.display = 'block';
                }
            }
        });
    });
}

function setupTableSorting() {
    const indexHeader = document.getElementById('index-header');
    const categoryHeader = document.getElementById('category-header');
    const nameHeader = document.getElementById('name-header');
    const table = indexHeader ? indexHeader.closest('table') : null;
    const tbody = table ? table.querySelector('tbody') : null;
    let isIndexAscending = true;
    let isCategoryAscending = true;
    let isNameAscending = true;

    if (indexHeader) {
        // Устанавливаем начальный порядок сортировки по номеру
        indexHeader.classList.add('ascending');

        indexHeader.addEventListener('click', function () {
            sortTable('index');
        });
    }

    if (categoryHeader) {
        categoryHeader.addEventListener('click', function () {
            sortTable('category');
        });
    }

    if (nameHeader) {
        nameHeader.addEventListener('click', function () {
            sortTable('name');
        });
    }

    function sortTable(type) {
        if (!tbody) return;

        const rows = Array.from(tbody.querySelectorAll('tr'));

        rows.sort((a, b) => {
            let aValue, bValue;

            if (type === 'index') {
                aValue = parseInt(a.children[0].innerText.trim());
                bValue = parseInt(b.children[0].innerText.trim());
            } else if (type === 'category') {
                aValue = a.children[1].innerText.trim().toLowerCase();
                bValue = b.children[1].innerText.trim().toLowerCase();
            } else if (type === 'name') {
                aValue = a.children[2].innerText.trim().toLowerCase();
                bValue = b.children[2].innerText.trim().toLowerCase();
            }

            if (type === 'index') {
                return aValue - bValue;
            } else {
                return aValue.localeCompare(bValue);
            }
        });

        // Изменяем порядок строк в зависимости от текущего направления сортировки
        if (type === 'index' && indexHeader) {
            if (!isIndexAscending) {
                rows.reverse();
            }
            isIndexAscending = !isIndexAscending;
            indexHeader.classList.toggle('ascending', isIndexAscending);
            indexHeader.classList.toggle('descending', !isIndexAscending);
            if (categoryHeader) {
                categoryHeader.classList.remove('ascending', 'descending');
            }
            if (nameHeader) {
                nameHeader.classList.remove('ascending', 'descending');
            }
        } else if (type === 'category' && categoryHeader) {
            if (!isCategoryAscending) {
                rows.reverse();
            }
            isCategoryAscending = !isCategoryAscending;
            categoryHeader.classList.toggle('ascending', isCategoryAscending);
            categoryHeader.classList.toggle('descending', !isCategoryAscending);
            if (indexHeader) {
                indexHeader.classList.remove('ascending', 'descending');
            }
            if (nameHeader) {
                nameHeader.classList.remove('ascending', 'descending');
            }
        } else if (type === 'name' && nameHeader) {
            if (!isNameAscending) {
                rows.reverse();
            }
            isNameAscending = !isNameAscending;
            nameHeader.classList.toggle('ascending', isNameAscending);
            nameHeader.classList.toggle('descending', !isNameAscending);
            if (indexHeader) {
                indexHeader.classList.remove('ascending', 'descending');
            }
            if (categoryHeader) {
                categoryHeader.classList.remove('ascending', 'descending');
            }
        }

        // Перерисовываем таблицу с учетом нового порядка строк
        rows.forEach((row, index) => {
            tbody.appendChild(row);
        });
    }
}

// Функция для настройки фильтрации по категории
function setupCategoryFilter() {
    const categorySelect = document.getElementById('category-select');
    const productsTable = document.getElementById('products-table');
    const tbody = productsTable ? productsTable.querySelector('tbody') : null;

    if (categorySelect && productsTable && tbody) {
        categorySelect.addEventListener('change', function () {
            const selectedCategoryId = categorySelect.value;
            const rows = tbody.querySelectorAll('tr');

            rows.forEach(row => {
                const categoryCell = row.children[1].innerText.trim();
                if (selectedCategoryId === 'all' || categoryCell === selectedCategoryId) {
                    row.style.display = ''; // Показываем строку
                } else {
                    row.style.display = 'none'; // Скрываем строку
                }
            });
        });
    }
}


function togglePassword(userId) {
    var passwordField = document.getElementById(`plain_password_${userId}`);
    var eyeIcon = document.getElementById(`eyeIcon_${userId}`);

    if (passwordField.textContent === "*******") {
        passwordField.textContent = document.getElementById(`initial_password_${userId}`).textContent;
        eyeIcon.classList.remove('fa-eye');
        eyeIcon.classList.add('fa-eye-slash');
    } else {
        passwordField.textContent = "*******";
        eyeIcon.classList.remove('fa-eye-slash');
        eyeIcon.classList.add('fa-eye');
    }
}

function updateFeedbacksReadStatus() {
    // Проверяем, находимся ли мы на странице отзывов
    if (window.location.pathname === '/myadmin/feedbacks/') {
        fetch('/myadmin/update_feedbacks_read_status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()  // Функция для получения CSRF-токена
            },
            body: JSON.stringify({}),
        })
        .then(response => {
            if (response.ok) {
                console.log('Статусы прочтения отзывов успешно обновлены.');
                // Дополнительные действия при необходимости
            } else {
                console.error('Ошибка при обновлении статусов прочтения отзывов.');
            }
        })
        .catch(error => {
            console.error('Ошибка при отправке запроса:', error);
        });
    }
}

function getCSRFToken() {
    // Функция для получения CSRF-токена из cookies
    const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)[1];
    return csrfToken;
}

function setupCategoryDropdown() {
    const fields = {
        1: ['processor', 'motherboard', 'ram', 'storage', 'power-supply', 'operating-system', 'screen-size', 'screen-resolution', 'keyboard-backlight'],
        2: ['processor', 'motherboard', 'ram', 'storage', 'power-supply', 'operating-system', 'screen-size', 'form-factor', 'keyboard-set'],
        3: ['processor', 'motherboard', 'ram', 'storage', 'power-supply', 'operating-system', 'screen-size', 'keyboard-set'],
        4: ['processor', 'motherboard', 'ram', 'storage', 'power-supply', 'operating-system', 'screen-size', 'touch-screen', 'screen-type', 'webcam'],
        5: ['processor', 'motherboard', 'ram', 'storage', 'power-supply', 'operating-system', 'graphics', 'screen-size', 'keyboard-set'],
        6: ['processor', 'motherboard', 'ram', 'storage', 'power-supply', 'operating-system'],
        7: ['processor', 'motherboard', 'ram', 'storage', 'power-supply', 'operating-system', 'controller', 'size']
    };

    // Делегирование события изменения в выпадающем списке
    $(document).on('change', 'select[id^=id_product_items-][id$=-category]', function() {
        var selectedValue = $(this).val();
        var $form = $(this).closest('.row.g-3.needs-validation');

        // Скрыть все специфичные поля
        $form.find('.specific-field').hide();
        
        $form.find('#quantity-field, #more-notes').css('display', 'flex');
        $form.find('#category-container').removeClass('col-sm-12').addClass('col-sm-6');
        $('#add-product, #send-button').css('display', 'flex');

        // Показать поля на основе выбранной категории
        if (fields[selectedValue]) {
            fields[selectedValue].forEach(function(field) {
                $form.find('#' + field + '-field, #' + field + '-notes-field').css('display', 'flex');
            });
        }
    });
}




function updateOrderStatus(status, orderId) {
    $.ajax({
        url: updateOrderStatusUrl,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': getCSRFToken(),
            'order_id': orderId,
            'status': status
        },
        success: function(data) {
            if (data.success) {
                // Обновление успешно выполнено
                $('#order-row-' + orderId).load(location.href + ' #order-row-' + orderId);
            } else {
                // Обработка ошибок, если необходимо
            }
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText);
            // Обработка ошибок AJAX запроса
        }
    });
}

function addProductItem(){
    let productItemCounter = 0;
    const productTotalForms = document.getElementById('id_product_items-TOTAL_FORMS');
    const productItemsContainer = document.getElementById('product-items-formset');

    const categoryDataElement = document.getElementById('category-container');
    const categories = JSON.parse(categoryDataElement.getAttribute('data-categories'));

    const processorField = document.getElementById('processor-field');
    const processors = JSON.parse(processorField.getAttribute('data-processors'));

    const motherboardField = document.getElementById('motherboard-field');
    const motherboards = JSON.parse(motherboardField.getAttribute('data-motherboards'));

    const ramField = document.getElementById('ram-field');
    const rams = JSON.parse(ramField.getAttribute('data-rams'));

    const storageField = document.getElementById('storage-field');
    const storages = JSON.parse(storageField.getAttribute('data-storages'));

    const graphicsField = document.getElementById('graphics-field');
    const graphics = JSON.parse(graphicsField.getAttribute('data-graphics'));

    const operatingSystemField = document.getElementById('operating-system-field');
    const operatingSystems = JSON.parse(operatingSystemField.getAttribute('data-operating-systems'));

    const screenSizeField = document.getElementById('screen-size-field');
    const screenSizes = JSON.parse(screenSizeField.getAttribute('data-screen-sizes'));

    const screenTypeField = document.getElementById('screen-type-field');
    const screenTypes = JSON.parse(screenTypeField.getAttribute('data-screen-types'));

    const screenResolutionField = document.getElementById('screen-resolution-field');
    const screenResolutions = JSON.parse(screenResolutionField.getAttribute('data-screen-resolutions'));
    
    const touchScreenField = document.getElementById('touch-screen-field');
    const touchScreens = JSON.parse(touchScreenField.getAttribute('data-touch-screens'));
    
    const formFactorField = document.getElementById('form-factor-field');
    const formFactors = JSON.parse(formFactorField.getAttribute('data-form-factors'));

    const webcamField = document.getElementById('webcam-field');
    const webcams = JSON.parse(webcamField.getAttribute('data-webcams'));

    const keyboardSetField = document.getElementById('keyboard-set-field');
    const keyboardSets = JSON.parse(keyboardSetField.getAttribute('data-keyboard-sets'));

    const keyboardBacklightField = document.getElementById('keyboard-backlight-field');
    const keyboardBacklights = JSON.parse(keyboardBacklightField.getAttribute('data-keyboard-backlights'));

    const powerSupplyField = document.getElementById('power-supply-field');
    const powerSupplies = JSON.parse(powerSupplyField.getAttribute('data-power-supplies'));

    const sizeField = document.getElementById('size-field');
    const sizes = JSON.parse(sizeField.getAttribute('data-sizes'));

    const controllerField = document.getElementById('controller-field');
    const controllers = JSON.parse(controllerField.getAttribute('data-controllers'));

    document.getElementById('add-product-item').addEventListener('click', function () {
        productItemCounter++;

        // Создание контейнера для нового продукта
        let newProductItem = document.createElement('div');
        newProductItem.classList.add('row', 'g-3', 'needs-validation');
        newProductItem.id = 'product-item-' + productItemCounter;

        newProductItem.innerHTML = `
            <!-- Category -->
            <input type="checkbox" name="product_items-${productItemCounter}-DELETE" id="id_product_items-${productItemCounter}-DELETE" class="hidden-checkbox">
            <div class="col-sm-12" id="category-container">
                <label for="id_product_items-${productItemCounter}-category" class="form-label">Категория</label>
                <select name="product_items-${productItemCounter}-category" id="id_product_items-${productItemCounter}-category" class="ui fluid search dropdown" required>
                    <option value="" disabled selected>Выберите категорию</option>
                    ${categories.map(category => `
                        <option value="${category.id}">${category.name}</option>
                    `).join('')}
                </select>
            </div>
            <!-- Quantity -->
            <div class="col-sm-6 flex-column specific-field" id="quantity-field">
                <label for="id_product_items-${productItemCounter}-quantity" class="form-label">Количество</label>
                <input type="number" name="product_items-${productItemCounter}-quantity" required id="id_product_items-${productItemCounter}-quantity" class="form-control" placeholder="Введите количество">
            </div>
            
            <!-- Processors -->
            <div class="col-sm-6 flex-column specific-field" id="processor-field">
                <label for="id_product_items-${productItemCounter}-processors" class="form-label">Процессор</label>
                <select name="product_items-${productItemCounter}-processors" id="id_product_items-${productItemCounter}-processors" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите процессор</option>
                        <option value="" disabled selected>Выберите процессор</option>
                        ${processors.map(processor => `
                            <option value="${processor.id}">${processor.name}</option>
                        `).join('')}
                </select>                
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="processor-notes-field">
                <textarea name="product_items-${productItemCounter}-processor_notes" class="form-control mt-2" placeholder="Примечание о процессорe" rows="2"></textarea>
            </div>
            
            <!-- Motherboards -->
            <div class="col-sm-6 flex-column specific-field" id="motherboard-field">
                <label for="id_product_items-${productItemCounter}-motherboards" class="form-label">Материнская плата</label>
                <select name="product_items-${productItemCounter}-motherboards" id="id_product_items-${productItemCounter}-motherboards" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите материнскую плату</option>
                        ${motherboards.map(motherboard => `
                            <option value="${motherboard.id}">${motherboard.name}</option>
                        `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="motherboard-notes-field">
                <textarea name="product_items-${productItemCounter}-motherboard_notes" class="form-control mt-2" placeholder="Примечание о материнской плате" rows="2"></textarea>
            </div>
            
            <!-- RAM -->
            <div class="col-sm-6 flex-column specific-field" id="ram-field">
                <label for="id_product_items-${productItemCounter}-rams" class="form-label">Оперативная память</label>
                <select name="product_items-${productItemCounter}-rams" id="id_product_items-${productItemCounter}-rams" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите оперативную память</option>
                    ${rams.map(ram => `
                        <option value="${ram.id}">${ram.size} ГБ (${ram.type})</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="ram-notes-field">
                <textarea name="product_items-${productItemCounter}-ram_notes" class="form-control mt-2" placeholder="Примечание об оперативной памяти" rows="2"></textarea>        
            </div>
            
            <!-- Storage -->
            <div class="col-sm-6 flex-column specific-field" id="storage-field">
                <label for="id_product_items-${productItemCounter}-storages" class="form-label">Накопители</label>
                <select name="product_items-${productItemCounter}-storages" id="id_product_items-${productItemCounter}-storages" class="ui fluid search dropdown" multiple>
                    <option value="" disabled selected>Выберите накопители</option>
                    ${storages.map(storage => `
                        <option value="${storage.id}">${storage.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="storage-notes-field">
                <textarea name="product_items-${productItemCounter}-storage_notes" class="form-control mt-2" placeholder="Примечание о накопителях" rows="2"></textarea>           
            </div>            
            <!-- Graphics -->
            <div class="col-sm-6 flex-column specific-field" id="graphics-field">
                <label for="id_product_items-${productItemCounter}-graphics" class="form-label">Видеокарта</label>
                <select name="product_items-${productItemCounter}-graphics" id="id_product_items-${productItemCounter}-graphics" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите размер памяти видеокарты</option>
                    ${graphics.map(graphic => `
                        <option value="${graphic.id}">${graphic.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="graphics-notes-field">
                <textarea name="product_items-${productItemCounter}-graphics_notes" class="form-control mt-2" placeholder="Примечание о графике" rows="2"></textarea>           
            </div>
            
            <!-- Operating Systems -->
            <div class="col-sm-6 flex-column specific-field" id="operating-system-field">
                <label for="id_product_items-${productItemCounter}-operating_systems" class="form-label">Операционная система</label>
                <select name="product_items-${productItemCounter}-operating_systems" id="id_product_items-${productItemCounter}-operating_systems" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите операционную систему</option>
                    ${operatingSystems.map(operatingSystem => `
                        <option value="${operatingSystem.id}">${operatingSystem.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="operating-system-notes-field">
                <textarea name="product_items-${productItemCounter}-operating_system_notes" class="form-control mt-2" placeholder="Примечание об операционной системе" rows="2"></textarea>         
            </div>
            
            <!-- Screen Sizes -->
            <div class="col-sm-6 flex-column specific-field" id="screen-size-field">
                <label for="id_product_items-${productItemCounter}-screen_sizes" class="form-label">Размер экрана</label>
                <select name="product_items-${productItemCounter}-screen_sizes" id="id_product_items-${productItemCounter}-screen_sizes" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите размер экрана</option>
                    ${screenSizes.map(screenSize => `
                        <option value="${screenSize.id}">${screenSize.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="screen-size-notes-field">
                <textarea name="product_items-${productItemCounter}-screen_size_notes" class="form-control mt-2" placeholder="Примечание о размере экрана" rows="2"></textarea>        
            </div>
            
            <!-- Screen Types -->
            <div class="col-sm-6 flex-column specific-field" id="screen-type-field">
                <label for="id_product_items-${productItemCounter}-screen_types" class="form-label">Тип экрана</label>
                <select name="product_items-${productItemCounter}-screen_types" id="id_product_items-${productItemCounter}-screen_types" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите тип экрана</option>
                    ${screenTypes.map(screenType => `
                        <option value="${screenType.id}">${screenType.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="screen-type-notes-field">
                <textarea name="product_items-${productItemCounter}-screen_type_notes" class="form-control mt-2" placeholder="Примечание о типе экрана" rows="2"></textarea>       
            </div>
            
            <!-- Screen Resolutions -->
            <div class="col-sm-6 flex-column specific-field" id="screen-resolution-field">
                <label for="id_product_items-${productItemCounter}-screen_resolutions" class="form-label">Разрешение экрана</label>
                <select name="product_items-${productItemCounter}-screen_resolutions" id="id_product_items-${productItemCounter}-screen_resolutions" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите разрешение экрана</option>
                    ${screenResolutions.map(screenResolution => `
                        <option value="${screenResolution.id}">${screenResolution.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="screen-resolution-notes-field">
                <textarea name="product_items-${productItemCounter}-screen_resolution_notes" class="form-control mt-2" placeholder="Примечание о разрешении экрана" rows="2"></textarea>      
            </div>
            
            <!-- Touch Screens -->
            <div class="col-sm-6 flex-column specific-field" id="touch-screen-field">
                <label for="id_product_items-${productItemCounter}-touch_screens" class="form-label">Тачскрин</label>
                <select name="product_items-${productItemCounter}-touch_screens" id="id_product_items-${productItemCounter}-touch_screens" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите тачскрин</option>
                    ${touchScreens.map(touchScreen => `
                        <option value="${touchScreen.id}">${touchScreen.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="touch-screen-notes-field">
                <textarea name="product_items-${productItemCounter}-touch_screen_notes" class="form-control mt-2" placeholder="Примечание о тачскрине" rows="2"></textarea>         
            </div>
            
            <!-- Form Factors -->
            <div class="col-sm-6 flex-column specific-field" id="form-factor-field">
                <label for="id_product_items-${productItemCounter}-form_factors" class="form-label">Форм-фактор</label>
                <select name="product_items-${productItemCounter}-form_factors" id="id_product_items-${productItemCounter}-form_factors" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите форм-фактор</option>
                    ${formFactors.map(formFactor => `
                        <option value="${formFactor.id}">${formFactor.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="form-factor-notes-field">
                <textarea name="product_items-${productItemCounter}-form_factor_notes" class="form-control mt-2" placeholder="Примечание о форм-факторе" rows="2"></textarea>         
            </div>
            
            <!-- Webcams -->
            <div class="col-sm-6 flex-column specific-field" id="webcam-field">
                <label for="id_product_items-${productItemCounter}-webcams" class="form-label">Веб-камера</label>
                <select name="product_items-${productItemCounter}-webcams" id="id_product_items-${productItemCounter}-webcams" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите веб-камеру</option>
                    ${webcams.map(webcam => `
                        <option value="${webcam.id}">${webcam.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="webcam-notes-field">
                <textarea name="product_items-${productItemCounter}-webcam_notes" class="form-control mt-2" placeholder="Примечание о веб-камере" rows="2"></textarea>          
            </div>
            
            <!-- Keyboard Sets -->
            <div class="col-sm-6 flex-column specific-field" id="keyboard-set-field">
                <label for="id_product_items-${productItemCounter}-keyboard_sets" class="form-label">Клавиатурный набор</label>
                <select name="product_items-${productItemCounter}-keyboard_sets" id="id_product_items-${productItemCounter}-keyboard_sets" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите клавиатурный набор</option>
                    ${keyboardSets.map(keyboardSet => `
                        <option value="${keyboardSet.id}">${keyboardSet.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="keyboard-set-notes-field">
                <textarea name="product_items-${productItemCounter}-keyboard_set_notes" class="form-control mt-2" placeholder="Примечание о клавиатурном наборе" rows="2"></textarea>           
            </div>
            
            <!-- Keyboard Backlights -->
            <div class="col-sm-6 flex-column specific-field" id="keyboard-backlight-field">
                <label for="id_product_items-${productItemCounter}-keyboard_backlights" class="form-label">Подсветка клавиатуры</label>
                <select name="product_items-${productItemCounter}-keyboard_backlights" id="id_product_items-${productItemCounter}-keyboard_backlights" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите подсветку клавиатуры</option>
                    ${keyboardBacklights.map(keyboardBacklight => `
                        <option value="${keyboardBacklight.id}">${keyboardBacklight.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="keyboard-backlight-notes-field">
                <textarea name="product_items-${productItemCounter}-keyboard_backlight_notes" class="form-control mt-2" placeholder="Примечание о подсветке клавиатуры" rows="2"></textarea>         
            </div>
            
            <!-- Power Supplies -->
            <div class="col-sm-6 flex-column specific-field" id="power-supply-field">
                <label for="id_product_items-${productItemCounter}-power_supplies" class="form-label">Блок питания</label>
                <select name="product_items-${productItemCounter}-power_supplies" id="id_product_items-${productItemCounter}-power_supplies" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите блок питания</option>
                    ${powerSupplies.map(powerSupply => `
                        <option value="${powerSupply.id}">${powerSupply.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="power-supply-notes-field">
                <textarea name="product_items-${productItemCounter}-power_supply_notes" class="form-control mt-2" placeholder="Примечание о блоке питания" rows="2"></textarea>         
            </div>
            
            <!-- Sizes -->
            <div class="col-sm-6 flex-column specific-field" id="size-field">
                <label for="id_product_items-${productItemCounter}-sizes" class="form-label">Размеры</label>
                <select name="product_items-${productItemCounter}-sizes" id="id_product_items-${productItemCounter}-sizes" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите размер</option>
                    ${sizes.map(size => `
                        <option value="${size.id}">${size.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="size-notes-field">
                <textarea name="product_items-${productItemCounter}-size_notes" class="form-control mt-2" placeholder="Примечание о размерах" rows="2"></textarea>        
            </div>
            
            <!-- Controllers -->
            <div class="col-sm-6 flex-column specific-field" id="controller-field">
                <label for="id_product_items-${productItemCounter}-controllers" class="form-label">Контроллеры</label>
                <select name="product_items-${productItemCounter}-controllers" id="id_product_items-${productItemCounter}-controllers" class="ui fluid search dropdown">
                    <option value="" disabled selected>Выберите контроллер</option>
                    ${controllers.map(controller => `
                        <option value="${controller.id}">${controller.name}</option>
                    `).join('')}
                </select>
            </div>
            <div class="col-sm-6 flex-column justify-content-end specific-field" id="controller-notes-field">
                <textarea name="product_items-${productItemCounter}-controller_notes" class="form-control mt-2" placeholder="Примечание о контроллерах" rows="2"></textarea>        
            </div>
            
            <!-- Notes -->
                <div class="col-sm-12 flex-column specific-field" id="more-notes">
                    <label for="id_product_items-0-notes" class="form-label">Дополнительные примечания</label>
                    <textarea name="product_items-0-notes" id="id_product_items-0-notes" class="form-control" placeholder="Напишите дополнительные примечания" rows="4"></textarea>
                </div>
            <div class="col-sm-12 mt-3">
            <label class="custom-select custom-file-label btn btn-danger" data-index="${productItemCounter}" id="delete-product-item-${productItemCounter}">Удалить</label>
            </div>
        </div>
    </div>
</div>
</div>
</div>`;
document.getElementById('product-items-formset').appendChild(newProductItem);

productItemsContainer.addEventListener('click', function (event) {
    if (event.target && event.target.matches('.custom-select.custom-file-label.btn.btn-danger')) {
        const index = event.target.getAttribute('data-index');
        handleDeleteProductItem(index);
    }
});

productTotalForms.setAttribute('value', productItemCounter + 1)
$('.ui.dropdown').dropdown();
});
}

function handleDeleteProductItem(index) {
    const checkbox = document.getElementById(`id_product_items-${index}-DELETE`);
    const productItem = document.getElementById(`product-item-${index}`);
    
    if (checkbox && productItem) {
        checkbox.checked = true;
        productItem.remove();
    }
}

// Initialize all scripts when the document is ready
$(document).ready(function() {
    initBackToTopButton();
    initShowProductsOnHover();
    initFeedbackForm();
    initDropdownMenus();
    initFormsets();
    addProductItem();
    setupDeleteFunctionality();
    setupTableSorting();
    setupCategoryFilter();
    updateFeedbacksReadStatus();
    setupCategoryDropdown();
});



function toggleDetails(index) {
    var detailsRow = document.getElementById('details-' + index);
    var button = document.getElementById('toggle-button-' + index);
    
    if (detailsRow.style.display === 'none' || detailsRow.style.display === '') {
        detailsRow.style.display = 'table-row';
        button.textContent = 'Скрыть';
    } else {
        detailsRow.style.display = 'none';
        button.textContent = 'Показать';
    }
}
