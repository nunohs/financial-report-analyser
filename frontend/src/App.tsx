import { useState } from "react"
import UploadScreen from "./components/UploadScreen"
import ChatScreen from "./components/ChatScreen"

type AppState = "upload" | "loading" | "ready"

function App() {
  const [appState, setAppState] = useState<AppState>("upload")
  const [summary, setSummary] = useState("")
  const [error, setError] = useState("")

  const handleUpload = async (file: File) => {
    setAppState("loading")
    setError("")

    const formData = new FormData()
    formData.append("file", file)

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      })

      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || "Upload failed")
      }

      // Fetch summary after successful upload
      const summaryRes = await fetch("http://localhost:8000/summary")
      const summaryData = await summaryRes.json()
      setSummary(summaryData.summary)
      setAppState("ready")
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed")
      setAppState("upload")
    }
  }

  const handleReset = () => {
    setAppState("upload")
    setSummary("")
    setError("")
  }

  return (
    <div className="app">
      {appState === "upload" || appState === "loading" ? (
        <UploadScreen
          onUpload={handleUpload}
          isLoading={appState === "loading"}
          error={error}
        />
      ) : (
        <ChatScreen summary={summary} onReset={handleReset} />
      )}
    </div>
  )
}

export default App