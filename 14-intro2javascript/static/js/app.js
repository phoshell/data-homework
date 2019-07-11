// from data.js
var tableData = data;

// Get a reference to the table body
var tbody = d3.select("tbody");

// 
function buildTable(data) {
    // Use d3 to update each cell's text with
    data.forEach(function(ufoReport) {
        // console.log(ufoReport);
        var row = tbody.append("tr");
        Object.entries(ufoReport).forEach(function([key, value]) {
        //   console.log(key, value);

        // Append a cell to the row for each value
        // in the weather report object
        var cell = row.append("td");

        // Insert data into a table
        cell.text(value);
        });
    });
}

// Selects the submit button
var submit = d3.select("#filter-btn");

// FUNCTION TO FILTER DATA
submit.on("click", function() {
        var row = d3.select("tbody").selectAll("td");
        row.remove();

        // Prevent the page from refreshing
        d3.event.preventDefault();

        // Select the input element and get the raw HTML node
        var inputElement = d3.select("#datetime");
        console.log(inputElement);

        // Get the value property of the input element
        var inputValue = inputElement.property("value");
        console.log(inputValue);

        let filteredData = tableData;

        // checking tbody for input value 
        var filtered = filteredData.filter(tbody => tbody.datetime === inputValue);
        console.log(filtered);

        buildTable(filtered);

});

buildTable(tableData);
