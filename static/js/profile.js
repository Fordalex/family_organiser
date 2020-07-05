var tl = gsap.timeline()

console.log('working')

$(document).on( 'click','#add-button', function() {
    if ($(this).hasClass('closed')) {
        // reveal the links
       tl.to('.profile-page-container', 0.5, {transform: 'translate(0, -365px)'});
       tl.to('#add-button', 0.5, {transform: 'rotateZ(45deg)', background: 'linear-gradient(120deg, #f88480, #e83939)'},'-=0.5')
       $(this).toggleClass('closed')

    } else if ($('#add-data-form-container').hasClass('closed')) {
        // hide the links
        tl.to('.profile-page-container', 0.5, {transform: 'translate(0, -454px)'})
        tl.to('#add-button', 0.5, {transform: 'rotateZ(0deg)', background: 'linear-gradient(120deg, #80f886, #39E86D)'},'-=0.5')
        $(this).toggleClass('closed')
    } else {
        // close form and hide links
        setTimeout(function() {
            $('#add-data-form-container').html('')
        }, 200)
        gsap.to('#send-button', 0.6, {transform: 'translate(0px, 80px)'})
        tl.to('.profile-page-container', 0.5, {transform: 'translate(0, -454px)'})
        tl.to('#add-button', 0.5, {transform: 'rotateZ(0deg)', background: 'linear-gradient(120deg, #80f886, #39E86D)'},'-=0.5')
        $(this).toggleClass('closed')
        $('#add-data-form-container').toggleClass('closed')
    }
});


// form animations

$(document).on('click', '#add-status-form', function() {
    if ($('#add-data-form-container').hasClass('closed')) {
        // show the form
        tl.to('.profile-page-container', 0.5, {transform: 'translate(0, -100px)'})
    } else {
        // hide the form
        
    }

    $('#add-data-form-container').toggleClass('closed')
});

$(document).on('click', '#send-button', function() {
    $('#status-form').submit()
});