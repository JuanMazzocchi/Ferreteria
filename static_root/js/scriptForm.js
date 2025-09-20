// Creo las variables para cada input del form
const form = document.getElementById('formulario_contacto')
const nombre = document.getElementById('id_nombreContacto')
const email = document.getElementById('id_emailContacto')
const telefono = document.getElementById('id_telefonoContacto')
const comentario = document.getElementById('id_mensajeContacto')

// El event listener para que no se envie el form y agrega ka clase was validated

form.addEventListener('submit', (event) => {

  
  if (!form.checkValidity()) {
      event.preventDefault(); 
      event.stopPropagation();
    }
  
    form.classList.add('was-validated');

});


// En cada input valida si es true (quita los la clase is valid) o false (agrega los la clase is valid)
// Mucho no sirve por que solo esta validando si en el input hay caracteres escritos o no
// Por lo que hay que rehacerlo
nombre.addEventListener('input', () => {
    if (nombre.validity.valid) {
      nombre.classList.remove('is-invalid');
    } else {
      nombre.classList.add('is-invalid');
    }
});

email.addEventListener('input', () => {
    if (email.validity.valid) {
      email.classList.remove('is-invalid');
    } else {
      email.classList.add('is-invalid');
    }
});

telefono.addEventListener('input', () => {
    if (telefono.validity.valid) {
      telefono.classList.remove('is-invalid');
    } else {
      telefono.classList.add('is-invalid');
    }
});

comentario.addEventListener('input', () => {
    if (comentario.validity.valid) {
      comentario.classList.remove('is-invalid');
    } else {
      comentario.classList.add('is-invalid');
    }
});