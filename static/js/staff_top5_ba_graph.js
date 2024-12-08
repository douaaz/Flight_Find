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

    var Chart2 = Highcharts.chart(chart2_id, {
        chart: {
            type: chart2_type
        },
        title: {
            text: c2title
        },
        xAxis: {
            categories: c2xAxis_categories
        },
        yAxis: {
            title: {
                text: c2yAxis_title_text
            }
        },
        series: [{
            name: c2series1_name,
            data: c2series1_data
        }]
    });

    var Chart3 = Highcharts.chart(chart3_id, {
        chart: {
            type: chart3_type
        },
        title: {
            text: c3title
        },
        xAxis: {
            categories: c3xAxis_categories
        },
        yAxis: {
            title: {
                text: c3yAxis_title_text
            }
        },
        series: [{
            name: c3series1_name,
            data: c3series1_data
        }]
    });
});
