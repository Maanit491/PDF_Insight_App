import React from 'react';
// import PDFUpload from './components/PDFupload';
// import AskQuestion from './components/askquestion';
import Header from './components/header';
import Chatbot from './components/chatbot';
import api from './api';

function App() {
    return (
        <div>
            <Header/>
            <Chatbot/>
            {/* <PDFUpload />
            <AskQuestion /> */}
        </div>
    );
}

export default App;
