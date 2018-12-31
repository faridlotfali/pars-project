#  روز دهم

### <center> ورود با ajax </center>


```
<script>
    
        $(document).on('submit','#login_form', function(e){
          e.preventDefault();
          var user = $('#username').val();
          $.ajax({
            type:'POST',
            url : '/login2/',
            data:{
              username:$('#username').val(),
              password:$('#password').val(),
              csrfmiddlewaretoken: $('input[name = csrfmiddlewaretoken ]').val(),
            },
            success: function(){
                $('#Hiusername').text(`hi ${user}`);
                $('.login-text').text(' ');
                $('#login').modal('toggle');
                $('#login').removeClass('in');
                $('#login').attr("aria-hidden","true");
                $('#login').css("display", "none");
                $('.modal-backdrop').remove();
                $('body').removeClass('modal-open');
                setTimeout(function(){},2000);
            },
            error: function(error){
               alert("username or password doesnt exist");
               }
          });
  
        });
      </script>
```