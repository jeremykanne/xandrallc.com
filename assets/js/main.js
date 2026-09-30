/*-----------------------------------------------------------------------------------

    Theme Name: Ales - Business and Corporate Template
    Description: Business and Corporate HTML Template
    Author: chitrakootweb
    Version: 2.0

    /* ----------------------------------

    JS Active Code Index

        01. Preloader
        02. Sticky Header
        03. Scroll To Top
        04. Parallax
        05. Video
        06. Tabs
        07. Resize function
        08. FullScreenHeight function
        09. ScreenFixedHeight function
        10. FullScreenHeight and screenHeight with resize function
        11. Sliders
        12. CountUp
        13. Countdown
        14. Isotop


    ---------------------------------- */

(function($) {

    "use strict";

        /*------------------------------------
            01. Preloader
        --------------------------------------*/

        $('#preloader').fadeOut('normall', function() {
            $(this).remove();
        });

        /*------------------------------------
            02. Sticky Header
        --------------------------------------*/

        $(window).on('scroll', function() {
            var scroll = $(window).scrollTop();
            if (scroll <= 50) {
                $("header").removeClass("scrollHeader").addClass("fixedHeader");
            } else $("header").removeClass("fixedHeader").addClass("scrollHeader");
        });

        /*------------------------------------
            03. Scroll To Top
        --------------------------------------*/

        $(window).on('scroll', function() {
            if ($(this).scrollTop() > 500) {
                $(".scroll-to-top").fadeIn(400);

            } else {
                $(".scroll-to-top").fadeOut(400);
            }
        });

        $(".scroll-to-top").on('click', function(event) {
            event.preventDefault();
            $("html, body").animate({
                scrollTop: 0
            }, 600);
        });

        /*------------------------------------
            04. Parallax
        --------------------------------------*/

        // sections background image from data background
        var pageSection = $(".parallax,.bg-img");
        pageSection.each(function(indx) {

            if ($(this).attr("data-background")) {
                $(this).css("background-image", "url(" + $(this).data("background") + ")");
            }
        });

        /*------------------------------------
            05. Video
        --------------------------------------*/

        $('.story-video').magnificPopup({
            delegate: '.video',
            type: 'iframe'
        });

        /*------------------------------------
            06. Tabs
        --------------------------------------*/

        $('.tabs_animate').tabslet({
            mouseevent: 'click',
            attribute: 'href',
            animation: true
        });

        /*------------------------------------
            07. Resize function
        --------------------------------------*/

        $(window).resize(function(event) {
            setTimeout(function() {
                SetResizeContent();
            }, 500);
            event.preventDefault();
        });

        /*------------------------------------
            08. FullScreenHeight function
        --------------------------------------*/

        function fullScreenHeight() {
            var element = $(".full-screen");
            var $minheight = $(window).height();
            element.css('min-height', $minheight);
        }

        /*------------------------------------
            09. ScreenFixedHeight function
        --------------------------------------*/

        function ScreenFixedHeight() {
            var $headerHeight = $("header").height();
            var element = $(".screen-height");
            var $screenheight = $(window).height() - $headerHeight;
            element.css('height', $screenheight);
        }

        /*------------------------------------
            10. FullScreenHeight and screenHeight with resize function
        --------------------------------------*/

        function SetResizeContent() {
            fullScreenHeight();
            ScreenFixedHeight();
        }

        SetResizeContent();

    // === when document ready === //
    $(document).ready(function() {

        /*------------------------------------
            07. Sliders
        --------------------------------------*/

        // Testmonials carousel1
        $('#testmonials-carousel').owlCarousel({
            loop: false,
            responsiveClass: true,
            nav: true,
            margin: 0,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            responsive: {
                0: {
                    items: 1,
                    nav: false,
                    dots: true
                },
                600: {
                    items: 1,
                    nav: false,
                    dots: true
                },
                1000: {
                    items: 1,
                    dots: false
                }
            }
        })

        // Testmonials carousel2
        $('#testmonials-style2').owlCarousel({
            loop: true,
            responsiveClass: true,
            nav: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            responsive: {
                0: {
                    items: 1,
                    nav: false,
                    dots: true,
                    margin: 10,
                },
                768: {
                    items: 2,
                    nav: false,
                    dots: true,
                    margin: 15,
                },
                992: {
                    items: 2,
                    dots: false,
                    margin: 40,
                }
            }
        })

        // Services carousel
        $('#services-carousel').owlCarousel({
            loop: true,
            responsiveClass: true,
            dots: false,
            nav: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            responsive: {
                0: {
                    items: 1,
                    margin: 0,
                },
                768: {
                    items: 2,
                    margin: 0,
                },
                992: {
                    items: 3,
                    margin: 0,
                }
            }
        })

        // Blog grid carousel
        $('#blog-grid').owlCarousel({
            loop: true,
            dots: false,
            nav: false,
            autoplay: true,
            autoplayTimeout: 2500,
            responsiveClass: true,
            autoplayHoverPause: false,
            responsive: {
                0: {
                    items: 1,
                    margin: 0,
                },
                768: {
                    items: 2,
                    margin: 0,
                },
                992: {
                    items: 3,
                    margin: 0,
                }
            }
        })

        // Latest blog
        $('#latest-blog').owlCarousel({
            loop: true,
            dots: false,
            nav: false,
            autoplay: true,
            autoplayTimeout: 2500,
            responsiveClass: true,
            autoplayHoverPause: false,
            responsive: {
                0: {
                    items: 1,
                    margin: 0,
                },
                768: {
                    items: 2,
                    margin: 20,
                },
                992: {
                    items: 2,
                    margin: 30,
                },
                1200: {
                    items: 3,
                    margin: 30,
                }
            }
        })

        // Service grids
        $('#service-grids').owlCarousel({
            loop: true,
            dots: false,
            nav: false,
            autoplay: true,
            autoplayTimeout: 2500,
            responsiveClass: true,
            autoplayHoverPause: false,
            responsive: {
                0: {
                    items: 1,
                    margin: 0,
                },
                768: {
                    items: 2,
                    margin: 20,
                },
                992: {
                    items: 3,
                    margin: 30,
                }
            }
        })

        // Projects grids
        $('#project-grids').owlCarousel({
            loop: true,
            dots: true,
            nav: false,
            autoplay: true,
            autoplayTimeout: 2500,
            responsiveClass: true,
            autoplayHoverPause: false,
            responsive: {
                0: {
                    items: 1,
                    margin: 0,
                },
                768: {
                    items: 2,
                    margin: 20,
                },
                992: {
                    items: 3,
                    margin: 30,
                }
            }
        })

        // project grids full
        $('#project-grids-full').owlCarousel({
            loop: true,
            dots: true,
            nav: false,
            autoplay: true,
            autoplayTimeout: 2500,
            responsiveClass: true,
            autoplayHoverPause: false,
            responsive: {
                0: {
                    items: 1,
                    margin: 0,
                },
                599: {
                    items: 2,
                    margin: 15,
                },
                768: {
                    items: 2,
                    margin: 15,
                },
                992: {
                    items: 3,
                    margin: 15,
                },
                1200: {
                    items: 4,
                    margin: 20,
                },
                1400: {
                    items: 5,
                    margin: 20,
                }
            }
        })

        // Clients carousel
        $('#clients').owlCarousel({
            loop: false,
            nav: false,
            dots: false,
            autoplay: true,
            autoplayTimeout: 3000,
            responsiveClass: true,
            autoplayHoverPause: false,
            responsive: {
                0: {
                    items: 2,
                    margin: 20
                },
                768: {
                    items: 3,
                    margin: 40,
                },
                992: {
                    items: 4,
                    margin: 60,
                    },
                    1200: {
                    items: 5,
                    margin: 80,
                }
            }
        })

        // Project single carousel
        $('#project-single').owlCarousel({
            loop: false,
            nav: false,
            responsiveClass: true,
            dots: false,
            responsive: {
                0: {
                    items: 1,
                    margin: 15,
                },
                600: {
                    items: 2,
                    margin: 15,
                },
                1000: {
                    items: 3,
                    margin: 15
                }
            }
        })

        // Revolution slider1
        if ($("#rev_slider_1").length !== 0) {
            var tpj = jQuery;
            var revapi1;
            tpj(document).ready(function() {
                if (tpj("#rev_slider_1").revolution == undefined) {
                    revslider_showDoubleJqueryError("#rev_slider_1");
                } else {
                    revapi1 = tpj("#rev_slider_1").show().revolution({
                        sliderType: "standard",
                        sliderLayout: "fullwidth",
                        dottedOverlay: "none",
                        delay: 9000,
                        spinner: "spinner4",
                        navigation: {
                            keyboardNavigation: "off",
                            keyboard_direction: "horizontal",
                            mouseScrollNavigation: "off",
                            onHoverStop: "off",
                            touch: {
                                touchenabled: "on",
                                swipe_threshold: 75,
                                swipe_min_touches: 1,
                                swipe_direction: "horizontal",
                                drag_block_vertical: false
                            },
                            arrows: {
                                enable: false,
                                style: 'metis',
                                rtl: false,
                                hide_onleave: true,
                                hide_onmobile: true,
                                hide_under: 991,
                                hide_over: 9999,
                                hide_delay: 200,
                                hide_delay_mobile: 1200,
                                tmp: '',
                                left: {
                                    container: 'slider',
                                    h_align: 'left',
                                    v_align: 'center',
                                    h_offset: 20,
                                    v_offset: 0
                                },
                                right: {
                                    container: 'slider',
                                    h_align: 'right',
                                    v_align: 'center',
                                    h_offset: 20,
                                    v_offset: 0
                                }
                            },
                            bullets: {
                                enable: false,
                                hide_onmobile: false,
                                hide_under: 300,
                                style: "hermes",
                                hide_onleave: false,
                                hide_delay: 200,
                                hide_delay_mobile: 1200,
                                direction: "horizontal",
                                h_align: "center",
                                v_align: "bottom",
                                h_offset: 0,
                                v_offset: 30,
                                space: 8
                            },
                        },
                        responsiveLevels: [1240, 1024, 767, 480],
                        gridwidth: [1170, 1170, 767, 480],
                        gridheight: [650, 650, 600, 600],
                        lazyType: "none",
                        shadow: 0,
                        shuffle: "off",
                        autoHeight: "off",
                    });
                }
            });
        }

        // Revolution slider2
        if ($("#rev_slider_2").length !== 0) {
            var tpj = jQuery;
            var revapi4;
            tpj(document).ready(function() {
                if (tpj("#rev_slider_2").revolution == undefined) {
                    revslider_showDoubleJqueryError("#rev_slider_2");
                } else {
                    revapi4 = tpj("#rev_slider_2").show().revolution({
                        sliderLayout:"fullscreen",
                        delay:12000,
                        responsiveLevels:[4096,1024,778,420],
                        gridwidth:[1170,1024,778,410],
                        gridheight:600,
                        hideThumbs:10,
                        fullScreenAutoWidth: "on",
                        fullScreenOffsetContainer: ".rev-offset",

                        navigation: {
                            onHoverStop: "off",
                            touch: {
                                touchenabled: "on",
                                swipe_threshold: 75,
                                swipe_min_touches: 1,
                                swipe_direction: "horizontal",
                                drag_block_vertical: false
                            },
                            arrows:{
                                enable:true,
                                style: "hermes",
                                tmp: '<div class="tp-arr-allwrapper">  <div class="tp-arr-imgholder"></div> <div class="tp-arr-titleholder">{{title}}</div> </div>',
                                left: {
                                    h_align: "left",
                                    v_align: "center",
                                    h_offset: 0,
                                    v_offset: 0
                                },
                                right: {
                                    h_align: "right",
                                    v_align: "center",
                                    h_offset: 0,
                                    v_offset: 0
                                }
                            },
                            bullets:{
                                style:"",
                                enable:false,
                                hide_onmobile:false,
                                hide_onleave:true,
                                hide_delay:200,
                                hide_delay_mobile:1200,
                                hide_under:0,
                                hide_over:9999,
                                direction:"horizontal",
                                space:12,
                                h_align:"center",
                                v_align:"bottom",
                                h_offset:0,
                                v_offset:30,
                                tmp: ''
                            },
                        },

                        parallax:{
                            type:"scroll",
                            levels:[5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85],
                            origo:"enterpoint",
                            speed:400,
                            bgparallax:"on",
                            disable_onmobile:"on"
                        },

                        spinner:"spinner4"
                    });
                }
            });
        }
        // Revolution video
        if ($("#rev_slider_video").length !== 0) {
            var tpj = jQuery;
            var revapi3;
            tpj(document).ready(function() {
                if (tpj("#rev_slider_video").revolution == undefined) {
                    revslider_showDoubleJqueryError("#rev_slider_video");
                } else {
                    revapi3 = tpj("#rev_slider_video").show().revolution({
                        sliderType: "standard",
                        sliderLayout: "fullwidth",
                        dottedOverlay: "none",
                        delay: 9000,
                        spinner: "spinner4",
                        navigation: {
                            keyboardNavigation: "off",
                            keyboard_direction: "horizontal",
                            mouseScrollNavigation: "off",
                            onHoverStop: "off",
                            touch: {
                                touchenabled: "on",
                                swipe_threshold: 75,
                                swipe_min_touches: 1,
                                swipe_direction: "horizontal",
                                drag_block_vertical: false
                            },
                            arrows: {
                                enable: false
                            },
                            bullets: {
                                enable: false
                            },
                        },
                        responsiveLevels: [1240, 1024, 767, 480],
                        gridwidth: [1170, 1170, 767, 480],
                        gridheight: [700, 700, 600, 600],
                        lazyType: "none",
                        shadow: 0,
                        shuffle: "off",
                        autoHeight: "off",
                    });
                }
            });
        }

        /*------------------------------------
            08. CountUp
        --------------------------------------*/

        $('.countup').counterUp({
            delay: 25,
            time: 2000
        });

        /*------------------------------------
            09. Countdown
        --------------------------------------*/

        if ($(".countdown").length !== 0) {
            var tpj = jQuery;
            var countdown;
            tpj(document).ready(function() {
                if (tpj(".countdown").countdown == undefined) {
                    revslider_showDoubleJqueryError(".countdown");
                } else {
                    countdown = tpj(".countdown").show().countdown({
                        date: "01 Jan 2021 00:01:00", //set your date and time. EX: 15 May 2014 12:00:00
                        format: "on"
                    });
                }
            });
        }

    });

    // === when window loading === //
    $(window).on("load", function() {

        /*------------------------------------
            11. Isotop
        --------------------------------------*/

        // magnificPopup with slider
        $('.single-img').magnificPopup({
            delegate: '.popimg',
            type: 'image'
        });

        // isotope with magnificPopup
        $('.gallery').magnificPopup({
            delegate: '.popimg',
            type: 'image',
            gallery: {
                enabled: true
            }
        });

        var $gallery = $('.gallery').isotope({
            // options
        });

        // filter items on button click
        $('.filtering').on('click', 'span', function() {
            var filterValue = $(this).attr('data-filter');
            $gallery.isotope({
                filter: filterValue
            });
        });

        $('.filtering').on('click', 'span', function() {
            $(this).addClass('active').siblings().removeClass('active');
        });

        // stellar
        $(window).stellar();

    });

})(jQuery);
