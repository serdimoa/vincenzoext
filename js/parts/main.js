/**
 * Created by serdimoa on 02.11.15.
 */

if ($('.index_page').length) {
    var cart = window.document.querySelector('.cart');

    var cartItems = cart.querySelector('.cart__count');
}
if (settingsr){
if ( $.inArray('delete_buy_button', settingsr) > -1 ) {
    $('#orderNow').hide();
}
else{
}
    }

var delivery = sessionStorage.getItem('delivery');

if ($("#inputPhone").length) {
    $("#inputPhone").mask("+79999999999", {autoclear: false});
}
if ($("#form_auch-login").length) {
    $("#form_auch-login").mask("+79999999999", {autoclear: false});
}
if ($("#form-phone").length) {
    $("#form-phone").mask("+79999999999", {autoclear: false});
}
if ($("#phone").length) {
    $("#phone").mask("+79999999999", {autoclear: false})
}
var summ;
var dataTable = $('#tableOrder').DataTable({
    "language": {
        "emptyTable": "Корзина пуста"
    }
});
var cache_for_datatable;
var thiss;
function uniqId() {
  return "uniqId"+Math.round(new Date().getTime() + (Math.random() * 1000));
}
$(".sous_select_box a").click(function (e) {
    var data_name = $(this).data("text");
    sous_select(data_name);
    $("#select_sous").nifty('hide');

});
function sous_select(name) {
    var data_items = cache_for_datatable;
    var ids = uniqId();
    dataTable.row.add([
        "<h3>" + data_items['item_name'] + "</h3><small>" + data_items['item_component'] + "</small>",
        "<select id='"+ids+"' class='basic' ><option value=''>Выберите соус</option><option>Аррабиата</option><option>Сливочный</option><option>Песто</option><option>Грибной</option><option>Бешамель</option>",
        "<input type='number' value='1' data-price='" + data_items['item_price'] + "' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
        "<span class='cena'>" + data_items['item_price'] + " <i class='fa fa-rub'></i></span>",
        "<a href='#0' id='" + data_items['item_id'] + "' class='delete'><i class='fa fa-times'></i></a>"
    ]).draw(false);

    $('.basic').fancySelect().on('change.fs', function () {
        localStorage.setItem("cart", JSON.stringify(dataFromTable()));
    });
    thiss = $(this);
    $('#'+ids+' :contains(' + name + ')').prop("selected", true);

    $(".checkOut input[type=number]").on("change", function (e) {
        $('.full span').text(calculateSumm());

    });
    $('.full span').text(calculateSumm());
    iosOverlay({
        text: "Добавлено!",
        duration: 2e3,
        icon: "/static/img/check.png"
    });
    $('.basic').trigger('update.fs');

}
function delivery_func() {
    if (delivery === "undefined" || delivery == null) {
        $("#select_delivery").nifty("show");

    } else {
        $("input:radio[name=group2][value='" + sessionStorage.getItem('delivery') + "']").prop({"checked": true});
    }

}


if ($(".settings, .sale, .aboutus").length) {
    delivery_func();
}

if ($(".settings").length) {
    $.getJSON("/address", "",
        function (data) {
            console.log(JSON.parse(data.result));
            localStorage["memos"] = JSON.stringify(JSON.parse(data.result));
        });

    var items = getFromLocal('memos');
    var index;
    loadList(items);
    // if input is empty disable button
    $('#main-button').prop('disabled', true);
    $('#main-input').keyup(function () {
        if ($(this).val().length !== 0) {
            $('#main-button').prop('disabled', false);
        } else {
            $('#main-button').prop('disabled', true);
        }
    });
    // bind input enter with button submit
    $('#main-input').keypress(function (e) {
        if (e.which === 13) {
            if ($('#main-input').val().length !== 0)
                $('#main-button').click();
        }
    });
    $('#main-button').click(function () {
        var value = $('#main-input').val();
        items.push(value);
        //console.log(items[0]);
        $('#main-input').val('');
        loadList(items);
        storeToLocal('memos', items);
        // set button to
        $('button').prop('disabled', true);
    });
    // delete one item
    $('ul.addrList').delegate("span", "click", function (event) {
        event.stopPropagation();
        index = $('span').index(this);
        $('.addrList li').eq(index).remove();
        items.splice(index, 1);
        storeToLocal('memos', items);

    });

    // edit panel
    $('ul.addrList').delegate('li', 'click', function () {
        index = $('.addrList li').index(this);
        var content = items[index];
        $('#edit-input').val(content);
    });

    $('#edit-button').click(function () {
        items[index] = $('#edit-input').val();
        loadList(items);
        storeToLocal("memos", items);
    });

    // loadList
    function loadList(items) {
        $('.addrList li').remove();
        if (items.length > 0) {
            for (var i = 0; i < items.length; i++) {
                $('ul.addrList').append('<li class= "list-group-item" data-toggle="modal" data-target="#editModal">' + items[i] + '<span class="fa fa-close"></span</li>');
            }
        }
    };

    function storeToLocal(key, items) {
        var allAddress = JSON.stringify(items);
        localStorage[key] = allAddress;
        $.post("/address", {addresses: allAddress})
    }

    function getFromLocal(key) {

        if (localStorage[key]) {
            return JSON.parse(localStorage[key]);
        }
        else
            return [];
    }

}

function initIfhaveSession() {
    var cartValue = localStorage.getItem("cart");
    if (cartValue != null) {
        var cartObj = JSON.parse(cartValue);
        if (cartObj[0].row[0] != "Корзина пуста") {
            cartObj.forEach(function (entry) {
                if (entry.row[1] == null) {
                    dataTable.row.add([
                        entry.row[0],
                        "",
                        "<input type='number' value='" + entry.row[2] + "' data-price='" + entry.row[3] + "' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
                        "<span class='cena'>" + entry.row[3] + " <i class='fa fa-rub'></i></span>",
                        "<a href='#0' id='" + entry.row[4] + "' class='delete'><i class='fa fa-times'></i></a>"
                    ]).draw(false);
                    $(".checkOut input[type=number]").on("change", function (e) {
                        $('.full span').text(calculateSumm());

                    });

                    $('.full span').text(calculateSumm());
                } else {
                    var ids = uniqId();

                    dataTable.row.add([
                        entry.row[0],
                        "<select id='"+ids+"' class='basic'><option value=''>Выберите соус</option><option>Аррабиата</option><option>Сливочный</option><option>Песто</option><option>Грибной</option><option>Бешамель</option>",
                        "<input  type='number' value='" + entry.row[2] + "' data-price='" + entry.row[3] + "' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
                        "<span class='cena'>" + entry.row[3] + " <i class='fa fa-rub'></i></span>",
                        "<a href='#0' id='" + entry.row[4] + "' class='delete'><i class='fa fa-times'></i></a>"
                    ]).draw(false);

                    $('.basic').fancySelect().on('change.fs', function () {
                        localStorage.setItem("cart", JSON.stringify(dataFromTable()));
                    });

                    $('.fancified').on("change", function () {
                        localStorage.setItem("cart", JSON.stringify(dataFromTable()));
                        console.log("basic change ");

                    });
                    $('#'+ids+' :contains(' + entry.row[1] + ')').prop("selected", true);

                    $(".checkOut input[type=number]").on("change", function (e) {
                        $('.full span').text(calculateSumm());

                    });
                    $('.full span').text(calculateSumm());
                }

            });
            $('.basic').trigger('update.fs');
        }
    }
    //console.log(cartObj);
    //dataTable.add.row
}


if ($('.userIsAuch .full_price, .borderLeft .full_price').length) {
//    var full_price = localStorage.getItem("cart_price");
//    $('.full_price').text(full_price);
//    initIfhaveSession();
//    delivery_func();
    $("#adressAuch").select2({
        tags: true

        //data: data
    });
}
$('.userIsAuch h2, .borderLeft  h2 ').click(function () {
    $('.checkOut').addClass('isUp');
});

var tableOrder = $('#tableOrder tbody');

function dataFromTable() {
    var TableData = new Array();
    $('#tableOrder tr').each(function (row, tr) {
        TableData[row] = {
            row: [
                $(tr).find('td:eq(0)').html(),
                $(tr).find('td:eq(1)').find('.fancified option:selected').val(),
                $(tr).find('td:eq(2)').find("input").val(),
                $(tr).find('td:eq(3)').text(),
                $(tr).find('td:eq(4)').find('a').attr('id')
            ]
        }
    });
    TableData.shift();
    return TableData;
}

tableOrder.on('mouseenter', 'tr', function () {
    if ($(this).hasClass('selected')) {
        $(this).removeClass('selected');
    } else {
        dataTable.$('tr.selected').removeClass('selected');
        $(this).addClass('selected');
    }
});

$(".action--like.haslogin").click(function (e) {
    var page = $(this);
    console.log(page);
    $.getJSON('/like_add', {like: $(this).val()},
        function (data) {
            if (data.result == "adfavorited") {
                page.find("i").addClass('fa-heart');
                page.find("i").removeClass('fa-heart-o');
                swal({
                        title: "Ура!",
                        text: "Добавлено в избранное!",
                        timer: 1500,
                        type: "success",
                        showConfirmButton: false
                    }
                );

            }
            else if (data.result == "delete") {
                page.find("i").addClass('fa-heart-o');
                page.find("i").removeClass('fa-heart');
                swal({
                        title: "Упс!",
                        text: "Удалено из избранного!",
                        timer: 1500,
                        type: "error",
                        showConfirmButton: false
                    }
                );
            }
            else if (data.result == 0) {
                swal({
                        title: "Упс!",
                        text: "Что-то пошло не так!",
                        timer: 1500,
                        type: "error",
                        showConfirmButton: false
                    }
                );
            }


        });

});

$('#auch-menu-btn').click(function (event) {
    $.getJSON('/auch', {
            login: $('#inputPhone').val(),
            password: $('#inputPassword').val()
        },
        function (data) {
            if (data.result == 1) {
                swal({
                        title: "Ура!",
                        text: "Вход выполнен успешно!",
                        timer: 2000,
                        type: "success",
                        showConfirmButton: false
                    },
                    function () {
                        location.reload();
                    });
            } else {
                swal({
                    title: "Упс!",
                    text: "Такого пользоваеля не существует, либо пароль введен неправильно",
                    type: "error",
                    showConfirmButton: true
                });
            }
        })


});



$(".select_it").click(function () {
    $.cookie('delivery', $('input:radio[name=delivery]:checked').val());
    sessionStorage.setItem('delivery', $('input:radio[name=delivery]:checked').val());
    $.cookie("localLinkClicked", true);

    window.location.reload();
});

tableOrder.on('mouseleave', 'tr', function () {
    if ($(this).hasClass('selected')) {
        $(this).removeClass('selected');
    } else {
        dataTable.$('tr.selected').removeClass('selected');
        $(this).addClass('selected');
    }
});

function fnGetSelected(oTableLocal) {
    return oTableLocal.$('tr.selected');
}
$(".like_no_admin").click(function () {
    swal({
        title: "Эта функция доступна только для зарегистрированых пользователей<br> <h3 class='swal'>Зарегистрируйся и получи скидку 10%</h3>",
        confirmButtonColor: "#4CAF50",
        text: "",
        type: "info",
        html: true,
        showConfirmButton: true,
        showCancelButton: true,
        confirmButtonText: "Регистрация/Авторизация",
        cancelButtonText: "Позже",
        closeOnConfirm: false
    }, function () {
        document.location = "/site_auch"
    });
});
$('.pw-reset a, #restorePass').click(function () {
    var login = $('#inputPhone');
    if (login.val() != "") {
        $.getJSON('/pwreset', {login: login.val()},
            function (data) {
                console.log(data);
                if (data.result == "sent") {
                    swal("Пароль востановлен!", "Новый пароль отправлен на вашу почту!", "success");
                }
                else if (data.result == 0) {
                    swal("Упс!", "Такого пользователя нет!", "error");
                }
                else if (data.result == 2) {
                    swal({title: "Упс!", text: "Что-то пошло не так!", timer: 2000, showConfirmButton: true});
                }
            })
    }
    else {
        swal("Упс!", "Необходимо ввести телефон!", "warning");
    }

});
function calculateSumm() {
    summ = 0;
    $(".checkOut input[type=number]").each(function () {
        summ += parseInt($(this).val() * $(this).attr("data-price"));
    });
    summ = summ - summ*global_sale/100;

    if ($('.userIsAuch .full_price').length) {
        $('.full_price').text(summ);
    }

    if ($('.borderLeft .full_price').length) {
        $('.full_price').text(summ);
    }
    $.cookie("cart",JSON.stringify(dataFromTable()));
    $.cookie("cart_price",summ);
    localStorage.setItem("cart", JSON.stringify(dataFromTable()));
    localStorage.setItem("cart_price", summ);
    return summ;

}


function unique(arr) {
    var obj = {};

    for (var i = 0; i < arr.length; i++) {
        var str = arr[i];
        obj[str] = true; // запомнить строку в виде свойства объекта
    }

    return Object.keys(obj); // или собрать ключи перебором для IE8-
}
$(".checkOut input[type=number]").keypress(function (event) {
    event = event || window.event;

    if (event.charCode && (event.charCode < 48 || event.charCode > 57)) { // проверка на event.charCode - чтобы пользователь мог нажать backspace, enter, стрелочку назад...

        return false;
    }

    $('.full span').text(calculateSumm());


});


//Удаление из масива значение
function removeA(arr) {
    var what, a = arguments,
        L = a.length,
        ax;
    while (L > 1 && arr.length) {
        what = a[--L];
        $('.slider').anyslider();

        while ((ax = arr.indexOf(what)) !== -1) {
            arr.splice(ax, 1);
        }
    }
    return arr;
}

$(document).keyup(function (e) {
    if (e.keyCode == 27) { // escape key maps to keycode `27`
        $('.popUp').removeClass('isUp');
        $('html').toggleClass('overflowbody');
    }
});


$(".one--buy").click(function () {
    var data_items = jQuery.parseJSON($(this).attr("data-items"));
    if (data_items['sous'] == true) { // todo: set name
        cache_for_datatable = data_items;

        $("#select_sous").nifty("show")


    } else {
        dataTable.row.add([
            "<h3>" + data_items['item_name'] + "</h3><small>" + data_items['item_component'] + "</small>",
            " ",
            "<input type='number' value='1' data-price='" + data_items['item_price'] + "' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
            "<span class='cena'>" + data_items['item_price'] + " <i class='fa fa-rub'></i></span>",
            "<a href='#0' id='" + data_items['item_id'] + "' class='delete'><i class='fa fa-times'></i></a>"
        ]).draw(false);
        $(".checkOut input[type=number]").on("change", function (e) {
            $('.full span').text(calculateSumm());

        });
        $('.full span').text(calculateSumm());
        iosOverlay({
        text: "Добавлено!",
        duration: 2e3,
        icon: "static/img/check.png"
    });
    }
    cartItems.innerHTML = Number(cartItems.innerHTML) + 1;

});

jQuery(document).ready(function () {
    var tableOrder = $('#tableOrder');
    tableOrder.on('click', '.delete', function (e) {
        dataTable.row('.selected').remove().draw(false);
        if ($('.index_page').length) {
            cartItems.innerHTML = Number(cartItems.innerHTML) - 1;
        }
        $('.full span').text(calculateSumm());

    });

}); //ready

$('#orderNow').click(function (event) {
    if (calculateSumm() < 500) {
        swal({
            title: "Ой!",
            text: "Для доставки минимальная сумма заказа составляет 500 рублей",
            type: "error",
            html: true,
            showConfirmButton: true,
            confirmButtonText: "Я понял"
        })
    }
    else {
        window.location.href = "/order";
    }
});

$('.slider__item').click(function (event) {
    $('html').toggleClass('overflowbody');
    $("#one_img").removeAttr("src");
    $(".preloader").show();
    $('.popUp').addClass('isUp');

    $.ajax({
        type: 'POST',
        // Provide correct Content-Type, so that Flask will know how to process it.
        contentType: 'application/json',
        // Encode your data as JSON.
        // This is the type of data you're expecting back from the server.
        dataType: 'json',
        url: '/get_one_item/' + $(this).attr("data-id-item"),
        success: function (e) {
            $("#one_img").attr({
                "src": 'static/upload/' + e.result.imgs
            });
            var item_result = {
                item_id: e.result.item_id,
                item_name: e.result.name,
                item_price: e.result.price,
                item_component: e.result.components,
                item_weight: e.result.weight,
                item_category: e.result.category,
                sous: e.result.sous
            };


            $(".aboutProduct .action--buy").attr({
                "value": e.result.id,
                "data-items": JSON.stringify(item_result)
            });

            arrays_one = (e.result.components).split(",");
            if (arrays_one[0] == "") {
                $(".aboutProduct h3").hide();
            }
            else {
                $(".aboutProduct h3").show();
            }
            $("#one_array").empty();
            $.each(arrays_one, function (i) {
                var li = $('<li/>')
                    .text(arrays_one[i])
                    .appendTo($("#one_array"));
            });
            $("#one_price").html(e.result.price + '<i class="fa fa-rub"></i>');
            $("#one_weight").text(e.result.weight);
            $("#one_name").text(e.result.name);
            if ($.cookie("delivery") == "deliveryincafe" || e.result.cafe_only != true) {
                $(".aboutProduct .action--buy").show();
            } else {
                $(".aboutProduct .action--buy").hide();
            }
            setTimeout(function () {
                $(".preloader").hide()
            }, 500);

            //for (var item_resp in e.response) {
            //
            //}

        }
    });


});
$('.closebtn').click(function (event) {
    $('.popUp').removeClass('isUp');
    $('html').toggleClass('overflowbody');


});


$('.cart, .showCart, .userIsAuch h2,.borderLeft h2').click(function (event) {

    if (calculateSumm() == 0) {
        iosOverlay({
            text: "Корзина пуста",
            duration: 2e3,
            icon: "/static/img/cross.png"
        });
    } else {

        $('.full span').text(calculateSumm());
        $('html').toggleClass('overflowbody');

        $('.checkOut').addClass('isUp');
    }
    ;
});

$('.closezakazbtn').click(function (event) {
    $('.checkOut').removeClass('isUp');
    $('html').toggleClass('overflowbody');


});
/**
 Product Page
 **/
//Function for fixin sidebar
$(function () {
    if ($('.index_page').length) {

        var sidebar = $('#bar');
        var bodywithsidebar = $(".view");
        var cart = $(".cart");
        var top = sidebar.offset().top - parseFloat(sidebar.css('margin-top'));

        $(window).scroll(function (event) {
            var y = $(this).scrollTop();
            if (y >= top) {
                sidebar.addClass('fixed');
                bodywithsidebar.addClass('col-md-offset-2');
                cart.addClass("cartAbsolute cartPerc")
            } else {
                sidebar.removeClass('fixed');
                bodywithsidebar.removeClass('col-md-offset-2');
                cart.removeClass('cartAbsolute cartPerc');
            }
        });
    }
});


window.localLinkClicked = false;


function warning() {
    if ($.cookie('localLinkClicked')) {
        console.log("window page"); //you can put your code here.
        $.removeCookie("localLinkClicked");

    } else {
        console.log("window reload"); //you can put your code here.

        $.removeCookie("localLinkClicked");

        $("#select_delivery").nifty("show");
    }
}
window.onload = warning;

$("a").on("click", function () {
    var url = $(this).attr("href");

    // check if the link is relative or to your domain
    if (!/^http?:\/\/./.test(url) || /http?:\/\/127.0.0.1\:5000/.test(url)) {
        $.cookie("localLinkClicked", true);

    }
});

$(".logoa").click(function (e) {

    window.location.reload();
    $.removeCookie("localLinkClicked");

});
(function (window) {

    'use strict';

    var support = {
            animations: Modernizr.cssanimations
        },
        animEndEventNames = {
            'WebkitAnimation': 'webkitAnimationEnd',
            'OAnimation': 'oAnimationEnd',
            'msAnimation': 'MSAnimationEnd',
            'animation': 'animationend'
        },
        animEndEventName = animEndEventNames[Modernizr.prefixed('animation')],
        onEndAnimation = function (el, callback) {
            var onEndCallbackFn = function (ev) {
                if (support.animations) {
                    if (ev.target != this) return;
                    this.removeEventListener(animEndEventName, onEndCallbackFn);
                }
                if (callback && typeof callback === 'function') {
                    callback.call();
                }
            };
            if (support.animations) {
                el.addEventListener(animEndEventName, onEndCallbackFn);
            } else {
                onEndCallbackFn();
            }
        };

    // from http://www.sberry.me/articles/javascript-event-throttling-debouncing
    function throttle(fn, delay) {
        var allowSample = true;

        return function (e) {
            if (allowSample) {
                allowSample = false;
                setTimeout(function () {
                    allowSample = true;
                }, delay);
                fn(e);
            }
        };
    }

    // sliders - flickity
    if ($('.index_page').length) {
        var sliders = [].slice.call(document.querySelectorAll('.slider')),
        // array where the flickity instances are going to be stored
            flkties = [],
        // grid element
            grid = document.querySelector('.grid'),
        // isotope instance
            iso,
            bLazy,
        // filter ctrls
            filterCtrls = [].slice.call(document.querySelectorAll('.filter > button')),
        // cart
            cart = document.querySelector('.cart'),
            cartItems = cart.querySelector('.cart__count');
    }
    function onArrange() {
        bLazy.revalidate();
    }


    function init() {
        // preload images
        console.log(global_sale);

        if ($('.index_page').length) {
            initIsotope();
            initEvents();

            var $win = $(window);


            bLazy = new Blazy({
                offset: 200,
                success: function () {
                    iso.layout();

                }
            });


            iso.on('arrangeComplete', onArrange);


            // initFlickity();

            delivery_func();
            classie.remove(grid, 'grid--loading');

            var slider = $('.sliders').anyslider({
                interval: 10000,
                showBullets: false,
                showControls: false
            });
            var anyslider = slider.data('anyslider');

            $(".seq-prev").click(function (e) {
                anyslider.prev();

            });

            $(".seq-next").click(function (e) {
                anyslider.next();
            });

            $(".preloader").hide();


        }
        initIfhaveSession();


    }


    function initFlickity() {
        sliders.forEach(function (slider) {
            var flkty = new Flickity(slider, {
                prevNextButtons: false,
                wrapAround: true,
                cellAlign: 'left',
                contain: true,
                resize: false,
                pageDots: false
            });

            // store flickity instances
            flkties.push(flkty);
        });
    }

    function initIsotope() {
        iso = new Isotope(grid, {
            isResizeBound: false,
            itemSelector: '.grid__item',
            percentPosition: true,
            masonry: {
                // use outer width of grid-sizer for columnWidth
                columnWidth: '.grid__sizer'
            },
            transitionDuration: '0.5s'
        });

    }


    function initEvents() {
        filterCtrls.forEach(function (filterCtrl) {
            filterCtrl.addEventListener('click', function () {
                classie.remove(filterCtrl.parentNode.querySelector('.filter__item--selected'), 'filter__item--selected');
                classie.add(filterCtrl, 'filter__item--selected');
                iso.arrange({
                    filter: filterCtrl.getAttribute('data-filter')
                });
                recalcFlickities();
                iso.layout();
                bLazy.revalidate();
            });
        });

        // window resize / recalculate sizes for both flickity and isotope/masonry layouts
        window.addEventListener('resize', throttle(function (ev) {
            recalcFlickities();
            iso.layout();
        }, 50));

        // add to cart
        [].slice.call(grid.querySelectorAll('.grid__item')).forEach(function (item) {
            item.querySelector('.items-buy').addEventListener('click', addToCart);
        });
        //dataTable.
    }


    function addToCart() {
        var data_items = jQuery.parseJSON($(this).attr("data-items"));
        if (data_items['sous'] == "True") {
            cache_for_datatable = data_items;

            $("#select_sous").nifty("show")


        } else {
            dataTable.row.add([
                "<h3>" + data_items['item_name'] + "</h3><small>" + data_items['item_component'] + "</small>",
                " ",
                "<input type='number' value='1' data-price='" + data_items['item_price'] + "' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
                "<span class='cena'>" + data_items['item_price'] + " <i class='fa fa-rub'></i></span>",
                "<a href='#0' id='" + data_items['item_id'] + "' class='delete'><i class='fa fa-times'></i></a>"
            ]).draw(false);
            $(".checkOut input[type=number]").on("change", function (e) {
                $('.full span').text(calculateSumm());

            });
            $('.full span').text(calculateSumm());
            iosOverlay({
                text: "Добавлено!",
                duration: 2e3,
                icon: "static/img/check.png"
            });
            classie.add(cart, 'cart--animate');
            setTimeout(function () {
                cartItems.innerHTML = Number(cartItems.innerHTML) + 1;
            }, 200);
            onEndAnimation(cartItems, function () {
                classie.remove(cart, 'cart--animate');
            });

        }


    }

    function recalcFlickities() {
        for (var i = 0, len = flkties.length; i < len; ++i) {
            flkties[i].resize();
        }
    }

    init();

})(window);



