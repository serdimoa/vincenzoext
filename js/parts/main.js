/**
 * Created by serdimoa on 02.11.15.
 */
if ($('.index_page').length) {
    var cart = window.document.querySelector('.cart');

    var cartItems = cart.querySelector('.cart__count');
}
var delivery = $.cookie('delivery');

if($("#inputPhone").length){
    $("#inputPhone").mask("+79999999999",{autoclear: false});
}
if($("#phone").length){
    $("#phone").mask("+79999999999",{autoclear: false})
}
var summ;
var dataTable = $('#tableOrder').DataTable({
    "language": {
        "emptyTable": "Корзина пуста"
    }
});

function delivery_func() {
        if (delivery === undefined) {
            $("#select_delivery").nifty("show");

        } else {
            $("input:radio[name=group2][value='" + $.cookie('delivery') + "']").prop({"checked": true});
        }

    }

function initIfhaveSession() {
    var cartValue = sessionStorage.getItem("cart");
    if(cartValue!=null) {
        var cartObj = JSON.parse(cartValue);
        if (cartObj[0].row[0] != "Корзина пуста") {
            cartObj.forEach(function (entry) {
                console.log(entry.row[0]);
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
                    dataTable.row.add([
                        entry.row[0],
                        "<select class='basic'><option value=''>Выберите соус</option><option>Аррабиата</option><option>Сливочный</option><option>Песто</option><option>Грибной</option><option>Бешамель</option>",
                        "<input type='number' value='" + entry.row[2] + "' data-price='" + entry.row[3] + "' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
                        "<span class='cena'>" + entry.row[3] + " <i class='fa fa-rub'></i></span>",
                        "<a href='#0' id='" + entry.row[4] + "' class='delete'><i class='fa fa-times'></i></a>"
                    ]).draw(false);

                    $('.basic').fancySelect();

                    $('.fancified :contains(' + entry.row[1] + ')').prop("selected", true);

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


if ($('.userIsAuch .full_price, .borderLeft .full_price').length){
    var full_price = sessionStorage.getItem("cart_price");
    console.log(full_price);
    $('.full_price').text(full_price);
    initIfhaveSession();
    delivery_func();
    $("#adressAuch").select2({
            maximumSelectionLength: 1,
            tags: true,
            data: data
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

$(".action--like").click(function (e) {
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
            console.log(data.result);
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

$('input:radio[name=group2]').change(function () {
    $.cookie('delivery', this.value, {
        expires: 7
    });
    $('.full span').text(calculateSumm());
});

$('input:radio[name=group1]').change(function () {
    $.cookie('delivery', this.value, {
        expires: 7
    });

    $("#select_delivery").nifty("hide");
    $("input:radio[name=group2][value='" + $.cookie('delivery') + "']").prop({"checked": true});

    $('.full span').text(calculateSumm());
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
    if (summ != 0) {

        if ($.cookie('delivery') == "no_delivery") {
            summ = summ - summ * 10 / 100;

        }
    }
    if ($('.userIsAuch .full_price').length){
        $('.full_price').text(summ);
    }

    if($('.borderLeft .full_price').length){
        $('.full_price').text(summ);
    }

    sessionStorage.setItem("cart", JSON.stringify(dataFromTable()));
    sessionStorage.setItem("cart_price", summ);
    sessionStorage.setItem("delivery", $.cookie('delivery'));
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
        what = a[--L];$('.slider').anyslider();

        while ((ax = arr.indexOf(what)) !== -1) {
            arr.splice(ax, 1);
        }
    }
    return arr;
}

$(document).keyup(function (e) {
    if (e.keyCode == 27) { // escape key maps to keycode `27`
        $('.popUp').removeClass('isUp');

    }
});




$(".one--buy").click(function () {
    var data_items = jQuery.parseJSON($(this).attr("data-items"));
    if (data_items['item_category'] == 1) { // todo: set name
        dataTable.row.add([
            "<h3>" + data_items['item_name'] + "</h3><small>" + data_items['item_component'] + "</small>",
            "<select class='basic'><option value=''>Выберите соус</option><option>Аррабиата</option><option>Сливочный</option><option>Песто</option><option>Грибной</option><option>Бешамель</option>",
            "<input type='number' value='1' data-price='" + data_items['item_price'] + "' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
            "<span class='cena'>" + data_items['item_price'] + " <i class='fa fa-rub'></i></span>",
            "<a href='#0' id='" + data_items['item_id'] + "' class='delete'><i class='fa fa-times'></i></a>"
        ]).draw(false);
        $('.basic').fancySelect();
        $(".checkOut input[type=number]").on("change", function (e) {
            $('.full span').text(calculateSumm());

        });
        $('.full span').text(calculateSumm());


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
    }
    cartItems.innerHTML = Number(cartItems.innerHTML) + 1;
    iosOverlay({
        text: "Добавлено!",
        duration: 2e3,
        icon: "static/img/check.png"
    });
});

jQuery(document).ready(function () {
    if ($('.index_page').length) {



        var tableOrder = $('#tableOrder');
        tableOrder.on('click', '.delete', function (e) {
            dataTable.row('.selected').remove().draw(false);
            cartItems.innerHTML = Number(cartItems.innerHTML) - 1;

            $('.full span').text(calculateSumm());

        });
    }

}); //ready

$('#orderNow').click(function (event) {
    window.location.href = "/order";
});
var data = [{
    id: 1,
    text: 'г.Нижневартовск'
}, {
    id: 2,
    text: 'г.Мегион'
}, {
    id: 3,
    text: 'г.Лангепас'
}];

$('.slider__item').click(function (event) {
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
                item_category: e.result.category
            };


            $(".aboutProduct .action--buy").attr({
                "value": e.result.id,
                "data-items": JSON.stringify(item_result)
            });

            arrays_one = (e.result.components).split(",");
            if(arrays_one[0]=="") {
                $(".aboutProduct h3").hide();
            }
            else{
                $(".aboutProduct h3").show();
            }
                $("#one_array").empty();
                $.each(arrays_one, function (i) {
                    var li = $('<li/>')
                        .text(arrays_one[i])
                        .appendTo($("#one_array"));
                });

            $("#one_weight").text(e.result.weight);
            $("#one_name").text(e.result.name);
            $(".preloader").hide();

            //for (var item_resp in e.response) {
            //
            //}

        }
    });


});
$('.closebtn').click(function (event) {
    $('.popUp').removeClass('isUp');

});

$('.cart, .showCart').click(function (event) {
    //dataTable.clear().draw();
    //$.ajax({
    //    type: 'POST',
    //// Provide correct Content-Type, so that Flask will know how to process it.
    //    contentType: 'application/json',
    //// Encode your data as JSON.
    //    data: JSON.stringify($.parseJSON($.cookie('order')).values),
    //// This is the type of data you're expecting back from the server.
    //    dataType: 'json',
    //    url: '/get_order',
    //    success: function (e) {
    //        summ=0;
    //        //for (var item_resp in e.response){
    //        //    dataTable.row.add([
    //        //        "<h3>"+ e.response[item_resp].item_name+"</h3><small>"+e.response[item_resp].item_component+"</small>",
    //        //        "<input type='number' value='1' data-price='"+e.response[item_resp].price+"' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
    //        //        "<span class='cena'>"+e.response[item_resp].price+" <i class='fa fa-rub'></i></span>",
    //        //        "<a href='#0' id='"+e.response[item_resp].id+"' class='delete'><i class='fa fa-times'></i></a>"]
    //        //    ).draw( false );
    //        //        summ += parseInt(e.response[item_resp].price);
    //        //        $(".full span").text(summ);
    //
    //
    //        $(".checkOut input[type=number]").change(function () {
    //            $(".full span").text(calculateSumm())
    //        });
    //    }
    //});
    if (calculateSumm() == 0) {
        iosOverlay({
            text: "Корзина пуста",
            duration: 2e3,
            icon: "static/img/cross.png"
        });
    } else {
        $('.full span').text(calculateSumm());

        $('.checkOut').addClass('isUp');
    }
    ;
});

$('.closezakazbtn').click(function (event) {
    $('.checkOut').removeClass('isUp');

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
        // filter ctrls
            filterCtrls = [].slice.call(document.querySelectorAll('.filter > button')),
        // cart
            cart = document.querySelector('.cart'),
            cartItems = cart.querySelector('.cart__count');
    }


    function init() {
        // preload images
        if ($('.index_page').length) {

            imagesLoaded(grid, function () {
                barWidth();
                // initFlickity();
                initIsotope();
                initEvents();

                delivery_func();
                initIfhaveSession();
                classie.remove(grid, 'grid--loading');
                $('.sliders').anyslider({
                    showBullets: true,
                    showControls: true
                });

                $(".preloader").hide();


            });
        }

    }


    function barWidth() {
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
            transitionDuration: '0.6s'
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
        if (data_items['item_category'] == "Вторая") { // todo: set name
            dataTable.row.add([
                "<h3>" + data_items['item_name'] + "</h3><small>" + data_items['item_component'] + "</small>",
                "<select class='basic'><option value=''>Выберите соус</option><option>Аррабиата</option><option>Сливочный</option><option>Песто</option><option>Грибной</option><option>Бешамель</option>",
                "<input type='number' value='1' data-price='" + data_items['item_price'] + "' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
                "<span class='cena'>" + data_items['item_price'] + " <i class='fa fa-rub'></i></span>",
                "<a href='#0' id='" + data_items['item_id'] + "' class='delete'><i class='fa fa-times'></i></a>"
            ]).draw(false);
            $('.basic').fancySelect();
            $(".checkOut input[type=number]").on("change", function (e) {
                $('.full span').text(calculateSumm());

            });
            $('.full span').text(calculateSumm());


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


        }
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

    function recalcFlickities() {
        for (var i = 0, len = flkties.length; i < len; ++i) {
            flkties[i].resize();
        }
    }

    init();

})(window);



