export async function identifyAudio(formData: FormData) {
  try {
    const res = await fetch("/api/identify", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    return await res.json();

  } catch (error) {
    console.error("API error:", error);
    throw error;
  }
}