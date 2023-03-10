"use strict";
var KTAuthResetPassword = function () {
    var t, e, i;
    return {
        init: function () {
            t = document.querySelector("#kt_password_reset_form"), e = document.querySelector("#kt_password_reset_submit"), i = FormValidation.formValidation(t, {
                fields: {
                    email: {
                        validators: {
                            regexp: {
                                regexp: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                                message: "The value is not a valid email address"
                            },
                            notEmpty: {
                                message: "Email address is required"
                            }
                        }
                    }
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger,
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: ".fv-row",
                        eleInvalidClass: "",
                        eleValidClass: ""
                    })
                }
            }), e.addEventListener("click", (function (r) {
                r.preventDefault(), i.validate().then((function (i) {
                    "Valid" == i ? (e.setAttribute("data-kt-indicator", "on"), e.disabled = !0, setTimeout((function () {
                        let emailVal = $("#email").val()
                        $.ajax({
                            type: "POST",
                            url: "/reset-pwd-OTP/",
                            data: {
                                email: emailVal,
                            },
                            dataType: "json",
                            encode: true,
                            success : function(data) {
                                e.setAttribute("data-kt-indicator", "off")
                                if(data.status == 'true'){
                                    e.removeAttribute("data-kt-indicator"), e.disabled = !1, Swal.fire({
                                        text: "We have sent a password reset link to your email.",
                                        icon: "success",
                                        buttonsStyling: !1,
                                        confirmButtonText: "Ok, got it!",
                                        customClass: {
                                            confirmButton: "btn btn-primary"
                                        }
                                    }).then((function (e) {
                                        console.log(i);
                                        if (e.isConfirmed) {
                                            t.querySelector('[name="email"]').value = "";
                                            var i = t.getAttribute("data-kt-redirect-url");
                                            // i && (location.href = i)
                                            window.location.href = window.location.protocol + "//" + window.location.host + "/two-steps/" + emailVal + "/";
                                        }
                                    }))
                                    console.log('Data: '+JSON.stringify(data));
                                    // window.location.href = window.location.protocol + "//" + window.location.host + "/campaign-detail/" + (data.id).toString() + "/";
                                    // location.reload();
                                }else{
                                    Swal.fire({
                                        text: data.msg,
                                        icon: "error",
                                        buttonsStyling: !1,
                                        confirmButtonText: "Ok, got it!",
                                        customClass: {
                                            confirmButton: "btn btn-primary"
                                        }
                                      })
                                }
                                
                            },
                            error : function(request,error)
                            {
                                e.setAttribute("data-kt-indicator", "off")
                                Swal.fire({
                                    text: "Sorry, looks like there are some errors detected, please try again.",
                                    icon: "error",
                                    buttonsStyling: !1,
                                    confirmButtonText: "Ok, got it!",
                                    customClass: {
                                        confirmButton: "btn btn-primary"
                                    }
                                  })
                                console.log("Request: "+JSON.stringify(request));
                            }
                        });
                    }), 1500)) : Swal.fire({
                        text: "Sorry, looks like there are some errors detected, please try again.",
                        icon: "error",
                        buttonsStyling: !1,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    })
                }))
            }))
        }
    }
}();
KTUtil.onDOMContentLoaded((function () {
    KTAuthResetPassword.init()
}));