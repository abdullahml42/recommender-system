document.addEventListener("DOMContentLoaded", function () {

    // Get references to various elements in the HTML document
    const recommendButton = document.getElementById("recommend-button");
    const reviewerIdInput = document.getElementById("reviewer-id");
    const numItemsInput = document.getElementById("num-items");
    const recommendationsContainer = document.getElementById("recommendations-container");
    const recommendationsTable = document.getElementById("recommendations-table");
    const userIdSuggestions = document.getElementById("user-id-suggestions");
    let errorMessageElement = null;

    // Function to display user ID suggestions
    function displayUserIdSuggestions(suggestions) {
        // Clear the existing suggestions
        userIdSuggestions.innerHTML = "";

        // Generate HTML elements for each suggestion
        suggestions.forEach(suggestion => {
            const suggestionElement = document.createElement("div");
            suggestionElement.classList.add("suggestion");
            suggestionElement.textContent = suggestion;

            // Add a click event listener to populate the input field with the suggestion
            suggestionElement.addEventListener("click", function () {
                reviewerIdInput.value = suggestion;
                userIdSuggestions.innerHTML = "";
            });

            // Add the suggestion element to the suggestions container
            userIdSuggestions.appendChild(suggestionElement);
        });
    }

    // Event listener for user ID input
    reviewerIdInput.addEventListener("input", function () {
        const input = reviewerIdInput.value;

        // Check if the input is not empty
        if (input.trim() !== "") {
            // Simulated AJAX call to fetch user ID suggestions
            const suggestions = [
                "A0096681Y127OL1H8W3U",
                "AKX9EQ37PAYMY",
                "A2ZRAUZCUHW66X"
            ];
            displayUserIdSuggestions(suggestions);
        } else {
            // Clear the suggestions container if the input is empty
            userIdSuggestions.innerHTML = "";
        }
        resetRecommendations();
    });

    // Function to reset the recommendations
    function resetRecommendations() {
        // Hide the recommendations table and clear its rows
        recommendationsTable.style.display = "none";
        while (recommendationsTable.rows.length > 1) {
            recommendationsTable.deleteRow(1);
        }

        // Remove any error message if present
        if (errorMessageElement) {
            recommendationsContainer.removeChild(errorMessageElement);
            errorMessageElement = null;
        }
    }

    // Event listener for the recommend button
    recommendButton.addEventListener("click", function () {
        const reviewerId = reviewerIdInput.value;
        const numItems = numItemsInput.value;

        // Check if both the reviewer ID and number of items are not empty
        if (reviewerId.trim() !== "" && numItems.trim() !== "") {
            resetRecommendations();

            // Make a POST request to fetch recommendations from the server
            fetch("/recommend", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    reviewerId: reviewerId,
                    numItems: numItems
                })
            })
                .then(response => {
                    // Check if the response is successful
                    if (!response.ok) {
                        throw new Error("Request failed. Please try again.");
                    }
                    return response.json();
                })
                .then(data => {
                    // Process the recommendations received from the server
                    if (data.recommendations.length > 0) {
                        data.recommendations.forEach(recommendation => {
                            // Create a new row in the recommendations table
                            const row = recommendationsTable.insertRow();
                            const cell1 = row.insertCell();
                            const cell2 = row.insertCell();

                            // Set the values in the cells
                            cell1.textContent = recommendation.recommendedProductID;
                            cell2.textContent = recommendation.predictedRating;
                        });
                        recommendationsTable.style.display = "table";
                    } else {
                        // Display a message if no recommendations are found
                        const row = recommendationsTable.insertRow();
                        const cell = row.insertCell();
                        cell.colSpan = 2;
                        cell.textContent = "No recommendations found.";
                    }
                    recommendationsContainer.style.display = "block";
                })
                .catch(error => {
                    // Handle any errors that occur during the request
                    console.error("Error:", error);
                    errorMessageElement = document.createElement("p");
                    errorMessageElement.textContent = "An error occurred. Please try again.";
                    recommendationsContainer.appendChild(errorMessageElement);
                    recommendationsContainer.style.display = "block";
                });
        }
    });
});