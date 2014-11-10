var gridster_instance = $('main div.gridster > ul').gridster({
    widget_margins: [10, 10],
    widget_base_dimensions: [120, 120]
}).data('gridster').disable();
if ($('html').attr('data-transition')) {
    $('.transition').fadeTo(400, 1);
    $('main > div.carousel').carousel('next');
    setTimeout(function() { $('main div.carousel').carousel('next'); }, 400);
}
$('a.transition').click(function() {
    var a = $(this);
    $('main > div.carousel').on('slid.bs.carousel', function () {
        if (a.attr('data-margin')) $('.transition').fadeTo(400, 0, function() {
            $('main').animate({marginTop: a.attr('data-margin')}, 400);
            $('main div.item').animate({height: a.attr('data-height')}, 400, function() { location.href = a.attr('href'); });
        });
        else $('main div.item').animate({height: a.attr('data-height')}, 400, function() { location.href = a.attr('href'); });
    });
    $('main > div.carousel').carousel('next');
    return false;
});
$('#sign_out').click(function() {
    var a = $(this);
    $('main > div.carousel').on('slid.bs.carousel', function () {
        $('.transition').fadeTo(400, 0, function() {
            $('main').animate({marginTop: 260}, 400);
            $('main div.item').animate({height: 420}, 400, function() { location.href = a.attr('href'); });
        });
    });
    $.get("/user/signout").done(function() {
        $('main > div.carousel').carousel('next');
    });
    return false;
});
