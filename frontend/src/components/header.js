import React, { Component } from 'react';
import '../styles/header.css';
import groupsvg from './Group.svg';
import Spinner from './spinner1.svg';

class Header extends Component {
    constructor(props) {
        super(props);
        this.state = {
            fileName: '',
            errorMessage: '',
            isLoading: false 
        };
    }

    handleFileUpload = async (event) => {
        const file = event.target.files[0];
        const fileName = file ? file.name : '';

        if (file && file.type !== 'application/pdf') {
            this.setState({ errorMessage: 'Unsupported file type. Please upload a PDF file.', fileName: '', isLoading: false });
            return;
        }

        this.setState({ fileName, errorMessage: '', isLoading: true }); // Updating state with the file name and set loading state

        event.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('http://127.0.0.1:8000/uploadfile/', {
                method: 'POST',
                body: formData,
            });
            const result = await response.json();
            if (response.ok) {
                alert(`File uploaded successfully: ${result.filename}`);
            } else {
                this.setState({ errorMessage: result.error });
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Error uploading file');
        } finally {
            this.setState({ isLoading: false }); // Reset loading state
        }
    };

    render() {
        const { fileName, errorMessage, isLoading } = this.state;

        return (
            <div className="header">
                <div className="logo">
                    <img src="./AI_Planet_Logo.png" alt="Company Logo" className='img' />
                </div>
                <div className="file-name">
                    {isLoading ? (
                        <div className="uploading-container">
                            <span>Uploading...</span>
                            <img src={Spinner} alt="Loading..." className="spinner" />
                        </div>
                    ) : (
                        fileName && <span className="green"><img src={groupsvg} alt="file" />{fileName}</span>
                    )}
                </div>
                <div className="upload-button">
                    <label htmlFor="fileInput" className="custom-file-upload">
                        Upload PDF
                    </label>
                    <input type="file" id="fileInput" name="file" required style={{ display: 'none' }} onChange={this.handleFileUpload} />
                </div>
                {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
            </div>
        );
    }
}

export default Header;
