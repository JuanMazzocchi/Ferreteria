 

// FUNCIONES DEL CARRITO

const btnsConfirm = document.querySelectorAll("#btnBorrar")

if (btnsConfirm.length){
    for(const btn of btnsConfirm){
       btn.addEventListener("click", Event => {
           console.log(Event)
         const resp= confirm("Esta opcion no tiene marcha atras. Confirma?")
           if (!resp) {
               Event.preventDefault()
           }
       }) 
    }
    
};
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 1000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer)
      toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
  })

const modBoot = document.getElementById('btn-toggle');
const modBoot2 = document.getElementById('btn-toggle2');
modBoot?.addEventListener('click', carroBoot);
modBoot2?.addEventListener('click', carroBoot);
    


const modalcontent = document.getElementById('modalBootstrap');



const botonAñadirProducto = document.querySelectorAll('.btnAñadirAlCarrito');
botonAñadirProducto.forEach(addTocartbutton => {
    addTocartbutton.addEventListener('click', addToCartBtnClicked);
    });
const contenedorCarrito = document.getElementById('modalCarrito');

const btnVaciarCarro = document.getElementById('vaciarCarrito');
btnVaciarCarro?.addEventListener('click', btnVaciarClicked)


const downloadListener = document.getElementById('downloadBtn');
downloadListener?.addEventListener('click', downloadClicked );
const downloadListenerCel = document.getElementById('downloadBtnCel');
downloadListenerCel?.addEventListener('click', downloadClicked );

const downloadPedidoListener = document.getElementById('downloadPedidoBtn');
downloadPedidoListener?.addEventListener('click', downloadPedidoClicked );
const downloadPedidoListenerCel = document.getElementById('downloadPedidoBtnCel');
downloadPedidoListenerCel?.addEventListener('click', downloadPedidoClicked );
// const titulos=` <div class="row  titulares">
// <div class="col-2 p-0">
//   <p class="p-0 m-0 text-center">Codigo</p>
// </div>
// <div class="col-5 p-0"  >
//   <p class="p-0 m-0 text-center">Descripcion</p>
// </div>
// <div class="col-1 m-0 p-0">
//   <p class="p-0">Precio</p>
// </div>
// <div class="col-2 p-0">
//   <p class="p-0 m-0 text-center">Cant.</p>
// </div>
// <div class="col-1 p-0">
//   <p class="p-0 m-0">Quitar</p>
// </div>
// <div class="col-1   ">
//   <p class="p-0 m-0">SubTotal Producto</p>
// </div>
// </div>`;

const titulos=` <div class="row  titulares">
<div class="col-2 p-0">
  <p class="p-0 m-0 text-center"><b>Código</b></p>
</div>
<div class="col-2 p-0">
  <p class="p-0 m-0 text-center"><b>Cantidad</b></p>
</div>
<div class="col-6 p-0"  >
  <p class="p-0 m-0 text-center"><b>Descripción</b></p>
</div>
</div>`;

const btnPedido=document.getElementById('btnEnviarPedido');
if(btnPedido){btnPedido.addEventListener('click', btnPedidoClicked);}

const btnVolver=document.getElementById('btnVolver');
if(btnVolver){btnVolver.addEventListener('click', btnVolverClicked);}

// const btnSeleccion=document.querySelectorAll('.seleccion');
// btnSeleccion.forEach(seleccion =>{
//     seleccion.addEventListener('click',cantidadDefault
//     )
// });


function carroBoot(){

    let productosEnElCarro;
    productosEnElCarro =obtenerProductosLS();
    if(productosEnElCarro.length===0){
        modalcontent.innerHTML=`
        <div class="row justify-content-center" id="modalBootstrap">
        <h1>El Carro Esta Vacio</h1>
        </div>`;
        let btnEnviar=document.getElementById('btnEnviarPedido')
        btnEnviar?.setAttribute('disabled','')
    }
    else{
      let btnEnviar=document.getElementById('btnEnviarPedido')
      btnEnviar?.removeAttribute('disabled');
      modalcontent.innerHTML="";
      modalcontent.innerHTML=titulos;
      productosEnElCarro.forEach(arregladora);
      const borrarProductoCarro = document.querySelectorAll('.btnBorrarProducto');
      borrarProductoCarro.forEach(borroProducto => {
      borroProducto.addEventListener('click', borrarProductoCarroClicked);
      });

    // const restarCantidadCarro = document.querySelectorAll('.restaCantidad');
    // restarCantidadCarro.forEach(restarProducto =>{
    //     restarProducto.addEventListener('click', btnRestarCantidadClicked)
    // });
    // const sumarCantidadCarro = document.querySelectorAll('.sumaCantidad');
    // sumarCantidadCarro.forEach(sumarProducto=>{
    //     sumarProducto.addEventListener('click', btnSumarCantidadClicked);
    // });
    $(".cantidadInput").on('keyup', function (e) {      //Enter sirve para lanzar la funcion, ademas del OK
      if (e.key === 'Enter' || e.keyCode === 13) {
        // console.log("first")                       
        btnmodificarCarrito(e)
      }
    });
    totalCarro();}
    cantidadDefault();
};

function addToCartBtnClicked(event){
    const boton = event.target;
    const item = boton.closest('.item');

    const itemCodigo = item.querySelector('.item-codigo').textContent;
    const itemImage = item.querySelector('.item-image').src;
    const itemDescripcion = item.querySelector('.item-descripcionProducto').textContent;
    const itemPrecio= item.querySelector(".item-precioProducto").textContent;
    const itemUnidad = item.querySelector('.item-unidadDeVenta').textContent;
    let itemCantidad =item.querySelector('.cantidadDefault').value;
    // console.log(typeof(itemCantidad))
    itemCantidad = Number(itemCantidad)
    // console.log(itemCantidad)
    if(itemCantidad>0){
      infoProducto ={id:itemCodigo,imagen:itemImage,descripcion:itemDescripcion,precio:itemPrecio,unidad:itemUnidad,cantidad:itemCantidad};
      // infoProducto ={id:itemCodigo,descripcion:itemDescripcion,precio:itemPrecio,unidad:itemUnidad,cantidad:itemCantidad};
      // console.log(infoProducto)
      
      addToCarrito(infoProducto);
      boton.blur();
    }
};

function addToCarrito(infoProducto){
    let productosEnStorage;
    productosEnStorage=obtenerProductosLS();
    let indice=0; 
    
    if (productosEnStorage.length!=0){
        for(let i=0;i<productosEnStorage.length;i++){
                        
            if (productosEnStorage[i].id === infoProducto.id){
                indice = productosEnStorage[i];
                // console.log('igualdad de id entre : '+ productosEnStorage[i].id +" y "+infoProducto.id)
            }else{
                // console.log('desigual ' + productosEnStorage[i].id)
                continue
            }
        };
       if (indice!=0){
        
        let cantidadnueva=String(infoProducto.cantidad)
        indice.cantidad=cantidadnueva;
        // console.log('envio a guardar producto con cantidad modificada');
        guardarEnLS(indice);
        }else{
        // console.log('envio a guardar producto nuevo');
        guardarEnLS(infoProducto);
       }

    }
    else{
       // console.log("guardo default");  // solo si no hay nada cargado
        guardarEnLS(infoProducto);
    };
    Toast.fire({
        icon: 'success',
        title: 'Producto añadido al Carro'
      })
    cantidadDefault(); 
};


function arregladora(item){
    const filaCarrito= document.createElement('div');
    filaCarrito.classList.add('contenedorArticulos')
    // const contenidoCarrito= `<div class="row articulos p-0 listado contenedor m-0" >
    // <div class="col-2 art ">
    //   <p  class="item-codigo text-center ">${item.id}</p>
    // </div>
    // <div class="col-5 art px-1   p-0 "  >
    //   <p class="item-descripcionProducto  ">${item.descripcion}</p>
    // </div>
    // <div class="col-1 art mw-100   p-0 ">
    //   <p class="item-precioProducto p-0 m-0"> ${item.precio}</p>
    // </div>
    
    // <div class="col-2 art mw-100   p-0 text-center">
    // <input class="cantidadInput mw-50 p-0 m-0 " type="number" value=${item.cantidad} min="0" style="width: 50px;" ><button class="btn btn-success OKbtn" onclick="btnmodificarCarrito(event)" title="Modificar"><i class="bi bi-check"></i></button> 
    // </div>
    // <div class="col-1 art mw-100 m-0  p-0 ">
    // <button class="btn btn-danger btnBorrarProducto m-0" title="Quitar del Carro">X</button>
    // </div>
    // <div class="col-1 art mw-100  m-0  ">
    //   <p class="item-SubtotalProducto  subTotalCol ">$ ${(item.precio * item.cantidad).toFixed(2)}</p>
    // </div>
    // </div> `;

    const contenidoCarrito= `<div class="row articulos p-0 listado contenedor m-0 border border-dark" > 
    <div class='row gx-1' >
      <div class="col-2 art  ">
        <p  class="item-codigo text-center ">${item.id}</p>
      </div>
      <div class="col-2 art mw-100   p-0 text-center ">
      <p>
        <input class="cantidadInput mw-50 p-0 m-0  " type="number" value=${item.cantidad} min="0" style="width: 50px;" >
          <button class="btn btn-success OKbtn my-1" onclick="btnmodificarCarrito(event)" title="Modificar">
            <i class="bi bi-check"></i>
          </button> 
      </p>
      </div>
      <div class="col-7 art px-1   p-0  text-center "  >
        <p class="item-descripcionProducto  ">${item.descripcion}</p>
      </div>
       <div class="col-1 art mw-100 m-0  p-0 text-center">
      <button class="btn btn-danger btnBorrarProducto my-1" title="Quitar del Carro">X</button>
      </div> 
    </div>
    
    </div> `;
     
    filaCarrito.innerHTML=contenidoCarrito;
    modalcontent.append(filaCarrito);
 };


function guardarEnLS(productoAlStorage){
   
    let productos;
    productos =this.obtenerProductosLS();
    
    let cambiocantidad = false

    for (let i =0; i < productos.length; i++){
        if (productos[i].id === productoAlStorage.id){
            productos.splice([i], 1);
            productos.push(productoAlStorage);
            localStorage.setItem('productos', JSON.stringify(productos));
            // console.log('cambio cantidad y finalizo guardado en LS');
            cambiocantidad = true
            break
        };
    };
    if (cambiocantidad===false){
        productos.push(productoAlStorage);
        localStorage.setItem('productos', JSON.stringify(productos))
        // console.log('guardado producto nuevo en LS') ;
    };
    if (productos.length===0) { 
        // console.log('default')
        productos.push(productoAlStorage);
        localStorage.setItem('productos', JSON.stringify(productos));
    };
};


function obtenerProductosLS(){
    let productoLS;
      if(localStorage.getItem('productos')=== null){
            productoLS = [];
        }
        else {
            productoLS = JSON.parse(localStorage.getItem('productos'));
        };
        return productoLS
};


function btnVaciarClicked(){
    localStorage.clear();
    totalCarro();
    modalcontent.innerHTML="";
    modalcontent.innerHTML=`
    <div class="row justify-content-center" id="modalBootstrap">
    <h1>El Carro Esta Vacio</h1>
    </div>`;
    
};

// function btnRestarCantidadClicked(event){
//     let btn = event.target;
//     let prodAModificar = btn.closest('.contenedor');
//     let itemCodigo= prodAModificar.querySelector('.item-codigo').textContent;
//     let itemCantidad =prodAModificar.querySelector('.cantidadInput').value;
//     let productoModificado;
//     let productos;
//     productos =obtenerProductosLS();

//     for (let i = 0; i < productos.length; i++) {
//         if (productos[i].id===itemCodigo){

//             if(productos[i].cantidad===1){
//                 continue
//             }else{
//             productoModificado=productos[i];
//             productoModificado.cantidad=itemCantidad-1;
//             productos.splice([i],1,productoModificado); 
//             localStorage.setItem('productos', JSON.stringify(productos));
//             carroBoot();
//             totalCarro();
            
//             };
//         };
//     };
// };
function btnmodificarCarrito(event){
    let btn=event.target;
    let prodAModificar = btn.closest('.contenedor');
    let itemCodigo= prodAModificar.querySelector('.item-codigo').textContent;
    let itemCantidad =prodAModificar.querySelector('.cantidadInput').value;
    let productoModificado;
    let productos;
    productos =obtenerProductosLS();
   
    for (let i = 0; i <productos.length; i++) {
       if(productos[i].id===itemCodigo){
       
        productoModificado=productos[i];
        productoModificado.cantidad=itemCantidad;
        if(itemCantidad==0){
          productos.splice([i],1) //si la cantidad es 0 quito el producto del carro automaticamente
          localStorage.setItem('productos', JSON.stringify(productos));
          carroBoot();
          totalCarro();
        }else{
          productos.splice([i],1,productoModificado);//quita el array viejo y en su lugar pone el nuevo
          localStorage.setItem('productos', JSON.stringify(productos));
          carroBoot();
          totalCarro();
        };
       };
    };
};

// function btnSumarCantidadClicked(event){
//     let btn = event.target;
//     let prodAModificar = btn.closest('.contenedor');
//     let itemCodigo= prodAModificar.querySelector('.item-codigo').textContent;
//     let itemCantidad =parseInt( prodAModificar.querySelector('.cantidadInput').value);
//     let productoModificado;
//     let productos;
//     productos =obtenerProductosLS();

//     for (let i = 0; i < productos.length; i++) {
//         if (productos[i].id===itemCodigo){
            
//             productoModificado=productos[i];
//             productoModificado.cantidad=itemCantidad+1;
//             productos.splice([i],1,productoModificado); //quita el array viejo y en su lugar pone el nuevo
//             localStorage.setItem('productos', JSON.stringify(productos));
//             carroBoot();
//             totalCarro();
            
//             };
//         };
// };

function borrarProductoCarroClicked(event){
    let btn = event.target;
    let prodABorrar = btn.closest('.contenedor');
    let itemCodigo= prodABorrar.querySelector('.item-codigo').textContent;
    let productos;
    productos =obtenerProductosLS();
    for(let i =0; i < productos.length; i++){
        if(productos[i].id===itemCodigo){
            // console.log('producto '+productos[i].id+' borrandose' );
            productos.splice([i], 1);
            localStorage.setItem('productos', JSON.stringify(productos));
           // console.log("borrado");
            carroBoot();
            totalCarro();
            
        };
    };
};


function totalCarro(){
    let productos;
    productos =obtenerProductosLS();
    let total=0;
    let totalDiv = document.getElementById('totalCarro');
    if(totalDiv){
      for (let i = 0; i < productos.length; i++) {
          // console.log(productos[i].precio*productos[i].cantidad);
          total=total+(parseFloat(productos[i].precio)*parseFloat(productos[i].cantidad));
      };
      let totalnumero =  `<p>Total Pedido: $ ${total.toFixed(2)} </p>`;
      totalDiv.innerHTML=totalnumero;
     }
  };


function generarCookie(){   //genera una cookie con el pedido obtenido desde el localStorage

  let productos =obtenerProductosLS();
  let listaCarro=[]
    productos.forEach(element => {
      listaCarro.push("Cod: "+element.id +"---"+"Cantidad: "+ element.cantidad +"---"+ element.descripcion)
    });
    document.cookie= `carrito= ${listaCarro}; path=/`  
};
 

function cantidadDefault(){
    var myElement=document.querySelectorAll('.cantidadDefault');
    if(myElement.length!=0){
        let productos;
        productos =obtenerProductosLS();
        let codigos=document.querySelectorAll('.item-codigo');
        myElement.forEach(element=>{
            element.value=0
        });
      // codigos.forEach(element=>{console.log("supuesto codigo en pantalla"+element.textContent)})
        productos.forEach(element => {
            for (let i = 0; i < codigos.length; i++) {
               if(element.id===codigos[i].textContent){
                // console.log(element)
                // console.log("codigo en pantalla "+codigos[i].textContent+ " codigo producto "+ element.id)
                // console.log(typeof(codigos[i].textContent))
                // console.log(typeof(element.id))
              //  let cantidadEnPantalla=document.getElementById(element.id)
              //  cantidadEnPantalla.value=element.cantidad
                  if(document.getElementById(element.id)){
                    document.getElementById(element.id).value=element.cantidad;
                  }

                }else{
                    continue    
                };

            }
        });
    };
  };  

document.addEventListener("DOMContentLoaded",cantidadDefault()) //ejecuta la funcion cuando la pagina se carga

$(document).ready(function(){       //funcion del boton ir arriba
  $(window).scroll(function(){ 
      if ($(this).scrollTop() > 100) { 
          $('#scroll').fadeIn(); 
      } else { 
          $('#scroll').fadeOut(); 
      } 
  }); 
  $('#scroll').click(function(){ 
      $("html, body").animate({ scrollTop: 0 }, 300); 
      return false; 
  }); 
});



//  INDEX.HTML
function volver(){
    var contenedor=document.getElementById("container");
    contenedor.style.display = 'block';
    document.getElementById("volver").style.display = 'none';
    document.getElementById("cuadro").innerHTML="";
};

 

var pedidoTotal=document.getElementById('terminarPedido');

function btnPedidoClicked(){
    // let productos;
    // productos =obtenerProductosLS();
    // productos.forEach(acomodadorDePedido);
    pedidoTotal.style.display="block";
    const buttons = document.querySelectorAll('.btnBorrarProducto');

    for (const button of buttons) {
      // ✅ Set the disabled attribute
      button.setAttribute('disabled', '');
    }
    const oks =document.querySelectorAll('.OKbtn');

    for (const button of oks) {
      // ✅ Set the disabled attribute
      button.setAttribute('disabled', '');
    }

    const cantidades=document.getElementsByClassName('cantidadInput');
    for (const button of cantidades) {
      // ✅ Set the disabled attribute
      button.setAttribute('readonly', '');

    } 
    document.getElementById('botonesEnviar').style.display="none";
    // document.getElementById('totalCarro').style.display="none"
};

function btnVolverClicked(){
    pedidoTotal.style.display="none";
    document.getElementById('botonesEnviar').style.display="flex";

    const buttons = document.querySelectorAll('.btnBorrarProducto');

    for (const button of buttons) {
      // ✅ Remove the disabled attribute
      button.removeAttribute('disabled');
    }
    const oks =document.querySelectorAll('.OKbtn');

    for (const button of oks) {
      // ✅ Remove the disabled attribute
      button.removeAttribute('disabled');
    }

    const cantidades=document.getElementsByClassName('cantidadInput');
    for (const button of cantidades) {
      // ✅ Remove the disabled attribute
      button.removeAttribute('disabled');
    } 


};


const enviarFinal=document.getElementById('enviarFinal');
enviarFinal?.addEventListener('click',cerrarYborrar)

function cerrarYborrar(){
  Swal.fire({
    title: 'Su nota de pedido ha sido enviada',
    showDenyButton: false,
    showCancelButton: false,
    confirmButtonText: 'OK',
    timer:2000,
     
  }).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
      btnVaciarClicked()
    } else if (result.isDenied) {
      btnVaciarClicked()
    }
  })
  btnVaciarClicked()
  
};


function acomodadorDePedido(item){
    
    const divPedido=document.createElement('div');              //NO ESTA EN USO
    let itemPedido;
      
    itemPedido=`<div> Codigo: ${item.id} Producto: ${item.descripcion} Cantidad: ${item.cantidad} SubTotal: ${(item.precio * item.cantidad).toFixed(2)}</div> `;
    divPedido.innerHTML=itemPedido
    pedidoTotal.append(divPedido)
};


function modal(event){
    // console.log("first")
    let id=event.currentTarget.getAttribute("id")
    
    let descripcion=event.currentTarget.getAttribute("name")
     
    let modal=document.getElementById("imagenModal2")
     
    modal.setAttribute("src", "/media/img/"+id+".jpg")
    
    let titulo=document.getElementById('exampleModalLongTitle')
    
    titulo.innerHTML=descripcion
    let modalTodo=document.getElementById("modal2")

    
    $('#modal2').modal('toggle')
    cantidadDefault();
  };

function closeModal(){
     
    $('#modal2').modal('toggle')
    cantidadDefault();
  };


// boton de descargar lista de precios 

function downloadClicked() {
  console.log("first")
    Toast.fire( {
        title: 'Desea descargar la lista de precios a su dispositivo?',
        showConfirmButton: true,
        timer:false,
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: 'Descargar',
        denyButtonText: `Cancelar`,
      }).then((result) => {
        
        if (result.isConfirmed) {
          Swal.fire('La lista de precios a sido enviada a su dispositivo', '', 'success'),
          location.href ="/downloadLista";
        } else if (result.isDenied) {
        //   Swal.fire('Changes are not saved', '', 'info')
        }
      })
    
}

// boton de descargar el archivo de pedido por mail
function downloadPedidoClicked() {
    Toast.fire( {
        title: 'Desea descargar el archivo de pedido a su dispositivo?',
        showConfirmButton: true,
        timer:false,
        showDenyButton: true,
        showCancelButton: false,
        confirmButtonText: 'Descargar',
        denyButtonText: `Cancelar`,
      }).then((result) => {
        
        if (result.isConfirmed) {
          Swal.fire('El archivo de Pedidos a sido enviado a su dispositivo', '', 'success'),
          location.href ="/downloadPedidoPorMail";
        } else if (result.isDenied) {
        //   Swal.fire('Changes are not saved', '', 'info')
        }
      })
    
}

// Boton de sobreescribir la base de datos
const btnSobreescribir=document.getElementById('sobreescribirBase')
if(btnSobreescribir){
  btnSobreescribir.addEventListener('click', btnSobreescribirClicked)}

function btnSobreescribirClicked(){
   
  Swal.fire({
    title: 'Desea sobreescribir la base de datos? ',
    showDenyButton: true,
    showCancelButton: false,
    confirmButtonText: 'Sobreescribir',
    denyButtonText: `Cancelar`,
  }).then((result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
      Swal.fire('Este proceso puede tardar', 'no clickee nuevamente!', 'success'),
      location.href ="/borrarLlenar";
    } else if (result.isDenied) {
      Swal.fire('Cancelado', '', 'info')
    }
  })
};


$(".cantidadDefault").on('keyup', function (e) {       // cuando se presiona ENTER en el input de cantidad ejecuta la funcion 
  if (e.key === 'Enter' || e.keyCode === 13) {
    // console.log("otro")
    addToCartBtnClicked(e)
  }
});

$(".cantidadDefault").on('click',function(e){
  // console.log(e.target.id)
 let x=document.getElementById(e.target.id)     //desaparece el 0 al hacer click en el imput de cantidad y lo reinserta si no se añade el producto
 if(x.value==0){
  x.value=""
 }
 x.addEventListener('focusout',()=>{
  if(x.value==""){
    x.value=0
  }
  })
  
})

 
 


$(document).ready(function(){
	var estado = false;             //slide del carrito

	$('#btn-toggle').on('click',function(){
		$('.seccionToggle').slideToggle();

		if (estado == true) {
			// $(this).text("Abrir");
			$('body').css({
				"overflow": "auto"
			});
			estado = false;
		} else {
			// $(this).text("Cerrar");
			$('body').css({
				"overflow": "hidden"
			});
			estado = true;
		}
	});
  $('#btn-toggle2').on('click',function(){
		$('.seccionToggle').slideToggle();

		if (estado == true) {
			// $(this).text("Abrir");
			$('body').css({
				"overflow": "auto"
			});
			estado = false;
		} else {
			// $(this).text("Cerrar");
			$('body').css({
				"overflow": "hidden"
			});
			estado = true;
		}
	});
  $('#btn-toggle3').on('click',function(){
		$('.seccionToggle').slideToggle();

		if (estado == true) {
			// $(this).text("Abrir");
			$('body').css({
				"overflow": "auto"
			});
			estado = false;
		} else {
			// $(this).text("Cerrar");
			$('body').css({
				"overflow": "hidden"
			});
			estado = true;
		}
    btnVolverClicked();
	});
});

// Prioridad Lineas

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  // console.log(data);
  ev.target.value= data;
}



totalCarro();
