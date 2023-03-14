import React from 'react';
import FileUpload from './components/FileUpload';
import './App.css';
<script src='https://kit.fontawesome.com/a076d05399.js' crossorigin='anonymous'></script>

const App = () => (
  <div className='container mt-4'>
    <h4 className='display-4 text-center mb-4'>
      <i className ='fab fa-discord' /> Discord Classroom File Upload

    </h4>

    <FileUpload />
  </div>
);

export default App;