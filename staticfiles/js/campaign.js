$(document).ready(function(){
    console.log("Load campaign javascript");
    $("#delete_campaign").click(function() {
      var camp_id = $(this).attr("camp-id");
      Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
      }).then((result) => {
        if (result.isConfirmed) {
          // ajax request
          $.ajax({
              type: "DELETE",
              url: "/campaign-detail/"+camp_id+"/",
              success : function(data) {
                  Swal.fire(
                    'Deleted!',
                    'Your Campaign has been deleted.',
                    'success'
                  )
                  window.location.href = window.location.protocol + "//" + window.location.host + "/";
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
          
        }
      })
    });
    
    //country city state dropdown
    //country
    // ajax request
    $.ajax({
        // headers: { "X-CSRFToken": token },
        type: "POST",
        url: "/get-country/",
        data: {
            flag: 'country',
        },
        dataType: "json",
        encode: true,
        success : function(data) { 
            // console.log('Data: '+JSON.stringify(data));
            $('#country_assign').append($('<option>', { 
                value: '',
                text : '--- select country ---'
            }));
            // location.reload();
            for (var i = 0; i < data.data.length; i++) {
                // console.log(data.data[i]);
                $('#country_assign').append($('<option>', { 
                    value: data.data[i]['value'],
                    text : data.data[i]['name'] 
                }));
                //Do something
            }
        },
        error : function(request,error)
        {console.log("Request: "+JSON.stringify(request));}
    });
    // $.getJSON( "/static/json/countries.json", function( data ) {
    //     $.each( data, function( key, val ) {
    //         // console.log(key,val);
    //         // console.log(val.length);
    //         // console.log(key);
    //         $('#country_assign').append($('<option>', { 
    //             value: '',
    //             text : '--- select country ---'
    //         }));
    //         $.each(val, function( index, value ) {
    //             // console.log( index + ": " + value['id'] );
    //             $('#country_assign').append($('<option>', { 
    //                 value: value['id'],
    //                 text : value['name'] 
    //             }));
    //         });
    //     });
        
    // });
    // onchange the country dropdown
    $("#country_assign").change(function(){
        //variable "this" references the state dropdown element
        console.log($(this).val())
        var country = $(this).val();
        // remove all state options
        $('#state_assign').empty()
        // remove all city options
        $('#city_assign').empty()
        $('#state_assign').append($('<option>', { 
            value: '',
            text : '--- select state ---'
        }));
        //state
        $.ajax({
            // headers: { "X-CSRFToken": token },
            type: "POST",
            url: "/get-state/",
            data: {
                flag: 'state',
                countryValue: country,
            },
            dataType: "json",
            encode: true,
            success : function(data) { 
                // console.log('Data: '+JSON.stringify(data));
                $('#state_assign').append($('<option>', { 
                    value: '',
                    text : '--- select state ---'
                }));
                // location.reload();
                for (var i = 0; i < data.data.length; i++) {
                    // console.log(data.data[i]);
                    $('#state_assign').append($('<option>', { 
                        value: data.data[i]['value'],
                        text : data.data[i]['name'] 
                    }));
                    //Do something
                }
            },
            error : function(request,error)
            {console.log("Request: "+JSON.stringify(request));}
        });
        // $.getJSON( "/static/json/states.json", function( data ) {
        //     $.each( data, function( key, val ) {
        //         // console.log(key,val);
        //         // console.log(val.length);
        //         // console.log(key);
        //         $.each(val, function( index, value ) {
        //             // console.log( index + ": " + value['id'] );
        //             if(country == value['country_id']){
        //                 $('#state_assign').append($('<option>', { 
        //                     value: value['id'],
        //                     text : value['name'] 
        //                 }));
        //             }
        //         });
        //     });
            
        // });
    });
    // onchange the state dropdown
    $("#state_assign").change(function(){
        //variable "this" references the state dropdown element
        console.log($(this).val())
        var country = $('#country_assign').val();
        var state = $(this).val();
        // remove all city options
        $('#city_assign').empty()
        $('#city_assign').append($('<option>', { 
            value: '',
            text : '--- select city ---'
        }));
        //state
        $.ajax({
            // headers: { "X-CSRFToken": token },
            type: "POST",
            url: "/get-city/",
            data: {
                flag: 'city',
                countryValue: country,
                stateValue: state,
            },
            dataType: "json",
            encode: true,
            success : function(data) { 
                // console.log('Data: '+JSON.stringify(data));
                $('#city_assign').append($('<option>', { 
                    value: '',
                    text : '--- select city ---'
                }));
                // location.reload();
                for (var i = 0; i < data.data.length; i++) {
                    // console.log(data.data[i]);
                    $('#city_assign').append($('<option>', { 
                        value: data.data[i]['value'],
                        text : data.data[i]['name'] 
                    }));
                    //Do something
                }
            },
            error : function(request,error)
            {console.log("Request: "+JSON.stringify(request));}
        });
        // $.getJSON( "/static/json/cities.json", function( data ) {
        //     $.each( data, function( key, val ) {
        //         // console.log(key,val);
        //         // console.log(val.length);
        //         // console.log(key);
        //         $.each(val, function( index, value ) {
        //             // console.log( index + ": " + value['id'] );
        //             if(state == value['state_id']){
        //                 $('#city_assign').append($('<option>', { 
        //                     value: value['id'],
        //                     text : value['name'] 
        //                 }));
        //             }
        //         });
        //     });
            
        // });
    });

    // update the campaign data
    $("#campaignUpdateSubmit").click(async function (event) {
        event.preventDefault();
        if(parseInt($("#camp-session-pages").val()) > parseInt($("#total-pages").val())){
            Swal.fire({
                title: 'Error!',
                icon: 'error',
                text: 'Number of pages limit is '+ $("#total-pages").val(),
            })
            return
        }
        if(parseInt($("#camp-session-time").val()) > parseInt($("#onsite-time").val())){
            Swal.fire({
                title: 'Error!',
                icon: 'error',
                text: 'Session time limit is '+ $("#onsite-time").val(),
            })
            return
        }
        console.log($("#camp-active"));
        console.log($("#camp-active").is(":checked"));
        var formData = {
            id: $("#camp-id").val(),
            name: $("#camp-name").val(),
            website: $("#camp-website-url").val(),
            mobile_search: $("#camp-mobile-search").val(),
            bounce: $("#camp-bounce-rate").val(),
            pages: $("#camp-session-pages").val(),
            session_time: $("#camp-session-time").val(),
            description: $("#camp-description").val().trim(),
            active: $("#camp-active").is(":checked"),
            // search_type: $('input[name="search_type"]:checked').val()
        };
        console.log(formData);
        
        $.ajax({
            type: "POST",
            url: "/update-campaign/",
            data: formData,
            dataType: "json",
            encode: true,
            success : function(data) {
                if(data.status == 'False'){
                    Swal.fire({
                        title: 'Error!',
                        icon: 'error',
                        text: 'Validation Failed. Please try again.',
                    })              
                    return
                }
                Swal.fire({
                    title: 'Success',
                    icon: 'success',
                  })              
                // console.log('Data: '+JSON.stringify(data));
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
    });
  });

  function campaignSessionOutputUpdate(vol) {
    $('#page_Seesion_volumn').text(vol);
  }

  // delete the keyword
  function delete_keyword(keyword_id) {
    // var keyword_id = $(this).attr("keyword-id");
    // alert(keyword_id);
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        // ajax request
        $.ajax({
            type: "DELETE",
            url: "/keyword-detail/"+keyword_id+"/",
            success : function(data) {
                Swal.fire(
                  'Deleted!',
                  'Your keyword has been deleted.',
                  'success'
                )
                // keyword_row_2
                $('#keyword_row_'+keyword_id).hide();
                // window.location.href = window.location.protocol + "//" + window.location.host + "/";
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
  };

  function Upgrade() {
    // alert("Please Upgrade your plan to add keywords");
    Swal.fire({
      title: '<strong>Upgrade Your Plan</strong>',
      icon: 'info',
      html:
        'You can see our <b>Plans</b> ' +
        '<a href="/custom-Price/">here</a> '
    })
  }

  function getSearchPlanFeatures(){
    console.log("getSearchPlanFeatures")
    return $.ajax({
        type: "POST",
        url: "/get-search-plan/",
        data: {},
        dataType: "json",
        encode: true,
        success : function(data) { 
            console.log(data);
        },
        error : function(request,error)
        {console.log("Request: "+JSON.stringify(request));}
    });
  }