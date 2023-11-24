// MARKETPLACE SEARCH BAR
const search = document.querySelector(".search-container");
let searchPredictions = document.querySelectorAll(".search-predictions");
search.addEventListener("mouseover", () => {
    for (let i = 0; i < searchPredictions.length; i++) {
        searchPredictions[i].style.display = "block";
        }
});
search.addEventListener("mouseout", () => {
    for (let i = 0; i < searchPredictions.length; i++) {
        searchPredictions[i].style.display = "none";
        }
});