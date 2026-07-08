interface UploadScreenProps {
  onUpload: (file: File) => void
  isLoading: boolean
  error: string
}

function UploadScreen({ onUpload, isLoading, error }: UploadScreenProps) {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) onUpload(file)
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file) onUpload(file)
  }

  return (
    <div className="upload-screen">
      <div className="upload-header">
        <h1>Financial Report Analyser</h1>
        <p>Upload a company annual report and ask questions in plain English</p>
      </div>

      {!isLoading ? (
        <div
          className="upload-zone"
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
        >
          <div className="upload-icon">📄</div>
          <p>Drag and drop a PDF here</p>
          <span>or</span>
          <label className="upload-btn">
            Browse Files
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
          </label>
          <p className="upload-hint">Supports PDF only — annual reports, earnings documents</p>
        </div>
      ) : (
        <div className="loading-zone">
          <div className="spinner" />
          <p>Processing document...</p>
          <span>Building knowledge base from your report. This may take a few minutes.</span>
        </div>
      )}

      {error && <div className="error-msg">⚠️ {error}</div>}
    </div>
  )
}

export default UploadScreen