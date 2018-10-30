import React from 'react';
import icon from './icon.png';
import './App.css';
import {askForPermissionToReceiveNotifications} from './push-notification';
import FacebookLogin from 'react-facebook-login';
import aws_exports from './aws-exports';
import Amplify from 'aws-amplify';

var userName;

const responseFacebook = (response) => {
  console.log(response);
  
  userName = response.name.replace(/\s/g, '');

  Amplify.configure({
    Auth: {
        identityPoolId: aws_exports.aws_cognito_identity_pool_id, 
        region: aws_exports.aws_project_region
    },
    Analytics:
    {
      endpointId: response.name,
      appId: aws_exports.aws_mobile_analytics_app_id,
      region: aws_exports.aws_project_region,
    }
  });
}

const componentClicked = event => {
  console.log("clicked", event)
}

const App = () => (
  <div className="App" id="demo">
    <header className="App-header">
      <img src={icon} className="App-logo" alt="icon" />
      <h1 className="App-title">Welcome to the push-notification demo !</h1>
    </header>
    <div>
    <FacebookLogin appId="your_app_id"
                   autoLoad={true}
                   fields="name,email,picture"
                   onClick={componentClicked}
                   callback={responseFacebook} />
    </div>
    <button onClick={() => askForPermissionToReceiveNotifications(userName)} >
      Click here to receive notifications
    </button>
  </div>
);

export default App;
