function toggleSubtarea(checkbox) {
  fetch(checkbox.dataset.url, {
    method: "POST"
  })
  .then(response => response.json())
  .then(data => {
	const nuevo_estado = data.nuevo_estado;
	const indice = data.indice;

	document.querySelectorAll(".estado-tarea").item(indice).textContent = nuevo_estado.charAt(0).toUpperCase() + nuevo_estado.slice(1);
  })
  .catch(error => {
    console.error("Error toggling subtarea:", error);
  });
}