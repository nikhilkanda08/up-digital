"use strict";
var KTSigninTwoSteps = function () {
    var e, t;
    return {
        init: function () {
            var n, i, o, u, r, c;
            e = document.querySelector("#kt_sing_in_two_steps_form"), (t = document.querySelector("#kt_sing_in_two_steps_submit")).addEventListener("click", (function (n) {
                n.preventDefault();
                var i = !0,
                    o = [].slice.call(e.querySelectorAll('input[maxlength="1"]'));
                o.map((function (e) {
                    "" !== e.value && 0 !== e.value.length || (i = !1)
                })), !0 === i ? (t.setAttribute("data-kt-indicator", "on"), t.disabled = !0, setTimeout((function () {
                    t.removeAttribute("data-kt-indicator"), t.disabled = !1, Swal.fire({
                        text: "You have been successfully verified!",
                        icon: "success",
                        buttonsStyling: !1,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    }).then((function (t) {
                        if (t.isConfirmed) {
                            o.map((function (e) {
                                e.value = ""
                            }));
                            var n = e.getAttribute("data-kt-redirect-url");
                            n && (location.href = n)
                        }
                    }))
                }), 1e3)) : swal.fire({
                    text: "Please enter valid securtiy code and try again.",
                    icon: "error",
                    buttonsStyling: !1,
                    confirmButtonText: "Ok, got it!",
                    customClass: {
                        confirmButton: "btn fw-bold btn-light-primary"
                    }
                }).then((function () {
                    KTUtil.scrollTop()
                }))
            })), n = e.querySelector("[name=code_1]"), i = e.querySelector("[name=code_2]"), o = e.querySelector("[name=code_3]"), u = e.querySelector("[name=code_4]"), r = e.querySelector("[name=code_5]"), c = e.querySelector("[name=code_6]"), n.focus(), n.addEventListener("keyup", (function () {
                1 === this.value.length && i.focus()
            })), i.addEventListener("keyup", (function () {
                1 === this.value.length && o.focus()
            })), o.addEventListener("keyup", (function () {
                1 === this.value.length && u.focus()
            })), u.addEventListener("keyup", (function () {
                1 === this.value.length && r.focus()
            })), r.addEventListener("keyup", (function () {
                1 === this.value.length && c.focus()
            })), c.addEventListener("keyup", (function () {
                1 === this.value.length && c.blur()
            }))
        }
    }
}();
KTUtil.onDOMContentLoaded((function () {
    KTSigninTwoSteps.init()
}));

function resend_OTP(email){
    $.ajax({
        type: "POST",
        url: "/reset-pwd-OTP/",
        data: {
            email: email,
        },
        dataType: "json",
        encode: true,
        success : function(data) {
            if(data.status == 'true'){
                Swal.fire({
                    text: "OTP Sent",
                    icon: "success"
                    })
            }else{
                Swal.fire({
                    text: data.msg,
                    icon: "error"})
            }
        },
        error : function(request,error)
        {
            Swal.fire({
                text: "Sorry, looks like there are some errors detected, please try again.",
                icon: "error"
                })
        }
    });
}