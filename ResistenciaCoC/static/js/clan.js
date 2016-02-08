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

function startWar(){
    var clanTag = prompt("Enter clan tag without #");

    //Check for valid input.
    if(clanTag == null || clanTag == ''){
        return false;
    } else {
        // Check for valid tag.
        if (clanTag.length != 8){
            Materialize.toast("Please enter a valid clan tag.", 4000);
            return false;
        } else {
            // Tag for testing: #90JL9JCQ
            token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImI3ZTIzZjhhLWE1NzItNGJiYS05MmExLTVjMmMxNTQ3YWQxOSIsImlhdCI6MTQ1NDk2NjE4MCwic3ViIjoiZGV2ZWxvcGVyL2FjZjM1YTNkLWQyY2MtNmYzOC1jOTNmLTlmNmIzZWMyMWQ2YiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjU0LjIyOC4yMDguMTgyIiwiMTI3LjAuMC4xIl0sInR5cGUiOiJjbGllbnQifV19.z4KKAYUQ_VLHEOCF-fkta5cCzJlIxi_SS1sblPdvxogf8Efx697XbxEVI08yMcrdyLjKQtSgny_kdPso8RZiLQ";
            APIurl = "https://api.clashofclans.com/v1/clans/%23" + clanTag.toString() + "?Authorization=Bearer%20" + token;
            console.log(APIurl);
            testURL = "https://api.clashofclans.com/v1/clans/%2390JL9JCQ?Authorization=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZiMmE5OTNiLTRiNzgtNDhmZS1hZWJlLTAwZjVlNGJiOGZhMCIsImlhdCI6MTQ1NDk2Nzg3NSwic3ViIjoiZGV2ZWxvcGVyL2FjZjM1YTNkLWQyY2MtNmYzOC1jOTNmLTlmNmIzZWMyMWQ2YiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjIxNy4yMTYuODQuMjQ2Il0sInR5cGUiOiJjbGllbnQifV19.GjxKGPa75kBy4rNpjF_jaH-_CJ5PDM70xwDDJuXPvo20eX4-dJGcpOqOvcyvJAL0w4EJPxXkZ6IpOO3kLQQOCQ";
            //$.ajax({
            //    url: APIurl,
            //    beforeSend: function(xhr) {
            //        xhr.setRequestHeader("Authorization", "Bearer " + token);
            //    },
            //    crossDomain: true,
            //    type: 'GET',
            //    dataType: 'json',
            //    success: function(data, textStatus, jqXHR){
            //        console.log(data);
            //    }
            //
            //});

        }

    }

    return true;
}


