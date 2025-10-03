# Task at hand
given the components for the audio generation and data insertion sections , you need to create a module for the project which :
1. Takes a csv consisting of article details such as article title , description , source etc.
2. extracts description from the details and generates a SSML based script which will fed to the TTS service using gemini.
3. creates audio file for this SSML using Azure TTS.
4. inserts the audio generated into backblaze bucket.
5. if all the steps till now go according to plan , insert the data for the article in Cockroach DB database.
6. if there is a hiccup in a step before step 5 , repeat n times before skipping the moving on to the next one.
7. After completing this for every article in the CSV , return to the user the succesfull insertions in the database.

# things to keep in mind
1. Ensure that the SSML follows a consistent style in terms of speakers , pacing , emphasis points etc. so that the articles feel similar in style.
2. In order to save time , multi threading of some sorts which can be used in deployment should be implemented.
3. DON'T LEAK ANY API KEYS !!!

- After figuring all of this out , deploy the module .
