$(document).ready(function(){
    console.log("Load Base javascript");
    // Digital Clock
    setInterval(showTime, 1000);
    showTime();
    console.log("Load clock");

    $('input[type=radio][name=camp_search_type]').change(function() {
        if (this.value == '0') {
            $("#business_name_div").addClass("hide-div");
        }
        else if (this.value == '1') {
            $("#business_name_div").removeClass("hide-div");
        }
    });

    // website url validation
    $('#website_url').on('input',  function() {
        console.log("check")
        var input = $('#website_url').val();
        var result = input.replace(/https?:\/\/www./gi,'').replace(/http?:\/\/www./gi,'').replace(/www./gi,'')
        var result =  'www.'+result;
        $('#website_url').val(result);
    });

    $("#camp_submit").click(function (event) {
        event.preventDefault();
        var formData = {
            camp_title: $("#camp_title").val(),
            camp_search_type: $('input[name="camp_search_type"]:checked').val(),
            website_url: $("#website_url").val(),
            business_name: $("#business_name").val(),
        };
        console.log(formData);
        
        $.ajax({
            type: "POST",
            url: "/campaign/",
            data: formData,
            dataType: "json",
            encode: true,
            success : function(data) {
                Swal.fire({
                    title: 'Success',
                    icon: 'success',
                  })              
                console.log('Data: '+JSON.stringify(data));
                window.location.href = window.location.protocol + "//" + window.location.host + "/campaign-detail/" + (data.id).toString() + "/";
                // location.reload();
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

    // keyword submit
    $("#keyword_submit").click(function (event) {
        event.preventDefault();
        if ($("#search_per_day").val() < 0.05){
            // alert("minimum value is 0.05");
            Swal.fire({
                icon: 'warning',
                title: 'Oops...',
                text: 'minimum value is 0.05'
            })
            return false
        }
        if($("#keyword_str").val() == '' || $("#keyword_str").val() == null ||
        $("#search_per_day").val() == '' || $("#search_per_day").val() == null ||
        $("#country_assign").val() == '' || $("#country_assign").val() == null
        // || $("#state_assign").val() == '' || $("#state_assign").val() == null ||
        // $("#city_assign").val() == '' || $("#city_assign").val() == null
        ){
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Incomplete Data'
            })
            return false
        }
        var formData = {
            camp_id: $('a[name="create-keyword"]').attr('data-camp-id'),
            keyword_str: $("#keyword_str").val(),
            search_per_day: $("#search_per_day").val(),
            country_assign: $("#country_assign").val(),
            state_assign: $("#state_assign").val(),
            city_assign: $("#city_assign").val(),
        };
        console.log(formData);
        $.ajax({
            type: "POST",
            url: "/keyword/",
            data: formData,
            dataType: "json",
            encode: true,
            success : function(data) {
                console.log(data['status']);
                if(data['status'] == 'true'){
                    Swal.fire({
                        title: 'Success',
                        icon: 'success',
                      })              
                    console.log('Data: '+JSON.stringify(data));
                    location.reload();
                }else{
                    Swal.fire({
                        icon: 'error',
                        title: 'Upgrade your Plan',
                        text: 'Your Pending limit is '+data['count'] +' searches per day.',
                        // footer: '<a href="">Why do I have this issue?</a>'
                      })              
                }
                
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
    //change password
    $("#change_pwd_submit").click(function (event) {
        event.preventDefault();
        if($("#password1").val() != $("#password2").val()){
            Swal.fire({
                title: 'Password Not Same',
                icon: 'error',
              })
            return false
        }
        var formData = {
            password1: $("#password1").val(),
            password2: $("#password2").val(),
        };
        console.log(formData);
        
        $.ajax({
            type: "POST",
            url: "/change-password/",
            data: formData,
            dataType: "json",
            encode: true,
            success : function(data) {
                $('#kt_modal_reset_pwd').modal('toggle');
                Swal.fire({
                    title: 'Success',
                    icon: 'success',
                  })              
                console.log('Data: '+JSON.stringify(data));
                // window.location.href = window.location.protocol + "//" + window.location.host + "/campaign-detail/" + (data.id).toString() + "/";
                // location.reload();
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
    //chaneg password

    // monthly searches
    var ctx = document.getElementById("monthly_search_canvas");
    var doughnut_data = [$("#monthly_search_mobile").val(),$("#monthly_search_others").val()]
    var monthly_searches = new Chart(ctx, {
    // type: 'pie',
    type: 'doughnut',
    data: {
        // labels: ['MOBILE', 'OTHERS'],
        datasets: [{
        label: '# of Tomatoes',
        data: doughnut_data,
        backgroundColor: [
            'rgba(4,200,200,254)',
            'rgba(0,158,247,254)'
        ],
        borderColor: [
            'rgba(4,200,200,255)',
            'rgba(0,158,247,255)'
        ],
        borderWidth: 1
        }]
    },
    options: {
        //cutoutPercentage: 40,
        responsive: false,

    }
    });

    // total_keyword_chart
    var xValues = [100,200,300,400,500,600,700,800,900,1000];
    const CHART_COLORS = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
      };
    // console.log(JSON.parse($("#keywords_history").val()))
    var total_keyword_chart_data = JSON.parse($("#keywords_history").val())
    var total_keyword_chart_lebels = []
    var total_keyword_chart_counts = []
    var keyword_loop_count = 0;
    for (const [key, value] of Object.entries(total_keyword_chart_data)) {
        keyword_loop_count += 1;
        console.log(key, value);
        total_keyword_chart_lebels.push(key);
        total_keyword_chart_counts.push(value);

        $("#keywords_history_month_"+keyword_loop_count).html( key );
        $("#keywords_history_count_"+keyword_loop_count).html( value );
        $("#keywords_history_div_"+keyword_loop_count).addClass( "d-flex" );
        // keywords_history_div_1
        // keywords_history_month_1
        // keywords_history_count_1

        if(keyword_loop_count == 5) break;
      }
    console.log(total_keyword_chart_lebels,total_keyword_chart_counts);
    var total_keyword_chart_ctx = document.getElementById("total_keyword_chart");
    var total_keyword_chart = new Chart(total_keyword_chart_ctx, {
    type: "pie",
    data: {
        // labels: ["January", "February", "March", "April", "May"],
        labels: total_keyword_chart_lebels,
        datasets: [{
            label: 'MONTHS',
            // data: [120, 220, 80, 90, 50],
            data: total_keyword_chart_counts,
            // borderColor: 'rgba(42,208,208,255)',
            // backgroundColor: 'rgba(179,238,238,255)',

            // borderColor: ['rgb(71, 209, 243)',
            //             'rgb(10, 224, 162)',
            //             'rgb(130, 124, 248)',
            //             'rgb(254, 138, 128)',
            //             'rgb(255, 164, 92)'],
            backgroundColor:  ['rgb(71, 209, 243, 0.9)',
                            'rgb(10, 224, 162, 0.9)',
                            'rgb(130, 124, 248, 0.9)',
                            'rgb(254, 138, 128, 0.9)',
                            'rgb(255, 164, 92, 0.9)']
        }]
    },
    options: {
        plugins: {
                legend: {
                    display: false
                }
        },
        //cutoutPercentage: 40,
        responsive: false,

    }
    // options: {
    //     plugins: {
    //         legend: {
    //           display: false
    //         }
    //       },
    //     elements: {
    //         point:{
    //             radius: 0
    //         }
    //     },
    //     scales: {
    //         x: { // <-- object '{' now, instead of array '[{' before in v2.x.x
    //         //   ticks: {
    //         //     display: false
    //         //   },
    //           grid: {
    //             display: false
    //           },
    //         //   display: false
    //         },
    //         y: { // <-- object '{' now, instead of array '[{' before in v2.x.x
    //             // ticks: {
    //             //   display: false
    //             // },
    //             grid: {
    //               display: false
    //             },
    //             // display: false
    //         }
    //     },
    //     responsive: false,
    //     legend: {
    //         display: false
    //     },
    //     tooltips: {
    //         callbacks: {
    //           label: function(tooltipItem) {
    //         console.log(tooltipItem)
    //             return tooltipItem.yLabel;
    //         }
    //       }
    //     }
    //   }
    });
    // search_result_history_chart
    // search_result_history
    var search_result_history_data = JSON.parse($("#search_result_history").val())
    var search_result_history_lebels = []
    var search_result_history_counts = []
    for (const [key, value] of Object.entries(search_result_history_data)) {
        console.log(key, value);
        search_result_history_lebels.push(key);
        search_result_history_counts.push(value);
      }
    console.log(search_result_history_lebels,search_result_history_counts);
    var search_result_history_chart_ctx = document.getElementById("search_result_history_chart");
    var search_result_history_chart = new Chart(search_result_history_chart_ctx, {
    type: "line",
    data: {
        // labels: ["January", "February", "March", "April", "May", "June", "July"],
        labels: search_result_history_lebels,
        datasets: [{
            label: 'MONTHS',
            // data: [65, 0, 80, 81, 56, 85, 40],
            data: search_result_history_counts,
            borderColor: 'rgba(116,59,234,255)',
            backgroundColor: 'rgba(248,245,255,255)',
            fill: true,
            borderWidth: 2
        }]
    },
    options: {
        plugins: {
            legend: {
              display: false
            }
          },
        elements: {
            point:{
                radius: 0
            }
        },
        scales: {
            x: { // <-- object '{' now, instead of array '[{' before in v2.x.x
            //   ticks: {
            //     display: false
            //   },
              grid: {
                display: false
              },
            //   display: false
            },
            y: { // <-- object '{' now, instead of array '[{' before in v2.x.x
                // ticks: {
                //   display: false
                // },
                grid: {
                  display: false
                },
                // display: false
            }
        },
        responsive: false,
        // legend: {
        //     display: false
        // },
        tooltips: {
            callbacks: {
              label: function(tooltipItem) {
            console.log(tooltipItem)
                return tooltipItem.yLabel;
            }
          }
        }
      }
    });
  });

function showTime() {
    let time = new Date();
    // time = new Date(time.getUTCFullYear(), time.getUTCMonth(), time.getUTCDate(), time.getUTCHours(), time.getUTCMinutes(), time.getUTCSeconds(), time.getUTCMilliseconds());
    let hour = time.getHours();
    let min = time.getMinutes();
    let sec = time.getSeconds();

    hour = hour < 10 ? "0" + hour : hour;
    min = min < 10 ? "0" + min : min;
    sec = sec < 10 ? "0" + sec : sec;

    let currentTime = hour + ":"
        + min + ":" + sec;

    document.getElementById("clock")
        .innerHTML = currentTime;
}
  // validate two decimal points
  function validateTwoDecimalPoints(e) {
    // var patt = /^\d{1,10}(\.\d{1,4})?$/;
    var patt = /^\d*(\.)?(\d{0,2})?$/
    var t = e.value;
    // e.value = 0
    if(t.length>0){
        // console.log(patt.test(t));
        if(patt.test(t)){
            // console.log("tetsting");
            // console.log(t.indexOf("."));
            // console.log(t);
            // console.log();
            // console.log();
            if(t.indexOf(".") >= 0){
                // (t.substr(0, t.indexOf(".")) + t.substr(t.indexOf("."), 3))
                var parts = t.split('.', 2);
                if(parts[1].length > 2){
                    e.value = (t.substr(0, t.indexOf(".")) + t.substr(t.indexOf("."), 3))
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Only Two decimal Numebrs are allowed',
                        })
                }else{
                    e.value = t
                }
            } else{        
                e.value = t;
            }
        }else{
            e.value = t.substr(0, t.length-1);
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Only numebrs are allowed',
            })
        }
    }
}

//deactivate the subscription
function deactivateSubscription() {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, Cancel it!'
      }).then((result) => {
        if (result.isConfirmed) {
          // ajax request
          $.ajax({
            type: "GET",
            url: "/cancel-subscription/",
            success : function(data) {
                Swal.fire({
                    title: 'Success',
                    icon: 'success',
                  })              
                console.log('Data: '+JSON.stringify(data));
                location.reload();
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
          
        }
    })
}

//run bot
function runBot(id) {
    var formData = {
        id: id
    };
    console.log(formData);
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, Run it!'
      }).then((result) => {
        if (result.isConfirmed) {
            $('#overlay').fadeIn().delay(2000);
          // ajax request
          $.ajax({
                // headers: { "X-CSRFToken": token },
                type: "POST",
                url: "/run-bot/",
                data: formData,
                dataType: "json",
                encode: true,
                success : function(data) {
                    Swal.fire({
                        title: 'Success',
                        icon: 'success',
                    })              
                    console.log('Data: '+JSON.stringify(data));
                    $('#overlay').fadeOut();
                    location.reload();
                },
                error : function(request,error)
                {
                    $('#overlay').fadeOut();
                    Swal.fire({
                        title: 'Error!',
                        icon: 'error',
                    })
                    console.log("Request: "+JSON.stringify(request));
                }
            });
          
        }
    })
}
