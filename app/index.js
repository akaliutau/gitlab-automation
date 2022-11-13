/**
 * This is a simple node application
 *
 * You can then start the application with `npm start`.
 *
 */
var express = require('express');
var app = express();

var port = process.env.PORT || 8080;

app.get('/', express.static(__dirname + '/static'));

app.listen(port, function(err) {
    if (err) {
        console.log('Application failed to start', err);
        return;
    }
    console.log('Application listening on port ' + port);
});