
    $(window).load(function () {
        $('#submit').bind('click', function () { submit_click() });

        function submit_click(elem) {
            /*loading thing */
            $("#submit").hide();
            $("#form").append("<div id=\"cssload-loader\"><ul><li></li><li></li><li></li><li></li><li></li><li></li></ul></div>")
        }
    });
