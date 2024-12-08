$(document).ready(function () {
    $('form').on('submit', function (event) {
        $.ajax({
            data:{
                year : $('#year').val(),
                month : $('#month').val(),
                start_day : $('#start_date').val(),
                end_day : $('#end_date').val(),
            },
            type : 'POST',
            url : '/customerProcessSpending'
        })

        .done(function (data) {
            console.log(data["data"]);
            if (data["data"]){
                /*clean previous chart*/
                document.getElementById("top5_by_tickets").innerHTML = "";
                document.getElementById("top5_by_commission").innerHTML = "";
                /*create high chart*/
                chart_data = data["data"];
                var Chart1 = Highcharts.chart("top5_by_tickets", {
                    chart: {
                        type: chart1_type
                    },
                    title: {
                        text: chart_data["c1title"]
                    },
                    xAxis: {
                        categories: chart_data["c1xAxis_categories"]
                    },
                    yAxis: {
                        title: {
                            text: chart_data["c1yAxis_title_text"]
                        }
                    },
                    series: [{
                        data: chart_data["c1series1_data"]
                    }]
                });
                var Chart2 = Highcharts.chart("top5_by_commission", {
                    chart: {
                        type: chart2_type
                    },
                    title: {
                        text: chart_data["c2title"]
                    },
                    xAxis: {
                        categories: chart_data["c2xAxis_categories"]
                    },
                    yAxis: {
                        title: {
                            text: chart_data["c2yAxis_title_text"]
                        }
                    },
                    series: [{
                        data: chart_data["c2series1_data"]
                    }]
                });
            }

            else {
                /*clean previous data*/
                document.getElementById('top5_by_tickets').innerHTML = '';
                document.getElementById('top5_by_commission').innerHTML = '';
                li = document.createElement('li');
                li.innerHTML = data["error"];
                document.getElementById("top5_by_tickets").appendChild(li);
                document.getElementById("top5_by_commission").appendChild(li);
            }
        });
        event.preventDefault();
    });
});