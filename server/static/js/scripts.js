// Dropzone Configuration
Dropzone.options.imageDropzone = {
  paramName: "images[]",
  maxFilesize: 5, // MB
  acceptedFiles: "image/*",
  init: function () {
    this.on("addedfile", function (file) {
      // Add the file to the uploaded images list
      const uploadedImages = document.getElementById("uploadedImages");
      const listItem = document.createElement("li");
      listItem.textContent = file.name;
      listItem.dataset.file = file.upload.uuid; // Store file ID for ordering
      uploadedImages.appendChild(listItem);
    });

    this.on("success", function (file, response) {
      console.log("Response from server:", response); // Debugging: Log the response

      if (response.output) {
        const outputDiv = document.getElementById("outputText");

        // Remove placeholder text if present
        if (outputDiv.textContent === "Processed proofs will appear here...") {
          outputDiv.textContent = "";
        }

        // Append the new proof text to the existing content
        const existingContent = outputDiv.textContent.trim();
        const newContent = response.output.trim();

        outputDiv.textContent = existingContent
          ? existingContent + "\n\n" + newContent
          : newContent;
      } else {
        const outputDiv = document.getElementById("outputText");
        outputDiv.textContent += "\nNo proof generated for one of the uploads.";
      }
    });

    this.on("error", function (file, response) {
      console.error("Error from server:", response);
      const outputDiv = document.getElementById("outputText");
      outputDiv.textContent +=
        "\nAn error occurred while processing one of the uploads.";
    });
  },
};

// Make the Uploaded Images List Sortable
const uploadedImages = document.getElementById("uploadedImages");
new Sortable(uploadedImages, {
  animation: 150,
  ghostClass: "sortable-ghost",
  onEnd: function (evt) {
    console.log("New order:", evt.to); // Debugging: Log the new order
  },
});
