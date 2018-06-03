function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({ 
   beforeSend: function(xhr, settings) {
        console.log(settings);
       function getCookie(name) {
           var cookieValue = null;
           if (document.cookie && document.cookie != '') {
               var cookies = document.cookie.split(';');
               for (var i = 0; i < cookies.length; i++) {
                   var cookie = jQuery.trim(cookies[i]);
                   // Does this cookie string begin with the name we want?
                   if (cookie.substring(0, name.length + 1) == (name + '=')) {
                       cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                       break;
                   }
               }
           }
           return cookieValue;
       }
       // if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
           // Only send the token to relative URLs i.e. locally.
           xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
       }
   } 
});