import { useEffect, useState } from "react";
import API from "../services/api";

export interface DocumentRecord {
  id: string;
  filename: string;
  chunks: number;
  uploaded_at: string;
}

interface DocumentSelectorProps {
  refreshKey: number;
  selectedIds: string[];
  onSelectionChange: (ids: string[]) => void;
  onDocumentsLoaded: (hasDocuments: boolean) => void;
}

function DocumentSelector({ refreshKey, selectedIds, onSelectionChange, onDocumentsLoaded }: DocumentSelectorProps) {
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const fetchDocuments = async () => {
    try {
      const response = await API.get("/documents");
      setDocuments(response.data.documents);
      onDocumentsLoaded(response.data.documents.length > 0);
    } catch {
      setDocuments([]);
      onDocumentsLoaded(false);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshKey]);

  const toggleDocument = (id: string) => {
    if (selectedIds.includes(id)) {
      onSelectionChange(selectedIds.filter((docId) => docId !== id));
    } else {
      onSelectionChange([...selectedIds, id]);
    }
  };

  const selectAll = () => onSelectionChange([]);

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation(); // don't trigger toggleDocument when clicking the × 

    const confirmed = window.confirm("Delete this document? This can't be undone.");
    if (!confirmed) return;

    try {
      setDeletingId(id);
      await API.delete(`/documents/${id}`);
      onSelectionChange(selectedIds.filter((docId) => docId !== id));
      await fetchDocuments();
    } catch {
      window.alert("Failed to delete document. Please try again.");
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) return null;
  if (documents.length === 0) return null;

  const isSearchingAll = selectedIds.length === 0;

  return (
    <div className="doc-selector">
      <p className="doc-selector-label">Ask within</p>
      <div className="doc-selector-list">
        <button
          className={`doc-chip ${isSearchingAll ? "active" : ""}`}
          onClick={selectAll}
        >
          All documents
        </button>
        {documents.map((doc) => (
          <div key={doc.id} className="doc-chip-wrapper">
            <button
              className={`doc-chip ${selectedIds.includes(doc.id) ? "active" : ""}`}
              onClick={() => toggleDocument(doc.id)}
              disabled={deletingId === doc.id}
            >
              {doc.filename}
              <span
                className="doc-chip-delete"
                onClick={(e) => handleDelete(e, doc.id)}
                title="Delete document"
              >
                {deletingId === doc.id ? "…" : "×"}
              </span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default DocumentSelector;