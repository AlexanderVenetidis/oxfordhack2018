
AWS.config.region = 'eu-west-1'; // 1. Enter your region

AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'eu-west-1:e3b4700b-bb7e-4e7a-860f-35dae0bcc4eb' // 2. Enter your identity pool
});

AWS.config.credentials.get(function(err) {
    if (err) alert(err);
    console.log(AWS.config.credentials);
});

var bucketName = 'pictureswithstudents'; // Enter your bucket name
var bucket = new AWS.S3({
    params: {
        Bucket: bucketName
    }
});

var fileChooser = document.getElementById('thebutton');
var button = document.getElementById('button');
var results = document.getElementById('results');
button.addEventListener('click', function() {

    var file = fileChooser.files[0];

    if (file) {

        results.innerHTML = '';
        var objKey = file.name;
        var params = {
            Key: objKey,
            ContentType: file.type,
            Body: file,
            ACL: 'public-read'
        };

        bucket.putObject(params, function(err, data) {
            if (err) {
                results.innerHTML = 'ERROR: ' + err;
            } else {
                listObjs();
            }
        });
    } else {
        results.innerHTML = 'Nothing to upload.';
    }
}, false);
function listObjs() {
    var prefix = 'testing';
    bucket.listObjects({
        Prefix: prefix
    }, function(err, data) {
        if (err) {
            results.innerHTML = 'ERROR: ' + err;
        } else {
            var objKeys = "";
            data.Contents.forEach(function(obj) {
                objKeys += obj.Key + "<br>";
            });
            results.innerHTML = objKeys;
        }
    });
}
