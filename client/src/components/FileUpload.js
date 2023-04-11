import React, { Fragment, useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState();
  const [message, setMessage] = useState('');
  const [url, setUrl] = useState('');

  const onChange = e => {
    if (e.target.name === 'file') {
      setFile(e.target.files[0]);
    } 
  };

  const onSubmit = async e => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    const searchParams = new URLSearchParams(window.location.search);
    const secretId = searchParams.get('token');
    try {
      const response = await axios.post(`https://discord-classroom-file-uploads.herokuapp.com/upload?token=${secretId}`, formData, {
        headers: {
          'Content-type': 'multipart/form-data'
        }
      });
      const publicUrl = response.data.url;
      setMessage(`${file.name} File Uploaded Successfully.`);
      setUrl(publicUrl);
    } catch (err) {
      if (err.response.status === 500) {
        setMessage('There was a problem with the server');
      } else {
        setMessage(err.response.data.msg);
      }
    }
  };
  

  

  const isUploadEnabled = () => {
    return file;
  };

  return (
    <Fragment>
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <input type="file" className="custom-file-input" id="customFile" name="file" onChange={onChange} />
          <label className="custom-file-label" htmlFor="customFile"> </label>
        </div>
        <button type="submit" className="btn btn-primary btn-block mt-4" disabled={!isUploadEnabled()} >
          Upload
        </button>
      </form>
      {message && (
        <div className="upload-message">
          <div style={{ backgroundColor: 'lightgreen', padding: '10px' }}>
            {message}
          </div>
          {url && (
            <div className="upload-url">
              <div style={{ backgroundColor: 'lightblue', padding: '10px' }}>
                <span>{url}</span>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(url);
                  }}
                >
                Copy URL
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </Fragment>

  );
};

export default FileUpload;