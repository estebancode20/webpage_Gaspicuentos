// menu.js

const categoryMenu = document.querySelector("#categories");
const categoryList = document.querySelector("#categories ul");

// Mostrar el menú de categorías al hacer hover sobre la categoría
categoryMenu.addEventListener("mouseover", function() {
    categoryList.style.display = "block";
});

// Ocultar el menú de categorías al quitar el cursor
categoryMenu.addEventListener("mouseout", function() {
    categoryList.style.display = "none";
});

// Evitar que el menú se cierre cuando se interactúa con la lista
categoryList.addEventListener("mouseover", function() {
    categoryList.style.display = "block";
});

// Volver a ocultar el menú al quitar el cursor de la lista
categoryList.addEventListener("mouseout", function() {
    categoryList.style.display = "none";
});
