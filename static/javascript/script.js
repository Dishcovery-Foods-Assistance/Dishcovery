const mealList = document.getElementById("mealList");
const modalContainer = document.getElementById("modalContainer");
const mealDetailsContent = document.querySelector(".meal-details-content");
const recipeCloseBtn = document.getElementById("recipeCloseBtn");

// event listeners

function getMealList() {
  var ajax = $.ajax({
    url: "/search/",
    type: "GET",
    success: function (response) {
      if (response.message == "success") {
        var meals = response.meals;
        for (var i = 0; i < meals.length; i++) {
          meals += "<tr>";
          meals += "<td>" + meals[i].meal_img + "</td>";
          meals += "<td>" + meals[i].meal_name + "</td>";
          meals += "</tr>";
        }
      }
    },
  });
}
