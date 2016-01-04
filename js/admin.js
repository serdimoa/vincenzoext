/**
 * Created by serdimoa on 05.11.15.
 */
//= ../bower_components/datatables/media/js/jquery.dataTables.js
tinymce.init({
    selector: 'textarea',
    theme: 'modern',
    language_url: '/static/ru.js',
    plugins: [
        'advlist autolink link lists charmap print preview hr anchor pagebreak spellchecker',
        'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime nonbreaking',
        'save table contextmenu directionality emoticons template paste textcolor'
    ],
    toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link | print preview fullpage | forecolor backcolor emoticons'
});
function translit() {
// Символ, на который будут заменяться все спецсимволы
    var space = '-';
// Берем значение из нужного поля и переводим в нижний регистр
    var text = $('#category_name').val().toLowerCase();

// Массив для транслитерации
    var transl = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
        'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sh', 'ъ': space, 'ы': 'y', 'ь': space, 'э': 'e', 'ю': 'yu', 'я': 'ya',
        ' ': space, '_': space, '`': space, '~': space, '!': space, '@': space,
        '#': space, '$': space, '%': space, '^': space, '&': space, '*': space,
        '(': space, ')': space, '-': space, '\=': space, '+': space, '[': space,
        ']': space, '\\': space, '|': space, '/': space, '.': space, ',': space,
        '{': space, '}': space, '\'': space, '"': space, ';': space, ':': space,
        '?': space, '<': space, '>': space, '№': space
    }

    var result = '';
    var curent_sim = '';

    for (i = 0; i < text.length; i++) {
        // Если символ найден в массиве то меняем его
        if (transl[text[i]] != undefined) {
            if (curent_sim != transl[text[i]] || curent_sim != space) {
                result += transl[text[i]];
                curent_sim = transl[text[i]];
            }
        }
        // Если нет, то оставляем так как есть
        else {
            result += text[i];
            curent_sim = text[i];
        }
    }

    result = TrimStr(result);

// Выводим результат
    $('#alias').val(result);

}

function TrimStr(s) {
    s = s.replace(/^-/, '');
    return s.replace(/-$/, '');
}

// Выполняем транслитерацию при вводе текста в поле
$(function () {
    $('#category_name').keyup(function () {
        translit();
        return false;
    });
});

$(window).load(function () {

    $(".delete_item").click(function () {
        var is_delete = confirm("Точно удалить?");
        if (is_delete == true) {
            window.location.href = "/panel/item_delete/" + parseInt(this.name)
        }
    });
    $(".delete_sales").click(function () {
        var is_delete = confirm("Точно удалить?");
        if (is_delete == true) {
            window.location.href = "/panel/sales_delete/" + parseInt(this.name)
        }
    })

});

$('#dts').DataTable({
    "language": {
        "url": "https://cdn.datatables.net/plug-ins/1.10.10/i18n/Russian.json"
    },
    stateSave: true

});
