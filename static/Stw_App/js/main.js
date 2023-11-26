// MARKETPLACE SEARCH BAR
const search = document.querySelector(".search-container");
const searchBox = document.getElementsByClassName("search-box")
let searchPredictions = document.querySelectorAll(".search-predictions");
search.addEventListener("mouseover", () => {
    for (let i = 0; i < searchPredictions.length; i++) {
        searchPredictions[i].style.display = "block";
        searchBox[i].style.borderRadius = "8px 8px 0 0"
        }
});
search.addEventListener("mouseout", () => {
    for (let i = 0; i < searchPredictions.length; i++) {
        searchPredictions[i].style.display = "none";
        searchBox[i].style.borderRadius = "8px"
        }
});