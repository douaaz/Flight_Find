$(document).ready(function () {
    $('form').on('submit', function (event) {
        $.ajax({
            data:{
                year : $('#year').val(),
                start_month : $('#start_date').val(),
                end_month : $('#end_date').val(),
            },
            type : 'POST',
            url : '/customerProcessSpending'
        })

        .done(function (data) {
            console.log(data["data"]);
            if (data["data"]){
                /*clean previous chart*/
                document.getElementById("customer_track_spending").innerHTML = "";
                /*create high chart*/
                chart_data = data["data"];
                var myChart = Highcharts.chart("customer_track_spending", {
                    chart: {
                        type: chart_type
                    },
                    title: {
                        text: chart_data["title"]
                    },
                    xAxis: {
                        categories: chart_data["xAxis_categories"]
                    },
                    yAxis: {
                        title: {
                            text: chart_data["yAxis_title_text"]
                        }
                    },
                    series: [{
                        data: chart_data["series1_data"]
                    }]
                });
                /*refresh monthly spending data*/
                document.getElementById("spending_by_range").innerHTML = "";
                document.getElementById("spending_by_range").innerHTML = "Period Spending Sum:" + chart_data["total_spending_in_range"];

            }

            else {
                /*clean previous data*/
                document.getElementById('customer_track_spending').innerHTML = '';
                li = document.createElement('li');
                li.innerHTML = data["error"];
                document.getElementById("customer_track_spending").appendChild(li);
            }
        });
        event.preventDefault();
    });
});