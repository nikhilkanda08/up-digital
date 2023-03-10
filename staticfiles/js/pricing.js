var values = [25, 50, 100, 150, 200, 300, 500, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 20000, 30000, 40000, 50000];
$(document).ready(function(){
    console.log("Load pricing javascript");
    
    // $('#pricing').on('input', e => $('span').text(values[e.target.value]));

            // $("#slider").roundSlider({
            //     // sliderType: "min-range",
            //     // value: 80,
            //     // svgMode: true
            //     sliderType: "min-range",
            //     circleShape: "custom-quarter",
            //     min: 0,
            //     max: 11,
            //     value: 11,
            //     startAngle: 45,
            //     editableTooltip: false,
            //     radius: 300,
            //     width: 20,
            //     handleShape: "dot",
                
            // });
    $("#handle1").roundSlider({
        sliderType: "min-range",
        editableTooltip: false,
        radius: 250,
        width: 16,
        value: 0,
        min: 0,
        max: 21,
        // value: 25,
        // min: 25,
        // max: 50000,
        handleSize: 0,
        handleShape: "square",
        circleShape: "pie",
        startAngle: 315,
        tooltipFormat: "changeTooltip"
    });
    // $("#handle1").roundSlider('option','value',50);
    $("#pricing").on('input', async function() {
      console.log($(this).val());
      let slider = values[$(this).val()];
      // let slider = $(this).val();
      console.log(slider);
      let planIndexObj = {}
      await $.getJSON( "/static/json/searchPlan.json", function( data ) {
        $.each( data, function( key, val ) {
          // console.log(key,val);
          // console.log(val.length);
          // console.log(key);
          $.each(val, function( index, value ) {
            // console.log( index + ": " + value['id'] );
            // console.log(slider);
            // console.log(value['dailySearches']);
            if(slider >= value['dailySearches']){
              // console.log( slider + ": " + value['dailySearches'] );
              // console.log( value );
              planIndexObj = value;
            }
          });
        });
      });
      console.log(planIndexObj);

      $("#handle1").roundSlider('option','value',$(this).val());
      // $("#monthly_cost").text(parseFloat(planIndexObj['perSearchCost']*slider*30).toFixed(2));
      $("#monthly_cost").text(planIndexObj['cost']);

      $("#price_plan").val(planIndexObj['stripeID']);
      $("#monthly_campaigns").text("Unlimited");
      $("#monthly_keywords").text("Unlimited");
      $("#cost_per_search").text("$"+planIndexObj['perSearchCost']);
      $("#site_time").text("Up to "+planIndexObj['time']+" seconds");
      $("#page_views").text("Up to "+planIndexObj['pages']);
      $("#geo_targetting").text("State Level");
      $("#bounce_rate").text("Between to 0% and 100%");
    })
    //stripe
    
    // Create an instance of the Stripe object with your publishable API key
    var stripe = Stripe('pk_live_51M8SqmJCDPvINMYsoD2aUt5sDXwh6JJz9PL45fP7h5N3KAFARAUPDdoXf8bwgJq0PetgQvOcNnTMtCL4uVosHFwd00pKJCyuVX');
    var checkoutButton = document.getElementById('checkout-button');

    checkoutButton.addEventListener('click', function() {
      // Create a new Checkout Session using the server-side endpoint you
      // created in step 3.
      // const data = { planID: "price_1LwuCQA06DybZIHwXlRkIv1p" };
      const data = { planID: $("#price_plan").val()};
      fetch(window.location.protocol + "//" + window.location.host + "/create-checkout-session/", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      .then(function(response) {
        console.log(response);
        return response.json();
      })
      .then(function(session) {
        console.log(session);
        if(session.status == 'true'){
          Swal.fire({
            position: 'top-end',
            icon: 'success',
            title: 'Your Plan has been upgraded.',
            showConfirmButton: false,
            timer: 1500
          })
          window.location.href = window.location.protocol + "//" + window.location.host + "/";
        }else return stripe.redirectToCheckout({ sessionId: session.id });
      })
      .then(function(result) {
        console.log(result);
        // If `redirectToCheckout` fails due to a browser or network
        // error, you should display the localized error message to your
        // customer using `error.message`.
        if (result.error) {
          alert(result.error.message);
        }
      })
      .catch(function(error) {
        console.error('Error:', error);
      });
    });
    // stripe end
    
});

function campaignSessionOutputUpdate(vol) {
  $('#page_Seesion_volumn').text(vol);
}

function changeTooltip(e) {
  var val = e.value, speed;
  if (val < 20) speed = "Slow";
  else if (val < 40) speed = "Normal";
  else if (val < 70) speed = "Speed";
  else speed = "Very Speed";
  return values[val] + "<div> Daily Searches <div>";
}

function upgrade(){
  let palnID = $("#price_plan").val();
  console.log(palnID);
  window.location.href = window.location.protocol + "//" + window.location.host + "/stripe/"+palnID+"/";
}

