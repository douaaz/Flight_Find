document.addEventListener('DOMContentLoaded', function () {
    var myChart = Highcharts.chart(chart_id, {
        chart: {
            type: chart_type
        },
        title: {
            text: title
        },
        xAxis: {
            categories: xAxis_categories
        },
        yAxis: {
            title: {
                text: yAxis_title_text
            }
        },
        series: [{
            name: series1_name,
            data: series1_data
        }]
    });
});
