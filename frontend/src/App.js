import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [documents, setDocuments] = useState([]);
  const [stats, setStats] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchStats();
    fetchDocuments();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:8000/stats/');
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchDocuments = async () => {
    try {
      const response = await fetch('http://localhost:8000/documents/');
      const data = await response.json();
      setDocuments(data);
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload/', {
        method: 'POST',
        body: formData,
      });
      
      if (response.ok) {
        alert('Document uploaded successfully!');
        fetchStats();
        fetchDocuments();
      } else {
        alert('Upload failed');
      }
    } catch (error) {
      alert('Error uploading file');
    } finally {
      setUploading(false);
    }
  };

  const formatBytes = (bytes) => {
    if (bytes === 0 || bytes === undefined || bytes === null) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getSavingsText = (original, optimized) => {
    if (original === 0 || original === undefined || optimized === undefined) {
      return '0 Bytes (0.0%)';
    }
    
    const bytesSaved = original - optimized;
    const percent = ((bytesSaved / original) * 100).toFixed(1);
    
    if (bytesSaved >= 0) {
      return `${formatBytes(bytesSaved)} (${percent}%)`;
    } else {
      return `+${formatBytes(Math.abs(bytesSaved))} (${percent}%)`;
    }
  };

  const getSavingsColor = (original, optimized) => {
    if (original === 0 || original === undefined || optimized === undefined) {
      return 'savings-neutral';
    }
    
    const bytesSaved = original - optimized;
    return bytesSaved >= 0 ? 'savings-positive' : 'savings-negative';
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Document Management</h1>
        <p>Intelligent document reduction and deduplication</p>
      </header>

      <div className="upload-section">
        <h2>Upload Document</h2>
        <input 
          type="file" 
          onChange={handleFileUpload}
          disabled={uploading}
        />
        {uploading && <p>Uploading and processing...</p>}
      </div>

      {stats && (
        <div className="stats-section">
          <h2>Storage Statistics</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Documents</h3>
              <p className="stat-value">{stats.total_documents}</p>
            </div>
            <div className="stat-card">
              <h3>Original Size</h3>
              <p className="stat-value">{formatBytes(stats.total_original_size)}</p>
            </div>
            <div className="stat-card">
              <h3>Optimized Size</h3>
              <p className="stat-value">{formatBytes(stats.total_optimized_size)}</p>
            </div>
            <div className="stat-card">
              <h3>Total Savings</h3>
              <p className={`stat-value ${getSavingsColor(stats.total_original_size, stats.total_optimized_size)}`}>
                {getSavingsText(stats.total_original_size, stats.total_optimized_size)}
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="documents-section">
        <h2>Recent Documents</h2>
        <table className="documents-table">
          <thead>
            <tr>
              <th>Filename</th>
              <th>Type</th>
              <th>Original Size</th>
              <th>Optimized Size</th>
              <th>Savings</th>
              <th>Tier</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {documents.slice(0, 10).map(doc => (
              <tr key={doc.id}>
                <td>{doc.original_filename}</td>
                <td>{doc.file_type || 'N/A'}</td>
                <td>{formatBytes(doc.original_size)}</td>
                <td>{formatBytes(doc.optimized_size)}</td>
                <td className={getSavingsColor(doc.original_size, doc.optimized_size)}>
                  {getSavingsText(doc.original_size, doc.optimized_size)}
                </td>
                <td>
                  <span className={`tier-badge tier-${doc.tier || 'cold'}`}>
                    {doc.tier || 'cold'}
                  </span>
                </td>
                <td>
                  {doc.is_duplicate ? (
                    <span className="duplicate-badge">Duplicate</span>
                  ) : (
                    <span className="original-badge">Original</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;