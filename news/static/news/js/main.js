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
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


const add_to_favorites_url = '/favorites/add/'
const remove_from_favorites_url = '/favorites/remove/'
const favorites_api_url = '/favorites/api/'
const added_to_favorites_class = 'added'

function add_to_favorites() {
    $('.add_to_favorites').each((index, el) => {
        $(el).click((e) => {
            e.preventDefault()

            const type = $(el).data('type');
            const id = $(el).data('id');

            if($(e.target).hasClass(added_to_favorites_class)) {
                $.ajax({
                    url: remove_from_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                    },
                    success: (data) => {
                        $(el).removeClass(added_to_favorites_class);
                        $(el).text('Добавить в избранное');
                    }
                })
            } else {
                $.ajax({
                    url: add_to_favorites_url,
                    type: 'POST',
                    dataType: 'json',
                    data: {
                        type: type,
                        id: id,
                    },
                    success: (data) => {
                        $(el).addClass(added_to_favorites_class);
                        $(el).text('Убрать из избранного');
                    }
                })
            }
        })
    })
}

function get_session_favorites() {
    $.getJSON(favorites_api_url, (json) => {
        if(json !== null) {
            for(let i = 0; i < json.length; i++){
                $('.add_to_favorites').each((index, el) => {
                    const type = $(el).data('type');
                    const id = $(el).data('id');

                    if(json[i].type == type && json[i].id == id) {
                        $(el).addClass(added_to_favorites_class);
                        $(el).text('Убрать из избранного');
                    }
                })
            }
        }
    })
}

$(document).ready(function(){
    add_to_favorites();
    get_session_favorites();
})