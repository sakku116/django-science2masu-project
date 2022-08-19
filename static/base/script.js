function navHamburgerActive() {
  /* change responsive nav active style */
  var nav = document.getElementById("nav");
  var hamburger_line = document.getElementById("hamburgerLine");

  if (!nav.classList.contains("responsive")) {
    nav.classList.add("responsive");
  }
  else {
    nav.classList.remove("responsive")
  };
}