document.addEventListener("DOMContentLoaded", () => {
  const loader = document.getElementById("loader");
  const imageDropzone = document.getElementById("image-dropzone");
  const imageUpload = document.getElementById("image-upload");
  const imagePreview = document.getElementById("image-preview");
  const generateTextBtn = document.getElementById("generate-text-btn");
  const extractedText = document.getElementById("extracted-text");

  const markdownDropzone = document.getElementById("markdown-dropzone");
  const markdownUpload = document.getElementById("markdown-upload");
  const theoremText = document.getElementById("theorem-text");
  const generateProofBtn = document.getElementById("generate-proof-btn");
  const structuredProof = document.getElementById("structured-proof");

  let selectedImages = [];

  // Utility to show loader
  function showLoader() {
    loader.style.display = "flex";
  }

  // Utility to hide loader
  function hideLoader() {
    loader.style.display = "none";
  }

  // Copy to clipboard
  function setupCopyButtons() {
    document.querySelectorAll(".copy-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-clipboard-target");
        const textArea = document.querySelector(targetId);

        navigator.clipboard.writeText(textArea.value).then(() => {
          // Temporary success indicator
          btn.innerHTML = `
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="green" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 6 9 17l-5-5"/>
                        </svg>
                    `;

          setTimeout(() => {
            btn.innerHTML = `
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <rect x="8" y="2" width="8" height="4" rx="1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        `;
          }, 1500);
        });
      });
    });
  }

  // Dynamic textarea height
  function adjustTextareaHeight(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
    textarea.style.overflowY = textarea.scrollHeight > 400 ? "auto" : "hidden";
  }

  // Image Upload Handler
  function handleImageUpload(event) {
    const files = event.target.files;

    Array.from(files).forEach((file) => {
      if (file.type.startsWith("image/")) {
        const reader = new FileReader();

        reader.onload = (e) => {
          // Create wrapper for each image
          const wrapper = document.createElement("div");
          wrapper.className = "image-preview-item";
          wrapper.draggable = true;

          // Create image element
          const img = document.createElement("img");
          img.src = e.target.result;
          img.dataset.filename = file.name;

          // Create remove button
          const removeBtn = document.createElement("button");
          removeBtn.textContent = "✕";
          removeBtn.className = "remove-image";
          removeBtn.addEventListener("click", () => {
            wrapper.remove();
            selectedImages = selectedImages.filter((f) => f.name !== file.name);
          });

          // Drag and drop functionality
          wrapper.addEventListener("dragstart", (e) => {
            e.dataTransfer.setData("text/plain", wrapper.innerHTML);
            e.target.style.opacity = "0.5";
          });

          wrapper.addEventListener("dragend", (e) => {
            e.target.style.opacity = "1";
          });

          wrapper.addEventListener("dragover", (e) => {
            e.preventDefault();
          });

          wrapper.addEventListener("drop", (e) => {
            e.preventDefault();
            const data = e.dataTransfer.getData("text/plain");
            if (data) {
              const draggedElement = document.createElement("div");
              draggedElement.innerHTML = data;
              e.target.parentNode.insertBefore(draggedElement, e.target);
            }
          });

          // Append elements
          wrapper.appendChild(img);
          wrapper.appendChild(removeBtn);
          imagePreview.appendChild(wrapper);

          // Store file
          selectedImages.push(file);
        };

        reader.readAsDataURL(file);
      }
    });

    // Reset file input
    event.target.value = "";
  }

  // Markdown Upload
  function handleMarkdownUpload(event) {
    const file = event.target.files[0];

    if (file && file.name.endsWith(".md")) {
      const reader = new FileReader();
      reader.onload = (e) => {
        theoremText.value = e.target.result;
        adjustTextareaHeight(theoremText);
      };
      reader.readAsText(file);
    } else {
      alert("Please upload a valid markdown file");
    }
  }

  // Generate Image to Text
  async function generateImageText() {
    if (selectedImages.length === 0) {
      alert("Please upload images first");
      return;
    }

    showLoader();
    const formData = new FormData();
    selectedImages.forEach((file) => formData.append("images", file));

    try {
      const response = await fetch("/upload-images", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      extractedText.value = data.extracted_text;
      adjustTextareaHeight(extractedText);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to generate text from images");
    } finally {
      hideLoader();
    }
  }

  // Generate Structured Proof
  async function generateStructuredProof() {
    const proof = extractedText.value;
    const theorem = theoremText.value;

    if (!proof || !theorem) {
      alert("Please generate image text and upload theorem first");
      return;
    }

    showLoader();

    try {
      const response = await fetch("/generate-structured-proof", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ proof, theorem }),
      });
      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      structuredProof.value = data.structured_proof;
      adjustTextareaHeight(structuredProof);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to generate structured proof");
    } finally {
      hideLoader();
    }
  }

  // Event Listeners
  imageDropzone.addEventListener("click", () => imageUpload.click());
  imageUpload.addEventListener("change", handleImageUpload);

  markdownDropzone.addEventListener("click", () => markdownUpload.click());
  markdownUpload.addEventListener("change", handleMarkdownUpload);

  generateTextBtn.addEventListener("click", generateImageText);
  generateProofBtn.addEventListener("click", generateStructuredProof);

  // Initial setup
  setupCopyButtons();

  // Textarea height listeners
  [extractedText, theoremText, structuredProof].forEach((textarea) => {
    textarea.addEventListener("input", () => adjustTextareaHeight(textarea));
  });
});
