document.addEventListener('DOMContentLoaded', function() {
    $(document).ready(function() {
        $("form").submit(function(e) {
            // Prevent default form submission
            e.preventDefault();

            // Get height and weight input values
            var height = $("#height").val();
            var weight = $("#weight").val();

            // Calculate BMI
            var bmi = weight / ((height / 100) ** 2);
            // Round BMI to two decimal places
            bmi = parseFloat(bmi.toFixed(2));

            // Determine BMI status
            var status = "";
            if (bmi < 18.5) {
                status = "Underweight";
            } else if (bmi >= 18.5 && bmi < 24.9) {
                status = "Healthy";
            } else if (bmi >= 25 && bmi < 29.9) {
                status = "Overweight";
            } else if (bmi >= 30 && bmi < 34.9) {
                status = "Obese";
            } else if (bmi >= 35) {
                status = "Extremely Obese";
            }

            // Update the status display on the page
            $("#status").text(status);

            var data = {
                height: height,
                weight: weight,
                bmi: bmi,
                status: status
            };

            // Send data to the server
            $.ajax({
                type: "POST",
                url: "/result",
                data: JSON.stringify(data),
                contentType: "application/json",
                dataType: "html",
                success: function(response) {
                    $('#resultContainer').html(response);
                }
            });
        });
    });
});
