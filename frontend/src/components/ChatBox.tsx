import { useEffect, useRef, useState } from "react";
import API from "../services/api";
import type { AskResponse, Source } from "../types";

interface ChatBoxProps {
  documentReady: boolean;
  uploadedFileName: string;
  selectedDocumentIds: string[];
}

interface ChatMessage {
  question: string;
  answer: string;
  sources: Source[];
}

function ChatBox({ documentReady, selectedDocumentIds }: ChatBoxProps) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const documentIdsPayload = selectedDocumentIds.length > 0 ? selectedDocumentIds : null;

  const copyAnswer = async (answer: string, index: number) => {
    await navigator.clipboard.writeText(answer);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const downloadAnswer = (answer: string, index: number) => {
    const blob = new Blob([answer], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `edurag-answer-${index + 1}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const pushMessage = (question: string, answer: string, sources: Source[] = []) => {
    setMessages((prev) => [...prev, { question, answer, sources }]);
  };

  const askQuestion = async () => {
    if (!question.trim()) return;

    if (!documentReady) {
      pushMessage(question, "Please upload a PDF document first before asking questions.");
      return;
    }

    const currentQuestion = question;

    try {
      setLoading(true);
      setQuestion("");

      const response = await API.post<AskResponse>("/agent", {
        question: currentQuestion,
        document_ids: documentIdsPayload,
      });

      pushMessage(currentQuestion, response.data.answer, response.data.sources || []);
    } catch {
      pushMessage(currentQuestion, "Something went wrong. Please check your backend server.");
    } finally {
      setLoading(false);
    }
  };

  const runAction = async (label: string, endpoint: string) => {
    if (!documentReady) {
      pushMessage(label, `Please upload a PDF document first before using this.`);
      return;
    }

    try {
      setLoading(true);
      const response = await API.post<AskResponse>(endpoint, {
        question: "",
        document_ids: documentIdsPayload,
      });
      pushMessage(label, response.data.answer, response.data.sources || []);
    } catch {
      pushMessage(label, `Something went wrong while running "${label}".`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="chat-section">
      <div className="chat-header">
        <h2 className="section-title">Ask Your Document</h2>
        {messages.length > 0 && (
          <button className="clear-chat-button" onClick={() => setMessages([])}>
            Clear Chat
          </button>
        )}
      </div>

      <div className="quick-actions">
        <button onClick={() => runAction("Summarize document", "/summary")} disabled={!documentReady || loading}>
          Summarize
        </button>
        <button onClick={() => runAction("Generate quiz", "/quiz")} disabled={!documentReady || loading}>
          Generate Quiz
        </button>
        <button onClick={() => runAction("Key Topics", "/topics")} disabled={!documentReady || loading}>
          Key Topics
        </button>
        <button onClick={() => runAction("Explain Simply", "/explain")} disabled={!documentReady || loading}>
          Explain Simply
        </button>
      </div>

      <textarea
        className="question-box"
        value={question}
        placeholder="Ask a question, or try 'summarize this' or 'quiz me'..."
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button className="ask-button" onClick={askQuestion} disabled={!documentReady || loading}>
        {loading ? "Thinking..." : "Ask Question"}
      </button>

      <div className="chat-history">
        {messages.length === 0 ? (
          <div className="answer-card">
            <h3>Answer</h3>
            <p className="empty-text">Your answer will appear here.</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div className="message-card" key={index}>
              <div className="user-message">
                <strong>You</strong>
                <p>{message.question}</p>
              </div>

              <div className="ai-message">
                <div className="answer-header">
                  <strong>EduRAG Assistant</strong>
                  <button className="copy-button" onClick={() => copyAnswer(message.answer, index)}>
                    {copiedIndex === index ? "✅ Copied!" : "📋 Copy"}
                  </button>
                  <button className="download-button" onClick={() => downloadAnswer(message.answer, index)}>
                    ⬇ Download
                  </button>
                </div>

                <p className="answer-text">{message.answer}</p>

                {message.sources.length > 0 && (
                  <div className="sources">
                    <h4>Sources</h4>
                    {message.sources.map((source, sourceIndex) => (
                      <span className="source-badge" key={sourceIndex}>
                        {source.file} — Page {source.page}
                      </span>
                    ))}
                    <div ref={messagesEndRef} />
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </section>
  );
}

export default ChatBox;