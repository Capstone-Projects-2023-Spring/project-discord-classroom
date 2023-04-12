const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const { Storage } = require("@google-cloud/storage");
const fs  = require('fs');
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

const app = express();

app.use(cors());
app.use(fileUpload());

if (process.env.NODE_ENV === 'production') {
  // Exprees will sere up production assets
  app.use(express.static('client/build'));

  // Express serv up index.html fil if it doesn't recognize route
  const path = require('path');
  app.get('*', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'client', 'build', 'index.html'));
  });
}

const keyFilename = process.env.MY_KEY_FILENAME

const projectId = process.env.MY_PROJECT_ID;
const bucketName = process.env.MY_BUCKET_NAME;
const type = process.env.MY_TYPE;
const private_key_id = process.env.MY_PRIVATE_KEY_ID
const private_key = process.env.MY_PRIVATE_KEY
const client_email = process.env.MY_CLIENT_EMAIL
const client_id = process.env.MY_CLIENT_ID
const auth_uri = process.env.MY_AUTH_URI
const token_uri = process.env.MY_TOKEN_URI
const auth_provider_x509_cert_url = process.env.MY_AUTH_PROVIDER_X509_CERT_URL
const client_x509_cert_url = process.env.MY_CLIENT_X509_CERT_URL


const storage = new Storage({
  projectId,
  credentials:{
    type : type,
    private_key_id:private_key_id,
    private_key:private_key,
    client_email:client_email,
    client_id:client_id,
    auth_uri:auth_uri,
    token_uri:token_uri,
    auth_provider_x509_cert_url:auth_provider_x509_cert_url,
    client_x509_cert_url:client_x509_cert_url,
    bucketName:bucketName


  },
});

const bucket = storage.bucket(bucketName); 

const supabaseUrl  = process.env.MY_SUPABASE_URL;
const supabaseKey = process.env.MY_SUPABASE_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);


// Upload Enpoint
app.post('/upload', async (req, res) => {
  const secretId = req.query.token;
  console.log("Secret ID: ", secretId);

  const { data: tokens, error } = await supabase.from('Tokens').select('unique_id, created_at');
  let proceed = false;

  if (error) {
    console.error(error);
    return res.status(500).json({ msg: 'Unable to retrieve tokens' }); // add this line to send a response to the client
  } else {
    const currentTime = new Date(); // get the current time

    tokens.forEach(token => {
      const tokenTime = new Date(token.created_at); // get the token's creation time
      const timeDiffInMinutes = (currentTime - tokenTime) / (1000 * 60); // get the time difference in minutes
      if (token.unique_id === secretId) {
        if (timeDiffInMinutes <= 10) {
          proceed = true
        } 
        return;
      }
    });
  }
  if(!proceed) {
    console.log("Unable to proceed");
    return res.status(401).json({ msg: 'Unable to upload file' });
  }
  console.log("ok so we have a working token", proceed);

  
  if (req.files === null) {
    console.log("No file uploaded");
    return res.status(400).json({ msg: 'No file uploaded' });
  }

  try {
    console.log("Fileee found");
    const fileName = req.files.file.name;
    console.log("File Name: ", fileName);
    const blob = bucket.file(fileName);
    const blobStream = blob.createWriteStream();

    blobStream.on("finish", async () => {
      console.log("File upload finished");
      const publicUrl = `https://storage.googleapis.com/${bucketName}/${fileName}`;
      res.status(200).json({ url: publicUrl });
    });

    blobStream.end(req.files.file.data);
  } catch (error) {
    console.log("Error: ", error);
    res.status(500).send(error);
  }
});

  proceed = false
  
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server started on port ${PORT}`));
  