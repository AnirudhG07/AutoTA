let uploadedFiles = []; // Store uploaded files' metadata

Dropzone.options.imageDropzone = {
  paramName: "images[]",
  maxFilesize: 5, // MB
  acceptedFiles: "image/*",
  init: function () {
    this.on("success", function (file, response) {
      const uploadedImages = document.getElementById("uploadedImages");
      const listItem = document.createElement("li");
      listItem.textContent = file.name;
      listItem.dataset.file = response.files[file.name];
      uploadedImages.appendChild(listItem);
      uploadedFiles.push(response.files[file.name]);
    });
  },
};

const uploadedImages = document.getElementById("uploadedImages");
new Sortable(uploadedImages, {
  animation: 150,
  ghostClass: "sortable-ghost",
});

document.getElementById("copyButton").addEventListener("click", function () {
  const outputText = document.getElementById("outputText").textContent;
  navigator.clipboard
    .writeText(outputText)
    .then(() => alert("Copied to clipboard!"))
    .catch((error) => console.error("Copy failed:", error));
});

document
  .getElementById("generateButton")
  .addEventListener("click", function () {
    const orderedFiles = Array.from(uploadedImages.children).map(
      (li) => li.dataset.file,
    );

    if (!orderedFiles.length) {
      alert("No images uploaded!");
      return;
    }

    document.getElementById("loadingSpinner").style.display = "block";

    fetch("/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ files: orderedFiles }),
    })
      .then((response) => response.json())
      .then((data) => {
        const outputDiv = document.getElementById("outputText");
        outputDiv.textContent = data.output || "No text generated.";
        document.getElementById("loadingSpinner").style.display = "none";
      })
      .catch((error) => {
        console.error("Error generating text:", error);
        document.getElementById("loadingSpinner").style.display = "none";
      });
  });
