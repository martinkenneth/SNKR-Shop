// $(".size").on("click", function () {
//     console.log("Clicked!");
//     $(this).toggleClass("focus").siblings().removeClass("focus");
// });

// document.getElementById("size").onclick = function () {
//     console.log("Clicked!");
//     document.getElementsByClassName("size").className = "focus";
// };

// document.getElementById("lightmode").onclick = function () {
//     document.getElementById("container").className = "light";
// };

function select(el) {
    // var element = document.getElementById("myDIV");
    console.log("Clicked!");
    var all = document.getElementsByClassName("size");
    console.log(all);
    el.classList.toggle("focus").siblings(".size").removeClass("focus");
    // $(this).toggleClass("focus").siblings().removeClass("focus");
}
