$(document).ready(function(){
    // modal
    // Get the modal
    var modal = document.getElementById("myModal");
    
    // Get the button that opens the modal
    var btn = document.getElementById("myBtntesting");
    
    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];
    
    // When the user clicks the button, open the modal 
    // btn.onclick = function() {
    //   modal.style.display = "block";
    // }
    
    
    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    }
    
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }

    // reset the user password
    $('#resetPasswordButton').on('click', function(event){
        event.preventDefault();
        if($("#password").val() != $("#confirmPassword").val()){
            Swal.fire({
                title: 'Error!',
                text: 'Passwords are not same!!!',
                icon: 'error',
              })
            return false
        }
        var formData = {
            id: $("#userID").val(),
            password1: $("#password").val(),
            password2: $("#confirmPassword").val(),
        };
        console.log(formData);
        
        $.ajax({
            type: "POST",
            url: "/admin-reset-password/",
            data: formData,
            dataType: "json",
            encode: true,
            success : function(data) {
                Swal.fire({
                    title: 'Success',
                    icon: 'success',
                  })              
                console.log('Data: '+JSON.stringify(data));
                // location.reload();
                document.getElementById("myModal").style.display = "none";
            },
            error : function(request,error)
            {
                Swal.fire({
                    title: 'Error!',
                    icon: 'error',
                  })
                console.log("Request: "+JSON.stringify(request));
            }
        });
    });
});

function changePasswordModal() {
    $("#content_div").html("");
    var modal = document.getElementById("myModal");
    modal.style.display = "block";
}