function dC(name) {
    document.getElementById("card-image").src = "https://static.krcg.org/card/".concat(name, ".jpg")
    document.getElementById("card-modal").style.display = "block"
}

function hC(name) {
    if (window.matchMedia("(hover: none)").matches) {
        return
    }
    document.getElementById("card-hover-image").src = "https://static.krcg.org/card/".concat(name, ".jpg")
    document.getElementById("card-hover").style.display = "block"
}

function oC() {
    document.getElementById("card-hover").style.display = "none"
}
