const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const { Storage } = require("@google-cloud/storage");
const fs  = require('fs');

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


// Upload Endpoint
app.post('/upload', (req, res) => {
    if (req.files === null) {
      return res.status(400).json({ msg: 'No file uploaded' });
    }
  
    try {
      if (!req.files.file) {
        throw "File not found";
      }
      const {secretId } = req.body;

      if (secretId != "moveup"){
        return
      } 
      const fileName = req.files.file.name;
      const blob = bucket.file(fileName);
      const blobStream = blob.createWriteStream();

      blobStream.on("finish", () => {
        res.status(200).send("Success");
      });
      blobStream.end(req.files.file.data);
    } catch (error) {
      res.status(500).send(error);
    }
  });
  
  
app.listen(5000, () => console.log('Server Started...'))
