# re:Invent Workshop MOB314
Perform Social Media Sentiment Analysis with Pinpoint and Comprehend

## Video demo at AWS re:Invent 2018
[![Alt text](https://img.youtube.com/vi/0SVtt5wz_rE/0.jpg)](https://www.youtube.com/watch?v=0SVtt5wz_rE)

## Use Case
Imagine you are a brand with a large web and mobile presence. You want to monitor the conversation around your brand on social media and message your promoters/influencers and detractors across multiple channels. AWS and Pinpoint provide a great foundation for doing so easily and at massive scale.

## Demo
![Screenshot](images/pinpointdemo.gif)

## Architecture
![Screenshot](images/arch.png)

## Prereqs

1. Install Git by following the instructions here: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git. 
2. Install NPM and Node.js by following the instructions here: https://www.npmjs.com/get-npm. 
3. Install the Amplify CLI globally with `npm install -g @aws-amplify/cli`. If you get permission errors, try `sudo npm install -g @aws-amplify/cli`. If you are still getting issues installing on your local machine, it may be easier to run this workshop in a fresh [Cloud9 IDE](https://aws.amazon.com/cloud9/) or [Amazon Workspace](https://aws.amazon.com/workspaces/).
4. Download Google Chrome if you don't have it already: https://www.google.com/chrome/. 

## Steps

1. Clone this repo with `git clone https://github.com/mgdombrowski/mob314`
2. Change into your repo directory in the terminal with `cd mob314`.
3. Install dependencies with `npm install`
4. Configure the Amplify CLI with `amplify configure`
5. Initialize your Amplify project with `amplify init`. Follow the prompts and choose the selections shown below. You can substitute in whatever text editor you'll be using: 
![Screenshot](images/amplify-init.png)
6. While your project is initializing, create a Firebase account at https://firebase.google.com/. Add a new project and write down your credentials using the process outlined here: https://firebase.google.com/docs/cloud-messaging/concept-options#credentials. You will need your *Sender ID* and *Server Key*, both of which can be found in the Cloud Messaging tab of the Firebase console Settings pane.
![Screenshot](images/firebase1.png)
![Screenshot](images/firebase2.png)
7. Add notifications with `amplify add notifications`, *choose FCM*, choose the default generated Pinpoint project name, and paste your Firebase Server Key from the previous step.
8. Push your local changes to the cloud with `amplify push`. A file `/src/aws-exports.js` was created in your local project. Open this up and copy the `aws_mobile_analytics_app_id`.
9.  Launch the backend of the solution with a CloudFormation template using the link here: https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/create/review?stackName=PinpointStack&templateURL=https://s3.amazonaws.com/mattd-customer-share/mob314.template.yaml. For the parameters, add in your Pinpoint app ID you just copied from Step 8 above. Choose *Next* to accept defaults, select the checkbox at the bottom to acknowledge that CloudFormation may create IAM resources, then click *Create*. 
![Screenshot](images/cfn-capabilities.png)
The stack will take about 15 minutes to launch. When complete, note the `apiGatewayInvokeURL` in the *Outputs* tab of the CloudFormation stack, which we will use later to configure a Facebook Webhook.
10. Create a Facebook developer account at https://developers.facebook.com/. Create a new application and copy the application ID.
11. In `/src/App.js` in your local project, add your Facebook app ID from the previous step to the line that reads: ```<FacebookLogin appId="your_app_id_here"```.
12. In `/public/firebase-messaging-sw.js` in your local project, add your Google sender ID from step 6 above to the line that reads: ```messagingSenderId: 'your_sender_ID_here'```. Do the same again for the file `/src/push-notification.js`. Make sure you save your changes to the files.
13. Add the *Facebook Login* product to your Facebook app from the app dashboard. For the platform, select *Web (WWW)*. For the *Site URL*, enter `localhost:3000`.
![Screenshot](images/fblogin.png)
14. Add the *Webhooks* product to your Facebook app:
![Screenshot](images/add-webhooks.png)
14. In the drop-down menu select *Page*, then *Subscribe to this object*:
![Screenshot](images/subscribe.png). For *Callback URL*, paste in the output `apiGatewayInvokeURL` from the CloudFormation template in *Step 8* above. For *Verify Token*, paste in `ThisIsAToken`. 
15. Click the *Subscribe* button under *feed*. This ensures and feed updates on your Facebook page are subscribed to in real-time via Webhook.
16. Take your app public by pressing the big on button in your Facebook app dashboard: 
![Screenshot](images/app-public.png) You'll have to add a privacy policy URL, for now you can just enter `https://aws.amazon.com/privacy/`. You also have to add an *App Domain*, so enter `localhost`.
17. Service workers and Facebook login require serving content over HTTPS. To test this locally, we need to launch Chrome with a flag to accept self-signed SSL certificates. 

On a Mac, run: 
```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --user-data-dir=/tmp/foo --ignore-certificate-errors --unsafely-treat-insecure-origin-as-secure=https://localhost:3000
```
For Windows:

```
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --ignore-certificate-errors --unsafely-treat-insecure-origin-as-secure=https://localhost:3000
```

18. In your local project, launch the app with `npm start`. You should see Chrome open to `https:localhost:3000`. 
19. Login with Facebook with the first button then click the second button to register for push notifications. You can open the Chrome Javascript console to see the responses from Facebook and Firebase as your authenticate. 
![Screenshot](images/app.png)
Now minimize the window to ensure you get the push notification while the app is in the background.
20. Test the pipeline by pressing the *Test* button in your Facebook app's Webhook settings next to the *feed* . You should get a browser push notification within a few seconds thanking you for feedback and asking if you want to take a survey.
![Screenshot](images/test.png)
21. Follow your Facebook post through the pipeline:
- Navigate to your [Lambda function](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions). You should see a Lambda function called `PinpointStack-LambdaFunctionPost-*`, which should also be the *Last modified*. Click on the *Monitoring* tab, then *View Logs in CloudWatch*. Drill into the latest Log Stream and review the Lambda execution logs. What was the sentiment score?
- Navigate to the [S3 console](https://s3.console.aws.amazon.com/s3/home?region=us-east-1) and see the object that was created by your post.
- Navigate to the [ElasticSearch console](https://console.aws.amazon.com/es/home?region=us-east-1#). Click on the `page-updates` domain and the Kibana endpoint to visualize your page update. Click the *Discover* tab on the left and look at the documents that were indexed in real-time. To use Kibana, you must configure at least one index pattern. Kibana uses these patterns to identity which indices you want to analyze. For this tutorial, enter `page_updates*` and choose *Create*.
- Navigate to the [Pinpoint console](https://console.aws.amazon.com/pinpoint/home/?region=us-east-1#/apps). Drill into the app you created using the Amplify CLI and click on *Segments* on the sidebar. Create a segment and add a filter by user. You should see a user attribute for *Sentiment* appear and if you select it, an estimate of 1 endpoint will be targeted. You can now schedule a recurring push campaign to target users with positive, neutral or negative sentiment! 

## Bonus

1. Submit your app for Facebook review and configure against a live Facebook page.
2. How would you add hosting to publish this local site as a static page on S3/CloudFront?
3. Install this PWA on an Android device or emulator and test out push notification and offline capability.
4. What would this solution look like using Twitter APIs instead of Facebook?
5. How would you implement this solution as a native mobile app instead of a PWA?

## Cleanup

1. Delete any objects from your S3 bucket.
2. Delete stack in CloudFormation console: https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks?filter=active. 
3. In your mobile project, run `amplify delete` to delete cloud resources for your project.
