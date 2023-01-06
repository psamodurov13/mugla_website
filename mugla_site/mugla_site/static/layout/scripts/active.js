$(document).ready(function () {
    $('#mainav a').each(function(){
    let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
    let link = this.href;
    if(location == link) {
        $(this).parent().addClass('active');
        let secondParent = $(this).parent().parent().parent().get(0).tagName;
        if(secondParent == 'LI'){
            $(this).parent().parent().parent().addClass('active');
        }
    }
    });
});