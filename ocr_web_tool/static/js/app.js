/**
 * OCR Web Tool - Frontend Logic
 * Gestione upload drag & drop, fotocamera nativa, anteprima, paste da clipboard,
 * chiamate API asincrone e copia rapida negli appunti.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Riferimenti DOM
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileInput");
  const cameraInput = document.getElementById("cameraInput");
  const previewContainer = document.getElementById("previewContainer");
  const imagePreview = document.getElementById("imagePreview");
  const pdfPlaceholder = document.getElementById("pdfPlaceholder");
  const fileNameEl = document.getElementById("fileName");
  const fileSizeEl = document.getElementById("fileSize");
  const fileIconEl = document.getElementById("fileIcon");
  const removeFileBtn = document.getElementById("removeFileBtn");
  const submitOcrBtn = document.getElementById("submitOcrBtn");
  const languageSelect = document.getElementById("languageSelect");
  const preprocessSelect = document.getElementById("preprocessSelect");
  const autoRotateCheck = document.getElementById("autoRotateCheck");

  // Risultati
  const resultsCard = document.getElementById("resultsCard");
  const ocrOutput = document.getElementById("ocrOutput");
  const copyBtn = document.getElementById("copyBtn");
  const downloadBtn = document.getElementById("downloadBtn");
  const clearBtn = document.getElementById("clearBtn");
  const statTime = document.getElementById("statTime");
  const statConfidence = document.getElementById("statConfidence");
  const statChars = document.getElementById("statChars");
  const statWords = document.getElementById("statWords");
  const statPages = document.getElementById("statPages");
  const toast = document.getElementById("toast");
  const themeToggleBtn = document.getElementById("themeToggleBtn");

  // Stato file selezionato
  let currentFile = null;

  // =========================================================================
  // 1. Gestione Tema Chiaro/Scuro
  // =========================================================================
  const savedTheme = localStorage.getItem("ocr_theme") || "dark";
  applyTheme(savedTheme);

  themeToggleBtn.addEventListener("click", () => {
    const activeTheme = document.body.getAttribute("data-theme") || "dark";
    const nextTheme = activeTheme === "dark" ? "light" : "dark";
    applyTheme(nextTheme);
    localStorage.setItem("ocr_theme", nextTheme);
  });

  function applyTheme(theme) {
    document.body.setAttribute("data-theme", theme);
    const darkIcon = themeToggleBtn.querySelector(".icon-theme-dark");
    const lightIcon = themeToggleBtn.querySelector(".icon-theme-light");
    if (theme === "dark") {
      darkIcon.style.display = "block";
      lightIcon.style.display = "none";
    } else {
      darkIcon.style.display = "none";
      lightIcon.style.display = "block";
    }
  }

  // =========================================================================
  // 2. Notifiche Toast
  // =========================================================================
  let toastTimer = null;
  function showToast(message, type = "success") {
    clearTimeout(toastTimer);
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    toastTimer = setTimeout(() => {
      toast.className = "toast";
    }, 3200);
  }

  // =========================================================================
  // 3. Selezione ed elaborazione file (Upload, Drag&Drop, Fotocamera, Clipboard)
  // =========================================================================
  
  function formatBytes(bytes) {
    if (bytes === 0) return "0 Byte";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  }

  function handleFileSelected(file) {
    if (!file) return;

    const validExtensions = ["jpg", "jpeg", "png", "webp", "bmp", "tiff", "tif", "pdf"];
    const ext = file.name.split(".").pop().toLowerCase();
    
    if (!validExtensions.includes(ext)) {
      showToast(`Formato .${ext} non supportato. Usa JPG, PNG, WEBP o PDF.`, "error");
      return;
    }

    currentFile = file;
    fileNameEl.textContent = file.name;
    fileSizeEl.textContent = formatBytes(file.size);

    if (ext === "pdf") {
      fileIconEl.textContent = "📑";
      imagePreview.style.display = "none";
      pdfPlaceholder.style.display = "flex";
    } else {
      fileIconEl.textContent = "🖼️";
      pdfPlaceholder.style.display = "none";
      const reader = new FileReader();
      reader.onload = (e) => {
        imagePreview.src = e.target.result;
        imagePreview.style.display = "block";
      };
      reader.readAsDataURL(file);
    }

    previewContainer.style.display = "flex";
    previewContainer.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  // Event listener input standard e fotocamera
  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelected(e.target.files[0]);
    }
  });

  cameraInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelected(e.target.files[0]);
    }
  });

  // Drag & drop su dropZone
  ["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove("dragover");
    });
  });

  dropZone.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    if (dt && dt.files && dt.files[0]) {
      handleFileSelected(dt.files[0]);
    }
  });

  // Supporto incolla da tastiera (Ctrl+V / Cmd+V)
  window.addEventListener("paste", (e) => {
    const items = (e.clipboardData || e.originalEvent.clipboardData).items;
    for (let index in items) {
      const item = items[index];
      if (item.kind === "file") {
        const blob = item.getAsFile();
        if (blob) {
          const timestamp = new Date().toISOString().replace(/[-:T.]/g, "").slice(0, 14);
          const ext = blob.type.split("/")[1] || "png";
          const file = new File([blob], `screenshot_${timestamp}.${ext}`, { type: blob.type });
          handleFileSelected(file);
          showToast("Immagine incollata dagli appunti!", "success");
          break;
        }
      }
    }
  });

  // Rimozione file
  removeFileBtn.addEventListener("click", () => {
    resetUpload();
  });

  function resetUpload() {
    currentFile = null;
    fileInput.value = "";
    cameraInput.value = "";
    imagePreview.src = "";
    previewContainer.style.display = "none";
  }

  // =========================================================================
  // 4. Invio ed Elaborazione OCR
  // =========================================================================
  submitOcrBtn.addEventListener("click", async () => {
    if (!currentFile) {
      showToast("Seleziona prima un'immagine o documento.", "error");
      return;
    }

    const formData = new FormData();
    formData.append("file", currentFile);
    formData.append("language", languageSelect.value);
    formData.append("preprocessing", preprocessSelect.value);
    formData.append("auto_rotate", autoRotateCheck.checked ? "true" : "false");

    // Stato UI di caricamento
    const btnTextContent = submitOcrBtn.querySelector(".btn-text-content");
    const btnSpinner = submitOcrBtn.querySelector(".btn-spinner");
    submitOcrBtn.disabled = true;
    btnTextContent.style.display = "none";
    btnSpinner.style.display = "inline-block";

    try {
      // Chiamata relativa compatibile con Ingress e accesso diretto porta 5000
      const response = await fetch("api/ocr", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || `Errore HTTP ${response.status}`);
      }

      // Popola il testo estratto
      ocrOutput.value = data.text || "(Nessun testo rilevato nel documento)";
      
      // Aggiorna metriche
      statTime.textContent = `⏱ ${data.processing_time}s`;
      statConfidence.textContent = `🎯 ${data.confidence}%`;
      statChars.textContent = `🔤 ${data.char_count} car.`;
      statWords.textContent = `📝 ${data.word_count} parole`;
      
      if (data.page_count && data.page_count > 1) {
        statPages.textContent = `📄 ${data.page_count} pag.`;
        statPages.style.display = "inline-block";
      } else {
        statPages.style.display = "none";
      }

      // Mostra card risultati
      resultsCard.style.display = "block";
      resultsCard.scrollIntoView({ behavior: "smooth", block: "start" });
      showToast("Elaborazione OCR completata con successo!", "success");

    } catch (err) {
      console.error("Errore OCR:", err);
      showToast(`Errore: ${err.message}`, "error");
    } finally {
      submitOcrBtn.disabled = false;
      btnTextContent.style.display = "inline-flex";
      btnSpinner.style.display = "none";
    }
  });

  // =========================================================================
  // 5. Azioni Risultati (Copia, Scarica TXT, Pulisci)
  // =========================================================================
  
  // Copia negli appunti con feedback visivo
  copyBtn.addEventListener("click", async () => {
    const text = ocrOutput.value;
    if (!text.trim()) {
      showToast("Nessun testo da copiare.", "error");
      return;
    }

    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        // Fallback per contesti HTTP non sicuri
        ocrOutput.select();
        document.execCommand("copy");
      }

      // Feedback visivo sul pulsante
      const originalText = copyBtn.querySelector("span").textContent;
      copyBtn.classList.add("copied");
      copyBtn.querySelector("span").textContent = "Copiato! ✓";
      showToast("Testo copiato negli appunti!", "success");

      setTimeout(() => {
        copyBtn.classList.remove("copied");
        copyBtn.querySelector("span").textContent = originalText;
      }, 2500);

    } catch (err) {
      console.error("Errore copia appunti:", err);
      showToast("Impossibile copiare negli appunti automaticamente.", "error");
    }
  });

  // Download come file .txt
  downloadBtn.addEventListener("click", () => {
    const text = ocrOutput.value;
    if (!text.trim()) {
      showToast("Nessun testo da scaricare.", "error");
      return;
    }

    const baseName = currentFile ? currentFile.name.replace(/\.[^/.]+$/, "") : "estrazione_ocr";
    const filename = `${baseName}_ocr.txt`;
    const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`File "${filename}" scaricato!`, "success");
  });

  // Reset completo
  clearBtn.addEventListener("click", () => {
    ocrOutput.value = "";
    resultsCard.style.display = "none";
    resetUpload();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

});
