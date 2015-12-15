/**
 * Created by serdimoa on 02.11.15.
 */
function unique(arr) {
  var obj = {};

  for (var i = 0; i < arr.length; i++) {
    var str = arr[i];
    obj[str] = true; // запомнить строку в виде свойства объекта
  }

  return Object.keys(obj); // или собрать ключи перебором для IE8-
}

//Удаление из масива значение
function removeA(arr) {
    var what, a = arguments, L = a.length, ax;
    while (L > 1 && arr.length) {
        what = a[--L];
        while ((ax= arr.indexOf(what)) !== -1) {
            arr.splice(ax, 1);
        }
    }
    return arr;
}

$(document).keyup(function(e) {
    if (e.keyCode == 27) { // escape key maps to keycode `27`
        $('.popUp').removeClass('isUp');

    }
});
if (!$.cookie('order')) {
        $.cookie('order', '{"values":[]}');
        var oldValueUniqueLength = unique($.parseJSON($.cookie('order')).values).length;
}
else{
    var oldValueUniqueLength = unique($.parseJSON($.cookie('order')).values).length;
}
var dataTable = $('#tableOrder').DataTable();


jQuery(document).ready(function() {
    var sequenceElement = document.getElementById("sequence"),
        options = {
            animateCanvas: !1,
            phaseThreshold: !1,
            preloader: !0,
            reverseWhenNavigatingBackwards: !0
        },
        mySequence = sequence(sequenceElement, options);

    console.log(oldValueUniqueLength);
    $('#tableOrder').on( 'click', '.delete', function (e) {
        console.log(this.id);
        var colIdx = dataTable.row(this).index();
        dataTable.row(colIdx).remove().draw( false );
        arr = unique($.parseJSON($.cookie('order')).values);
        cleanArray = removeA(arr, this.id);
        $.removeCookie('order');
        $.cookie('order', '{"values":['+cleanArray+']}');



    });
    // $('.delete').click( function (event) {
    //     // var colIdx = dataTable.cell(this).index().column;
    //     dataTable.row(colIdx).remove().draw( false );
    // } );
    $('#menu').slicknav();


}); //ready

$('#orderNow').click(function (event) {
    window.location.href = "/order";
});
var data = [{ id: 1, text: 'г.Нижневартовск' }, { id: 2, text: 'г.Мегион' }, { id: 3, text: 'г.Лангепас' }];
$('#restorePass').click(function(event) {
    if ($("#auchPhone").val()=="") {
        $(".wrongPhone").show();
    } else{
        $(".orderModal").modal('hide');
        $(".auchUsers").empty();
        $("#sendAuchNone").attr({
            disabled: 'disabled'
        });
        $(".userIsAuch").show();
        $("#adressAuch").select2({
            placeholder: "Выберите ваш адрес",
            data:data
        });

    };
});

$('.slider__item').click(function(event) {
    $(".preloader").show();
    $('.popUp').addClass('isUp');
     $.ajax({
         type: 'POST',
         // Provide correct Content-Type, so that Flask will know how to process it.
         contentType: 'application/json',
         // Encode your data as JSON.
         // This is the type of data you're expecting back from the server.
         dataType: 'json',
         url: '/get_one_item/'+$(this).attr("data-id-item"),
         success: function (e) {
             console.log(e);
             $("#one_img").attr(
                 {"src" : 'static/upload/' + e.result.imgs }
             );
             arrays_one = (e.result.components).split(",");
             $("#one_array").empty();
             $.each(arrays_one, function(i) {
                var li = $('<li/>')
                    .text(arrays_one[i])
                    .appendTo($("#one_array"));
            });
             $("#one_name").text(e.result.name);
             $(".preloader").hide();

             //for (var item_resp in e.response) {
             //
             //}

         }
     });


});
$('.closebtn').click(function(event) {
    $('.popUp').removeClass('isUp');

});

$('.cart').click(function(event) {
    dataTable.clear().draw();
    $.ajax({
        type: 'POST',
    // Provide correct Content-Type, so that Flask will know how to process it.
        contentType: 'application/json',
    // Encode your data as JSON.
        data: JSON.stringify(unique($.parseJSON($.cookie('order')).values)),
    // This is the type of data you're expecting back from the server.
        dataType: 'json',
        url: '/get_order',
        success: function (e) {
            for (var item_resp in e.response){
                dataTable.row.add([
                    "<h3>"+ e.response[item_resp].item_name+"</h3><small>"+e.response[item_resp].item_component+"</small>",
                    "<input type='number' value='1' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
                    "<span class='cena'>"+e.response[item_resp].price+" <i class='fa fa-rub'></i></span>",
                    "<a href='#0' id='"+e.response[item_resp].id+"' class='delete'><i class='fa fa-times'></i></a>"]
                ).draw( false );
            }

        }
    });

    $('.checkOut').addClass('isUp');
});

$('.closezakazbtn').click(function(event) {
    $('.checkOut').removeClass('isUp');

});
/**
 Product Page
**/
//Function for fixin sidebar
$(function() {
    var sidebar = $('#bar');
    var bodywithsidebar = $(".view");
    var cart = $(".cart");
    var top = sidebar.offset().top - parseFloat(sidebar.css('margin-top'));

    $(window).scroll(function(event) {
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
});

(function(window) {

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
        onEndAnimation = function(el, callback) {
            var onEndCallbackFn = function(ev) {
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

        return function(e) {
            if (allowSample) {
                allowSample = false;
                setTimeout(function() {
                    allowSample = true;
                }, delay);
                fn(e);
            }
        };
    }

    // sliders - flickity
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

    function init() {
        // preload images
        imagesLoaded(grid, function() {
            barWidth();
            // initFlickity();
            initIsotope();
            initEvents();
            classie.remove(grid, 'grid--loading');
        });
    }

    function barWidth() {}

    function initFlickity() {
        sliders.forEach(function(slider) {
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
        filterCtrls.forEach(function(filterCtrl) {
            filterCtrl.addEventListener('click', function() {
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
        window.addEventListener('resize', throttle(function(ev) {
            recalcFlickities()
            iso.layout();
        }, 50));

        // add to cart
        [].slice.call(grid.querySelectorAll('.grid__item')).forEach(function(item) {
            item.querySelector('.action--buy').addEventListener('click', addToCart);
        });
    }

    function addToCart() {
        var cookieToJSON = $.parseJSON($.cookie('order'));
        cookieToJSON.values.push(parseInt(this.value));
        var valueUnique = unique(cookieToJSON.values);
        if(valueUnique.length>oldValueUniqueLength){
            //classie.add(cart, 'cart--animate');
            //setTimeout(function() {
            //    cartItems.innerHTML = Number(cartItems.innerHTML) + 1;
            //}, 200);
            //onEndAnimation(cartItems, function() {
            //    classie.remove(cart, 'cart--animate');
            //});
            oldValueUniqueLength=valueUnique.length;
            console.log("Новая уникальная длинна больше, чем старая")
        }
        else if(valueUnique.length<oldValueUniqueLength){
            console.log("Новая уникальная длинна меньше, чем старая")

        }
        else{

        }
        $.cookie('order',JSON.stringify(cookieToJSON));

        // classie.add(cart, 'cart--animate');

        // onEndAnimation(cartItems, function() {
        //     classie.remove(cart, 'cart--animate');
        // });
    }

    function recalcFlickities() {
        for (var i = 0, len = flkties.length; i < len; ++i) {
            flkties[i].resize();
        }
    }

    init();

})(window);
