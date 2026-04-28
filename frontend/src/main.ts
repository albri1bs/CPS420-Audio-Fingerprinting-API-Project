import './style.css'
import { identifyAudio } from './api'
import { startRecording, stopRecording } from './recorder'

// elements
const statusEl = document.querySelector("#status") as HTMLElement
const resultEl = document.querySelector("#result") as HTMLElement

// =======================
// Upload
// =======================
document.querySelector("#uploadBtn")?.addEventListener("click", async () => {
  const input = document.querySelector("#fileInput") as HTMLInputElement
  const file = input.files?.[0]

  if (!file) {
    alert("Please select a file")
    return
  }

  const formData = new FormData()
  formData.append("file", file)

  statusEl.innerText = "Uploading..."

  try {
    const data = await identifyAudio(formData)

    console.log("Response:", data)

    resultEl.innerText = JSON.stringify(data, null, 2)
    statusEl.innerText = "Done"

  } catch (err) {
    console.error(err)
    statusEl.innerText = "Error"
  }
})


// =======================
// Recording
// =======================
document.querySelector("#recordBtn")?.addEventListener("click", async () => {
  statusEl.innerText = "Recording..."
  await startRecording()
})

document.querySelector("#stopBtn")?.addEventListener("click", async () => {
  statusEl.innerText = "Processing..."

  try {
    const formData = await stopRecording()
    const data = await identifyAudio(formData)

    resultEl.innerText = JSON.stringify(data, null, 2)
    statusEl.innerText = "Done"

  } catch (err) {
    console.error(err)
    statusEl.innerText = "Error"
  }
})