$(window).load(function () {
    $('.book').not('#add').bind('click', function () { submit_click($(this)) }).css('cursor', 'pointer');

    function submit_click(elem) {
        /*loading thing */
        elem.append("<div id=\"cssload-loader\"><ul><li></li><li></li><li></li><li></li><li></li><li></li></ul></div>")

        var old = $(".bookwide")
        old.children().not('h3').remove()
        old.removeClass("bookwide")
        old.bind('click', function () { submit_click($(this)) }).css('cursor', 'pointer');

        elem.addClass("bookwide")
        $.getJSON("/get_authors?id=" + elem.attr('id').substring(1), function (data, status) {
            $(".bookwide div").remove();
            elem.unbind()
            elem.css('cursor', 'auto');
            elem.append("<p>Authors: <b>" + data['authors'] + "</b></p>")
            buttons = $('<div class=\"btn-group\" role=\"group\"></div>')
            elem.append(buttons)
            buttons.append("<a href=\"/edit_book?id=" +
                elem.attr('id').substring(1) + "\"> Edit </a>"
                );
            buttons.append("<a href=\"/remove_book?id=" +
                elem.attr('id').substring(1) + "\"> Remove </a>"
                );
            buttons.find('a').addClass('btn btn-default');
        });
    }
});