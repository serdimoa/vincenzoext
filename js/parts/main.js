/**
 * Created by serdimoa on 02.11.15.
 */
var summ;


function calculateSumm(){
    summ = 0;
     $(".checkOut input[type=number]").each( function() {
        summ += parseInt($(this).val() * $(this).attr("data-price"));
     });
    console.log("summa = "+summ);
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
$(".checkOut input[type=number]").keypress(function(event){
 event= event || window.event;

 if (event.charCode && (event.charCode < 48 || event.charCode > 57)) {// проверка на event.charCode - чтобы пользователь мог нажать backspace, enter, стрелочку назад...

     return false;
 }

     $(".full span").text(calculateSumm())


});




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

$(".aboutProduct .action--buy").click(function () {
    var cookieToJSON = $.parseJSON($.cookie('order'));
        cookieToJSON.values.push(parseInt(this.value));
    $.cookie('order',JSON.stringify(cookieToJSON));

});

if (!$.cookie('order')) {
        $.cookie('order', '{"values":[]}');
        var oldValueUniqueLength = $.parseJSON($.cookie('order')).values.length;
}
else{
    var oldValueUniqueLength = $.parseJSON($.cookie('order')).values.length;
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
        arr = $.parseJSON($.cookie('order')).values;
        cleanArray = removeA(arr, this.id);
        $.removeCookie('order');
        $('.full span').text(calculateSumm());
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
             $(".aboutProduct .action--buy").attr({"value":e.result.id});
             arrays_one = (e.result.components).split(",");
             $("#one_array").empty();
             $.each(arrays_one, function(i) {
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
$('.closebtn').click(function(event) {
    $('.popUp').removeClass('isUp');

});

$('.cart').click(function(event) {
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
            $("#select_delivery").nifty("show");

            classie.remove(grid, 'grid--loading');
            $(".preloader").hide();

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
            recalcFlickities();
            iso.layout();
        }, 50));

        // add to cart
        [].slice.call(grid.querySelectorAll('.grid__item')).forEach(function(item) {
            item.querySelector('.action--buy').addEventListener('click', addToCart);
        });
    }

    function addToCart() {



       console.log(jQuery.parseJSON($(this).attr("data-items")));
        var data_items = jQuery.parseJSON($(this).attr("data-items"));
        if(data_items['item_category']=="Вторая"){// todo: set name
            dataTable.row.add([
                "<h3>"+ data_items['item_name']+"</h3><small>"+data_items['item_component']+"</small>",
                "<select name='fancySelect' class='makeMeFancy'> <option value='0' selected='selected' data-skip='1'>Choose Your Product</option>        	<option value='1' data-icon='img/products/iphone.png' data-html-text='iPhone 4&lt;i&gt;in stock&lt;/i&gt;'>iPhone 4</option>        	<option value='2' data-icon='img/products/ipod.png' data-html-text='iPod &lt;i&gt;in stock&lt;/i&gt;'>iPod</option>            <option value='3' data-icon='img/products/air.png' data-html-text='MacBook Air&lt;i&gt;out of stock&lt;/i&gt;'>MacBook Air</option>            <option value='4' data-icon='img/products/imac.png' data-html-text='iMac Station&lt;i&gt;in stock&lt;/i&gt;'>iMac Station</option>        </select>",
                "<input type='number' value='1' data-price='"+data_items['item_price']+"' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
                "<span class='cena'>"+data_items['item_price']+" <i class='fa fa-rub'></i></span>",
                "<a href='#0' id='"+data_items['item_id']+"' class='delete'><i class='fa fa-times'></i></a>"
            ]).draw( false );
            var select = $('select.makeMeFancy');

	        var selectBoxContainer = $('<div>',{
	        	width		: select.outerWidth(),
	        	className	: 'tzSelect',
	        	html		: '<div class="selectBox"></div>'
	        });

	        var dropDown = $('<ul>',{className:'dropDown'});
	        var selectBox = selectBoxContainer.find('.selectBox');

	        // Looping though the options of the original select element

	        select.find('option').each(function(i){
	        	var option = $(this);

	        	if(i==select.attr('selectedIndex')){
	        		selectBox.html(option.text());
	        	}

	        	// As of jQuery 1.4.3 we can access HTML5
	        	// data attributes with the data() method.

	        	if(option.data('skip')){
	        		return true;
	        	}

	        	// Creating a dropdown item according to the
	        	// data-icon and data-html-text HTML5 attributes:

	        	var li = $('<li>',{
	        		html:	'<img src="'+option.data('icon')+'" /><span>'+
	        				option.data('html-text')+'</span>'
	        	});

	        	li.click(function(){

	        		selectBox.html(option.text());
	        		dropDown.trigger('hide');

	        		// When a click occurs, we are also reflecting
	        		// the change on the original select element:
	        		select.val(option.val());

	        		return false;
	        	});

	        	dropDown.append(li);
	        });

	        selectBoxContainer.append(dropDown.hide());
	        select.hide().after(selectBoxContainer);

	        // Binding custom show and hide events on the dropDown:

	        dropDown.bind('show',function(){

	        	if(dropDown.is(':animated')){
	        		return false;
	        	}

	        	selectBox.addClass('expanded');
	        	dropDown.slideDown();

	        }).bind('hide',function(){

	        	if(dropDown.is(':animated')){
	        		return false;
	        	}

	        	selectBox.removeClass('expanded');
	        	dropDown.slideUp();

	        }).bind('toggle',function(){
	        	if(selectBox.hasClass('expanded')){
	        		dropDown.trigger('hide');
	        	}
	        	else dropDown.trigger('show');
	        });

	        selectBox.click(function(){
	        	dropDown.trigger('toggle');
	        	return false;
	        });

	        // If we click anywhere on the page, while the
	        // dropdown is shown, it is going to be hidden:

	        $(document).click(function(){
	        	dropDown.trigger('hide');
	        });
        }
        else{
             dataTable.row.add([
                "<h3>"+ data_items['item_name']+"</h3><small>"+data_items['item_component']+"</small>",
                " ",
                "<input type='number' value='1' data-price='"+data_items['item_price']+"' min='1' max='999' class='form-control' aria-label='Text input with multiple buttons'>",
                "<span class='cena'>"+data_items['item_price']+" <i class='fa fa-rub'></i></span>",
                "<a href='#0' id='"+data_items['item_id']+"' class='delete'><i class='fa fa-times'></i></a>"
            ]).draw( false );
        }


        //$.cookie('order',JSON.stringify(cookieToJSON));

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


