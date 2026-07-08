import { useState } from "react"

const SUGGESTED_QUESTIONS = [
  "What were the main revenue drivers this year?",
  "What risks did management highlight?",
  "How did net profit change year on year?",
  "What are the company's growth plans?",
]

interface ChatScreenProps {
  summary: string
  onReset: () => void
}

interface Message {
  role: "user" | "bot"
  text: string
  sources?: string[]
}

function ChatScreen({ summary, onReset }: ChatScreenProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isAsking, setIsAsking] = useState(false)
  const [expandedSources, setExpandedSources] = useState<Record<number, boolean>>({})

  const askQuestion = async (question: string) => {
    if (!question.trim() || isAsking) return

    const userMessage: Message = { role: "user", text: question }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsAsking(true)

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      })

      const data = await res.json()
      const botMessage: Message = {
        role: "bot",
        text: data.answer,
        sources: data.sources,
      }
      setMessages((prev) => [...prev, botMessage])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Something went wrong. Please try again.", sources: [] },
      ])
    } finally {
      setIsAsking(false)
    }
  }

  const toggleSources = (index: number) => {
    setExpandedSources((prev) => ({ ...prev, [index]: !prev[index] }))
  }

  return (
    <div className="chat-screen">
      {/* Left panel - Chat */}
      <div className="chat-panel">
        <div className="chat-header">
          <h2>Ask the Report</h2>
          <button className="reset-btn" onClick={onReset}>
            ↩ Upload New Report
          </button>
        </div>

        <div className="messages">
          {messages.length === 0 && (
            <div className="suggested">
              <p>Suggested questions:</p>
              <div className="chips">
                {SUGGESTED_QUESTIONS.map((q) => (
                  <button key={q} className="chip" onClick={() => askQuestion(q)}>
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <p>{msg.text}</p>
              {msg.role === "bot" && msg.sources && msg.sources.length > 0 && (
                <div className="sources">
                  <button
                    className="sources-toggle"
                    onClick={() => toggleSources(i)}
                  >
                    {expandedSources[i] ? "▲ Hide Sources" : "▼ View Sources"}
                  </button>
                  {expandedSources[i] && (
                    <div className="sources-list">
                      {msg.sources.map((src: string, j: number) => (
                        <div key={j} className="source-chunk">
                          <span>Source {j + 1}</span>
                          <p>{src}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}

          {isAsking && (
            <div className="message bot">
              <p className="typing">Analysing report...</p>
            </div>
          )}
        </div>

        <div className="input-row">
          <input
            type="text"
            placeholder="Ask a question about the report..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && askQuestion(input)}
            disabled={isAsking}
          />
          <button onClick={() => askQuestion(input)} disabled={isAsking}>
            Ask
          </button>
        </div>
      </div>

      {/* Right panel - Summary */}
      <div className="summary-panel">
        <h2>Report Summary</h2>
        <div className="summary-content">
          {summary.split("\n").map((line: string, i: number) =>
            line.trim() ? <p key={i}>{line}</p> : null
          )}
        </div>
      </div>
    </div>
  )
}

export default ChatScreen