// app.js
$(document).ready(function () {
  // Get cupcakes from API and update the page
  function getCupcakes() {
    axios
      .get("/cupcakes")
      .then(function (response) {
        const cupcakes = response.data.cupcakes;
        const cupcakeList = $("#cupcake-list");
        cupcakeList.empty();
        cupcakes.forEach(function (cupcake) {
          // Add each cupcake to the list as a new list item
          const li = $("<li>").text(
            `Flavor: ${cupcake.flavor}, Size: ${cupcake.size}, Rating: ${cupcake.rating}`
          );
          cupcakeList.append(li);
        });
      })
      .catch(function (error) {
        console.error("Error fetching cupcakes:", error);
      });
  }

  getCupcakes();

  // Handle form submission to add new cupcake
  $("#add-cupcake-form").submit(function (event) {
    event.preventDefault();
    const flavor = $("#flavor").val();
    const size = $("#size").val();
    const rating = $("#rating").val();
    const cupcakeData = {
      flavor: flavor,
      size: size,
      rating: rating,
    };
    axios
      .post("/cupcakes", cupcakeData)
      .then(function (response) {
        // Refresh cupcakes data and reset form fields
        getCupcakes();
        $("#flavor").val("");
        $("#size").val("");
        $("#rating").val("");
      })
      .catch(function (error) {
        console.error("Error adding cupcake:", error);
      });
  });
});
