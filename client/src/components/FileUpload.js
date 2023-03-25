import React, { Fragment, useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
  const [file, setFile] = useState();
  const [message, setMessage] = useState('');
  const [secretId, setSecretId] = useState('');

  const onChange = e => {
    if (e.target.name === 'file') {
      setFile(e.target.files[0]);
    } else if (e.target.name === 'secretId') {
      setSecretId(e.target.value);
    }
  };

  const onSubmit = async e => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    formData.append('secretId', secretId);
    try {
      await axios.post('/upload', formData, {
        headers: {
          'Content-type': 'multipart/form-data'
        }
      });

      setMessage(`${file.name} File Uploaded Successfully`);

    } catch (err) {
      if (err.response.status === 500) {
        setMessage('There was a problem with the server');
      } else {
        setMessage(err.response.data.msg);
      }
    }
  };

  const isUploadEnabled = () => {
    return file && secretId;
  };

  return (
    <Fragment>
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <input type="file" className="custom-file-input" id="customFile" name="file" onChange={onChange} />
          <label className="custom-file-label" htmlFor="customFile"> </label>
        </div>
        <div className="form-group">
          <label htmlFor="secretId">Secret ID</label>
          <input type="text" className="form-control" id="secretId" name="secretId" value={secretId} onChange={onChange} />
        </div>

        <button
          type="submit" className="btn btn-primary btn-block mt-4" disabled={!isUploadEnabled()} >
          Upload
        </button>
      </form>
      {message && ( <div style={{ backgroundColor: 'lightgreen', padding: '10px' }}> {message} </div> )}
    </Fragment>
  );
};

export default FileUpload;
