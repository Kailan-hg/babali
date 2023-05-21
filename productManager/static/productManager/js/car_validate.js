  // Asignar botones
  let container_car = document.querySelector('[class="container-car"]');
  let button_print = document.querySelector('[class="button-print"]');

  // Mostar vista del carrito
  function container_car_show() {
    button_print.onclick = container_car_delete;
    container_car.style.display = "flex";
  }

  // Borrar vista del carrito
  function container_car_delete() {
    button_print.onclick = container_car_show;
    container_car.style.display = "none";
  }