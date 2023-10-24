// require ("static/css/styles.css");

const navigation = document.getElementById("nav");
const backdrop = document.getElementById("backdrop");

const toggleBurger = () => {
  navigation.classList.toggle("nav_open");
  backdrop.classList.toggle("backdrop_open");
}

const disableBurger = () => {
  console.log("disableBurger");
  navigation.classList.remove("nav_open");
  backdrop.classList.remove("backdrop_open");
}

const burgerButton = document.getElementById("burger");
burgerButton.addEventListener("click", toggleBurger);

const closeButton = document.getElementById("btn-close");
closeButton.addEventListener("click", toggleBurger);

backdrop.addEventListener("click", toggleBurger);

window.addEventListener("resize", disableBurger)
