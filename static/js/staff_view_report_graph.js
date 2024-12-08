document.addEventListener('DOMContentLoaded', function () {
    var Chart1 = Highcharts.chart(chart1_id, {
        chart: {
            type: chart1_type
        },
        title: {
            text: c1title
        },
        xAxis: {
            categories: c1xAxis_categories
        },
        yAxis: {
            title: {
                text: c1yAxis_title_text
            }
        },
        series: [{
            name: c1series1_name,
            data: c1series1_data
        }]
    });
});
