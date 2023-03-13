function expand(id) {
  var x = document.getElementById(id);
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
function expand_poll() {
  var x = document.getElementById("poll_options");
  var y = document.getElementById("boolean");

  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }

  if (y.value === "false") {
    y.value = "true";
  } else {
    y.value = "false";
  }
}
