$(document).ready(function () {
    $('#search').on('submit', function (event) {
        $.ajax({
            data:{
                start_date : $('#start_date').val(),
                end_date : $('#end_date').val(),
            },
            type : 'POST',
            url : '/baProcessCommission'
        })

        .done(function (data) {
            console.log(data["data"]);
            if (data["data"]){
                /*clean previous chart*/
                /*document.getElementById("commission_chart").innerHTML = "";*/
                /*create high chart*/

                chart_data = data["data"];
/*
                var myChart = Highcharts.chart("commission_chart", {
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
*/
                /*refresh <p> data*/
                document.getElementById("total_commission").innerHTML = "";
                document.getElementById("total_commission").innerHTML = "Total Commission: " + chart_data["total_commission"];
                document.getElementById("commission_by_range").innerHTML = "";
                document.getElementById("commission_by_range").innerHTML = "Average Commission: " + chart_data["average_commission_in_range"];
                document.getElementById("sold_ticket_num").innerHTML = "";
                document.getElementById("sold_ticket_num").innerHTML = "Number of tickets sold: " + chart_data["sold_ticket_num"];

            }

            else {
                /*clean previous data*/
                document.getElementById("total_commission").innerHTML = "";
                document.getElementById("commission_by_range").innerHTML = "";
                document.getElementById("sold_ticket_num").innerHTML = "";
                var li = document.createElement('li');
                li.innerHTML = data["error"];
                document.getElementById("total_commission").appendChild(li);
                document.getElementById("commission_by_range").appendChild(li);
                document.getElementById("sold_ticket_num").appendChild(li);
            }
        });
        event.preventDefault();
    });
});