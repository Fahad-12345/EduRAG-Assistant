import { useState } from "react";
import API from "../services/api";

interface FileUploadProps {
  onUploadSuccess: (fileName: string) => void;
}

function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  const uploadFile = async () => {
    if (!file) {
      setMessage("Please select a PDF first.");
      return;
    }

    try {
      setUploading(true);
      setMessage("");

      const formData = new FormData();
      formData.append("file", file);

      await API.post("/upload", formData);
      onUploadSuccess(file.name);
      setFile(null);

      setMessage("PDF uploaded and indexed successfully.");
    } catch {
      setMessage("Upload failed. Please check backend server.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <section className="upload-section">
      <h2 className="section-title">Upload Academic Document</h2>

      <div className="upload-card">
        <div>
          <p className="upload-title">PDF Course Material</p>
          <p className="upload-subtitle">
            Upload lecture notes, assignment briefs, rubrics, or course outlines. You can add multiple documents to your workspace.
          </p>

          {file && <p className="file-name">Selected: {file.name}</p>}
        </div>

        <div className="upload-actions">
          <label className="file-label">
            Choose PDF
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </label>

          <button onClick={uploadFile} disabled={uploading}>
            {uploading ? "Uploading..." : "Upload"}
          </button>
        </div>
      </div>

      {message && <p className="status-message">{message}</p>}
    </section>
  );
}

export default FileUpload;