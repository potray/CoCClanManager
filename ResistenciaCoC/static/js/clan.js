// Copied from https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
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

// Copied from https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function manage_member_request(request_id, accepted) {

    var csrftoken = getCookie('csrftoken');
    // Send accept to the server, hide the request and show toast for feedback.
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: '',
        type: 'POST',
        data: {
            id: request_id.toString(),
            form_type: 'member_request',
            accepted: accepted.toString()
        },
        success: function () {
            $('#' + request_id).hide();
            if (accepted) {
                Materialize.toast('Accepted', 4000);
                // Get member name from DOM. We need to get the first of the content of the div (just the text).
                var memberName = $('#' + request_id).contents().get(0).nodeValue;
                // Add member to the member list.
                $('#clan_members').append('<li class=collection-item>' + memberName + '</li>')
            }
            else
                Materialize.toast('Rejected!', 4000);
        },

        error: function (xhr, textStatus, thrownError) {
            Materialize.toast(textStatus, 4000);
            console.log(thrownError)
        }
    });

}

