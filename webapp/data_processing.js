
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

AWS.config.update({
  region: "eu-west-1",
  endpoint: 'dynamodb.eu-west-1.amazonaws.com',
  // accessKeyId default can be used while using the downloadable version of DynamoDB.
  // For security reasons, do not store AWS Credentials in your files. Use Amazon Cognito instead.
  accessKeyId: "AKIAI4V6BUXBIVO6V74A",
  // secretAccessKey default can be used while using the downloadable version of DynamoDB.
  // For security reasons, do not store AWS Credentials in your files. Use Amazon Cognito instead.
  secretAccessKey: "nW0CINrQAjWdhK4yeDHNAayfSi57eWB/sucL8JTy"
});

var flagvid = false;
var flagspeech = false;

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

        var loader = document.getElementById("loader");
        loader.style.opacity=0.8



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
window.setInterval(function(){
  if (flagvid == false){
    readItemVid();
  }
  if (flagspeech == false){
    readItemSpeech();
  }

  /// call your function here
}, 2000);

var docClient = new AWS.DynamoDB.DocumentClient();

function readItemVid() {
  var table = "Frames";


  var params = {
      TableName: table

  };
  var datavid = docClient.scan(params, function(err, data) {
      if (err) {

          // document.getElementById('textarea').innerHTML = "Unable to read item: " + "\n" + JSON.stringify(err, undefined, 2);
      } else {
        flagvid = true;
        var loader = document.getElementById("loader");
        loader.style.opacity=0;
        w3.displayObject("vidtable", JSON.parse(JSON.stringify(data, undefined, 2)));
        return JSON.parse(JSON.stringify(data, undefined, 2));      }
  })};

  function readItemSpeech() {
    var table = "Speech";


    var params = {
        TableName: table
    };
    var dataspeech = docClient.scan(params, function(err, data) {
        if (err) {

            // document.getElementById('textarea').innerHTML = "Unable to read item: " + "\n" + JSON.stringify(err, undefined, 2);
        } else {
          flagspeech = true;
          var loader = document.getElementById("loader");
          loader.style.opacity=0;
          w3.displayObject("speechtable", JSON.parse(JSON.stringify(data, undefined, 2)));
          return JSON.parse(JSON.stringify(data, undefined, 2));
        }
      }
    )};
