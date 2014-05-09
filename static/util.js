//getQueryObject
//parses URL parameters into map and returns it.
getQueryObject = function() {
    var href = document.location.href;
    var queryString = href.split('?')[1];

    if (queryString) {
        var obj = {}
        queryString.split('&').forEach(function(pair) {
            var t = pair.split('=');
            obj[t[0]] = t[1];
        });
        return obj
    }
    return {default: true}
};

//getCookieObject
//parses Cookies into a map for easy access.
getCookieObject = function() {
    var obj = {}
    if (document.cookie.trim() != '') {
        document.cookie.split(';').forEach(function(pair) {
            var t = pair.split('=')
        });
    }
    return obj;
}
cookie = getCookieObject()
