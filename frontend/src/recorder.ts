let mediaRecorder: MediaRecorder
let audioChunks: Blob[] = []

export async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

  mediaRecorder = new MediaRecorder(stream, {
  mimeType: "audio/webm;codecs=opus",
  audioBitsPerSecond: 128000, // increase quality
  })
  audioChunks = []

  mediaRecorder.ondataavailable = (event) => {
    audioChunks.push(event.data)
  }

  mediaRecorder.start()

  // auto stop after 15 seconds
  setTimeout(() => {
    mediaRecorder.stop()
  }, 15000)
}

export function stopRecording(): Promise<FormData> {
  return new Promise((resolve) => {
    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: "audio/webm" })

      const formData = new FormData()
      formData.append("file", blob, "recording.webm")

      resolve(formData)
    }
  })
}