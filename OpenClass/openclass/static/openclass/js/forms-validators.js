function validateSettingsForm() {
    first_name = document.forms["update_user"]["first_name"].value;
    last_name = document.forms["update_user"]["last_name"].value;
    email = document.forms["update_user"]["email"].value;
    alert = document.getElementById("errorAlert");
    if (first_name == "") {
        // alert.style = "";
        alert.innerHTML =  "First Name can't be empty!";
        // alert.style = "display: default;";
        $('#errorAlert').hide();
        $('#errorAlert').toggle("slow");
        // $('#errorAlert').slideToggle("slow");
        return false;
    }
    else if (last_name == "") {
        alert.style = "display: default;";
        $('#errorAlert').hide();
        $('#errorAlert').toggle("slow");
        alert.innerHTML =  "Last Name can't be empty!";
        return false;
    }
    else if (email == "") {
        alert.style = "display: default;";
        $('#errorAlert').hide();
        $('#errorAlert').toggle("slow");
        alert.innerHTML =  "Email can't be empty!";
        return false;
    }
}

function validateSignUpForm() {
    pass1 = document.forms["signupForm"]["password"].value;
    pass2 = document.forms["signupForm"]["pw2"].value;
    alert = document.getElementById("errorAlert");
    if (!(pass1 == pass2)) {
        // alert.style = "";
        alert.innerHTML =  "Passwords don't match!";
        // alert.style = "display: default;";
        $('#errorAlert').hide();
        $('#errorAlert').toggle("slow");
        // $('#errorAlert').slideToggle("slow");
        return false;
    }
}

