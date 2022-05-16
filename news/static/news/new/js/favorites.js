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
                        $('#favorites > span').text(data.count);
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
                        $('#favorites > span').text(data.count);
                    }
                })
            }
        })
    })
}

function get_session_favorites() {
    $.getJSON(favorites_api_url, (json) => {
        if(json !== null) {
            $('#favorites > span').text(json.length);
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

    $("#id_address").suggestions({
        token: "99767383f97ee605594a85d9714f70f3655a278f",
        type: "ADDRESS",
        /* Вызывается, когда пользователь выбирает одну из подсказок */
        onSelect: function(suggestion) {
            console.log(suggestion);
        }
    });

    $(function () {
        $("#id_date_of_birth, input[id$='-finish'], input[id$='-start']").datepicker({
          format:'dd.mm.yyyy',
    });
  });

    $(function() {
        $('.exp-formset .exp-formset-item').formset({
            addText: 'Добавить',
            deleteText: 'Удалить',
            addCssClass: 'btn btn-primary mt-1',
            deleteCssClass: 'btn btn-danger',
            hideLastAddForm: true,
        });
    })

    $('#feed_submit').submit(function(e){
        text = $('#id_text').val();
        $('input[name="message_copy"]').val(text);
    });

    $('#feed_send_form').submit(function(e){
        text = $('#id_text').val().trim();
        if (text.length == 0) {
            e.preventDefault();
            $('.invalid-feedback').show('fast').hide(4000);
            return
        }
    });
})