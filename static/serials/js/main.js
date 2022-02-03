'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay(200).fadeOut("slow");
    });

    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
        Scroll To Top
    --------------------*/
    $("#scrollToTopButton").click(function() {
        $("html, body").animate({ scrollTop: 0 }, "slow");
        return false;
     });

    /*------------------
        Active Menu
    --------------------*/
    $('.header__menu a').each(function() {
        let location = window.location.href;
        let link = this.href;
        if(location == link) {
            $(this).parent().addClass('active');
        }
    });

    /*------------------
		Crew Slider
	--------------------*/
    $('.owl-carousel').owlCarousel({
        loop:false,
        margin:10,
        nav:false,
        stagePadding:30,
        responsive:{
            0:{
                items:2
            },
            600:{
                items:3
            },
            1000:{
                items:4
            }
        }
    });

})(jQuery);