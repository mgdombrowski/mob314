import firebase from 'firebase';
import aws_exports from './aws-exports';
var AWS = require('aws-sdk/dist/aws-sdk-react-native');

var myCredentials = new AWS.CognitoIdentityCredentials({IdentityPoolId: aws_exports.aws_cognito_identity_pool_id});
AWS.config.update({region: aws_exports.aws_project_region, credentials: myCredentials});
var pinpoint = new AWS.Pinpoint();

export const initializeFirebase = () => {
  firebase.initializeApp({
    messagingSenderId: 'your_sender_id' 
  });
}

export const askForPermissionToReceiveNotifications = async userName => {
  try {

    const messaging = firebase.messaging();
    await messaging.requestPermission();
    const token = await messaging.getToken();
    console.log('user token: ', token);

    var params = {
      ApplicationId: aws_exports.aws_mobile_analytics_app_id,
      EndpointId: userName.toString(),
      EndpointRequest: { 
        Address: token,
        ChannelType: 'GCM',
      }
    };
    pinpoint.updateEndpoint(params, function(err, data) {
      if (err) console.log(err, err.stack); // an error occurred
      else     console.log(data);           // successful response
    });

    return token;
  } catch (error) {
    console.error(error);
  }
}
