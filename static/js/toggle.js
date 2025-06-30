// Actualiza el estado de una tarea por si tiene subtareas sin completar, algunas completadas o todas completadas, para que actualice el estado de la tarea según esto
function toggleSubtarea(checkbox) {
  // Se obtiene el estado actual de la subtarea
  fetch(checkbox.dataset.url, {
    method: "POST"
  })
  // Se obtiene el nuevo estado de la subtarea y se transforma a JSON
  .then(response => response.json())
  .then(data => {
  
  // Obtiene el nuevo estado y el índice de la tarea
	const nuevo_estado = data.nuevo_estado;
	const indice = data.indice;

  // Se actualiza el texto del estado de la subtarea en la interfaz
	document.querySelectorAll(".estado-tarea").item(indice).textContent = nuevo_estado.charAt(0).toUpperCase() + nuevo_estado.slice(1);
  })
  .catch(error => {
    console.error("Error toggling subtarea:", error);
  });
}