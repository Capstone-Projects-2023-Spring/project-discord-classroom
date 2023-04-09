const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const { Storage } = require("@google-cloud/storage");
const fs  = require('fs');
const { createClient } = require('@supabase/supabase-js');

const app = express();

app.use(cors());
app.use(fileUpload());

let keyFilename = "mykey.json"; 



const keyFileContents = fs.readFileSync(keyFilename);
const keyFileData = JSON.parse(keyFileContents);

const projectId = keyFileData.project_id;
const bucketName = keyFileData.bucket_name;

const storage = new Storage({
  projectId,
  keyFilename,
});

const bucket = storage.bucket(bucketName); 


const supabaseUrl  = keyFileData.supabaseUrl
const supabaseKey = keyFileData.supabaseKey
const supabase = createClient(supabaseUrl, supabaseKey);

// Upload Endpoint
app.post('/upload', async (req, res) => {
    const secretId = req.query.token;

    
    const { data: tokens, error } = await supabase.from('Tokens').select('unique_id, created_at');
    let proceed = false;

    if (error) {
      console.error(error);
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
      return res.status(401).json({ msg: 'Unable to upload' });
    }

    
    if (req.files === null) {
      return res.status(400).json({ msg: 'No file uploaded' });
    }
  
    try {
      if (!req.files.file) {
        throw "File not found";
      }

     
      const fileName = req.files.file.name;
      const blob = bucket.file(fileName);
      const blobStream = blob.createWriteStream();

      blobStream.on("finish", async () => {
        const publicUrl = `https://storage.googleapis.com/${bucketName}/${fileName}`;
        res.status(200).json({ url: publicUrl });
      
      });

      blobStream.end(req.files.file.data);
    } catch (error) {
      res.status(500).send(error);
    }
  });
  
  
app.listen(5000, () => console.log('Server Started...'))