// Se carga en <head> (sin defer) para aplicar el tema guardado antes de pintar y evitar parpadeos.
// Oscuro por defecto; la preferencia del visitante se guarda en localStorage.
(() => {
  try {
    if (localStorage.getItem('theme') === 'light') {
      document.documentElement.dataset.theme = 'light';
    }
  } catch (_) { /* almacenamiento bloqueado: se queda en oscuro */ }
})();
