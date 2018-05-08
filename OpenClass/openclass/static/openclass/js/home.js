(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 54)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 56
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Hide navbar when modals trigger
  $('.portfolio-modal').on('show.bs.modal', function(e) {
    $(".navbar").addClass("d-none");
  })
  $('.portfolio-modal').on('hidden.bs.modal', function(e) {
    $(".navbar").removeClass("d-none");
  })

})(jQuery); // End of use strict

$(document).ready(function(){
    window_width = $(window).width();
        
    // Make the images from the card fill the hole space
    hipster_cards.fitBackgroundForCards();
      
});

hipster_cards = {
    misc:{
        navbar_menu_visible: 0
    },
    
    fitBackgroundForCards: function(){
        $('[data-background="image"]').each(function(){
            $this = $(this);
                        
            background_src = $this.data("src");                                
            
            if(background_src != "undefined"){                
                new_css = {
                    "background-image": "url('" + background_src + "')",
                    "background-position": "center center",
                    "background-size": "cover"
                };
                
                $this.css(new_css);                
            }              
        });
        
        $('.card .header img').each(function(){
            $card = $(this).parent().parent();
            $header = $(this).parent();
                        
            background_src = $(this).attr("src");                                
            
            if(background_src != "undefined"){                
                new_css = {
                    "background-image": "url('" + background_src + "')",
                    "background-position": "center center",
                    "background-size": "cover"
                };
                
                $header.css(new_css);                
            }              
        });
        
    },   
}