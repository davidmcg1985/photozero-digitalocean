$('#like').click(function(){
      $.ajax({
               type: "POST",
               url: "{% url 'like' %}",
               data: {'slug': $(this).attr('name'), 'csrfmiddlewaretoken': '{{ csrf_token }}'},
               dataType: "json",
               success: function(response) {
                      alert(response.message);
                      alert('Company likes count is now ' + response.likes_count);
                },
                error: function(rs, e) {
                       alert(rs.responseText);
                }
          }); 
    })
