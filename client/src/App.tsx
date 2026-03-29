import { useState, useEffect } from 'react';
import axios from 'axios';
import { FileUpload, FormatOptions, Preview, DownloadButton } from './components';
import './App.css';

const API_BASE = '/api';

interface FormatOptionsType {
  fix_title_page: boolean;
  fix_headings: boolean;
  fix_citations: boolean;
  fix_references: boolean;
  fix_spacing: boolean;
  generate_toc: boolean;
  use_ai_enhancement: boolean;
}

interface Issue {
  issue_type: string;
  description: string;
  location?: string;
  suggestion: string;
}

function App() {
  // State
  const [file, setFile] = useState<File | null>(null);
  const [fileId, setFileId] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isFormatting, setIsFormatting] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [aiAvailable, setAiAvailable] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [issuesFound, setIssuesFound] = useState<Issue[]>([]);
  const [issuesFixed, setIssuesFixed] = useState(0);

  const [options, setOptions] = useState<FormatOptionsType>({
    fix_title_page: true,
    fix_headings: true,
    fix_citations: true,
    fix_references: true,
    fix_spacing: true,
    generate_toc: true,
    use_ai_enhancement: false
  });

  // Check AI status on mount
  useEffect(() => {
    axios.get(`${API_BASE}/ai-status`)
      .then(res => setAiAvailable(res.data.available))
      .catch(() => setAiAvailable(false));
  }, []);

  // Handle file selection
  const handleFileSelect = async (selectedFile: File) => {
    setFile(selectedFile);
    setError(null);
    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await axios.post(`${API_BASE}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      setFileId(response.data.file_id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.');
      setFile(null);
    } finally {
      setIsUploading(false);
    }
  };

  // Handle format submission
  const handleFormat = async () => {
    if (!fileId) return;

    setIsFormatting(true);
    setError(null);

    try {
      const formData = new FormData();
      Object.entries(options).forEach(([key, value]) => {
        formData.append(key, String(value));
      });

      const response = await axios.post(`${API_BASE}/format/${fileId}`, formData);

      setIssuesFound(response.data.issues_found || []);
      setIssuesFixed(response.data.issues_fixed || 0);
      setDownloadUrl(response.data.download_url);
      setIsComplete(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Formatting failed. Please try again.');
    } finally {
      setIsFormatting(false);
    }
  };

  // Reset to start over
  const handleReset = () => {
    setFile(null);
    setFileId(null);
    setIsComplete(false);
    setDownloadUrl(null);
    setError(null);
    setIssuesFound([]);
    setIssuesFixed(0);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-5xl mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <span className="text-3xl">📝</span>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">APA Formatter</h1>
              <p className="text-sm text-gray-500">Transform your documents to APA 7th Edition</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 py-8">
        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
            <span className="text-red-500">⚠️</span>
            <div>
              <p className="text-red-700 font-medium">Error</p>
              <p className="text-red-600 text-sm">{error}</p>
            </div>
            <button 
              onClick={() => setError(null)}
              className="ml-auto text-red-400 hover:text-red-600"
            >
              ✕
            </button>
          </div>
        )}

        {/* Step 1: Upload */}
        {!file && (
          <div className="mb-8">
            <h2 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <span className="w-7 h-7 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm">1</span>
              Upload Your Document
            </h2>
            <FileUpload onFileSelect={handleFileSelect} isUploading={isUploading} />
          </div>
        )}

        {/* Step 2 & 3: Options & Preview */}
        {file && (
          <div className="grid md:grid-cols-2 gap-6">
            {/* Left: Options */}
            <div>
              <h2 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
                <span className="w-7 h-7 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm">2</span>
                Choose Options
              </h2>
              <FormatOptions 
                options={options} 
                onOptionsChange={setOptions} 
                aiAvailable={aiAvailable}
              />

              {/* Format Button */}
              {!isComplete && (
                <button
                  onClick={handleFormat}
                  disabled={isFormatting || !fileId}
                  className={`
                    w-full mt-4 py-3 px-6 rounded-lg font-medium text-white
                    transition-all duration-200 flex items-center justify-center gap-2
                    ${isFormatting || !fileId
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-blue-600 hover:bg-blue-700 shadow-lg shadow-blue-200'}
                  `}
                >
                  {isFormatting ? (
                    <>
                      <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Formatting...
                    </>
                  ) : (
                    <>
                      <span>✨</span>
                      Format Document
                    </>
                  )}
                </button>
              )}
            </div>

            {/* Right: Preview */}
            <div>
              <h2 className="text-lg font-semibold text-gray-700 mb-4 flex items-center gap-2">
                <span className="w-7 h-7 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm">3</span>
                Result
              </h2>
              <Preview
                filename={file.name}
                fileSize={file.size}
                isFormatting={isFormatting}
                isComplete={isComplete}
                issuesFound={issuesFound}
                issuesFixed={issuesFixed}
              />

              {/* Download Button */}
              {isComplete && (
                <div className="mt-4">
                  <DownloadButton
                    downloadUrl={downloadUrl}
                    isReady={isComplete}
                    onDownload={() => {}}
                    onReset={handleReset}
                  />
                </div>
              )}
            </div>
          </div>
        )}

        {/* APA Info Section */}
        <div className="mt-12 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📚 APA 7th Edition Quick Reference</h3>
          <div className="grid md:grid-cols-3 gap-6 text-sm text-gray-600">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Document Format</h4>
              <ul className="space-y-1">
                <li>• 1" margins on all sides</li>
                <li>• Double-spaced throughout</li>
                <li>• Times New Roman 12pt</li>
                <li>• 0.5" first-line indent</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-700 mb-2">In-Text Citations</h4>
              <ul className="space-y-1">
                <li>• (Author, Year)</li>
                <li>• (Author, Year, p. X)</li>
                <li>• Author (Year) states...</li>
                <li>• 3+ authors: et al.</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Headings (5 Levels)</h4>
              <ul className="space-y-1">
                <li>• L1: Centered, Bold</li>
                <li>• L2: Left, Bold</li>
                <li>• L3: Left, Bold Italic</li>
                <li>• L4-5: Indented...</li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-auto py-6 text-center text-sm text-gray-500">
        <p>APA Formatter • Built for students and researchers</p>
      </footer>
    </div>
  );
}

export default App;
