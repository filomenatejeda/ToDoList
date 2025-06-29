function toggleSubtarea(checkbox) {
  fetch(checkbox.dataset.url, {
    method: "POST"
  }).catch(error => {
    console.error("Error toggling subtarea:", error);
  });
}
