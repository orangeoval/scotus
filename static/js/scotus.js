$(document).ready(function(){
    // Hide messages for sessions with js disabled
    $('.js-disabled').hide();

    // Show loading wheel when click verify
    $('input[value="Verify"]').click(function () {
        $('div.load-wheel').show();
    });

    //$('.overview').css( 'border', '3px solid red');
    $('.overview').css( 'top', '275px');
});
